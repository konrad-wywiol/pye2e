import os
from gherkin.parser import Parser
from gherkin.pickles.compiler import compile
from gherkin.errors import CompositeParserException
from . import _in_step
from ._custom_exceptions import DriverException, ParserException, print_error
from ._enums import Directories, Type, Status, Colours


class StepsQueue:
    def __init__(self, methods, webdriver):
        self.features_list = []
        self.queue_list = []
        self.methods = methods
        self.parser = Parser()
        self.webdriver = webdriver
        self.passed_steps = 0
        self.failed_steps = 0
        self.wip_tag_flag = False
        self.first_scenario_flag = True

    def prepare_steps(self):
        try:
            self._load_features_files()

        except ParserException as e:
            raise ParserException(e)

        except CompositeParserException as e:
            print_error(e)
            raise ParserException

    def start(self):
        for feature in self.features_list:
            if self._skip_if_tag(feature.tag):
                continue
            self._each_feature(feature)
        self._print_summary()

    def _skip_if_tag(self, tag):
        if self.wip_tag_flag and tag == '@wip':
            return False

        if not self.wip_tag_flag:
            return False

        return True

    def _each_feature(self, feature):
        self._print_gherkin(Type.FEATURE, feature.feature_text)
        for scenario in feature.scenarios:
            if self._skip_if_tag(scenario.tag):
                continue
            self._each_scenario(scenario)

    def _each_scenario(self, scenario):
        if self.first_scenario_flag:
            self.first_scenario_flag = False

        else:
            self.webdriver.refresh_webdriver()

        self.first_scenario_flag = False
        self._print_gherkin(Type.SCENARIO, scenario.scenario_text)
        for step in scenario.steps:
            result = self._each_step(step)
            if result != Status.SUCCESS:
                break

    def _each_step(self, step):
        status = None
        error = None
        try:
            step.add_webdriver_to_params(self.webdriver)
            step.call_method(self.methods)
            status = Status.SUCCESS

        except TypeError as e:
            status = Status.FAILED
            error = e

        except DriverException as e:
            status = Status.FAILED
            error = e

        finally:
            self._print_gherkin(Type.STEP, step.text_without_params, status=status)
            if error is not None:
                print_error(error)

            if status is None:
                raise

            if status == Status.SUCCESS:
                self.passed_steps += 1

            else:
                self.failed_steps += 1

            return status

    def _print_gherkin(self, type, text, status=None):
        tab = '    '
        if type == Type.FEATURE:
            print()
            print(Colours.CYAN + text + Colours.DEFAULT)

        elif type == Type.SCENARIO:
            print(Colours.CYAN + tab + text + Colours.DEFAULT)

        elif type == Type.STEP:
            if status == Status.SUCCESS:
                print(tab + tab + Colours.GREEN + text + Colours.DEFAULT)

            elif status == Status.FAILED:
                print(tab + tab + Colours.RED + text + Colours.DEFAULT)

    def _print_summary(self):
        print()
        print(Colours.GREEN + 'PASSED: ' + str(self.passed_steps) + Colours.DEFAULT)
        if self.failed_steps == 0:
            print(Colours.RED + 'FAILED: ' + str(self.failed_steps) + Colours.DEFAULT)
        else:
            print(Colours.RED + 'FAILED: ' + str(self.failed_steps) + Colours.DEFAULT)

    def _load_features_files(self):
        if not os.listdir(Directories.FEATURES):
            raise ParserException('features directory is empty')

        for feature_file in os.listdir(Directories.FEATURES):
            self._open_feature_file(Directories.FEATURES + feature_file)

    def _open_feature_file(self, file_path):
        with open(file_path, 'r') as feature_file:
            gherkin_document = self.parser.parse(feature_file.read())
            self._read_gherkin(gherkin_document)

    def _read_gherkin(self, gherkin_document):
        try:
            pickles = compile(gherkin_document)
            feature = gherkin_document['feature']
            self._read_gherkin_feature(pickles, feature)

        except KeyError:
            pass

    def _read_gherkin_feature(self, pickles, feature_object):
        feature = feature_object['name']
        self.features_list.append(Feature(feature))
        for scenario in pickles:
            self._read_gherkin_scenario(scenario)

    def _read_gherkin_scenario(self, scenario_object):
        scenario = scenario_object['name']
        self.features_list[-1].add_scenario(Scenario(scenario))
        tags = scenario_object['tags']
        for tag in tags:
            self._read_gherkin_tag(tag)

        steps = scenario_object['steps']
        for step in steps:
            self._read_gherkin_step(step)

    def _read_gherkin_tag(self, tag):
        self.features_list[-1].tag = tag['name']
        self.features_list[-1].scenarios[-1].tag = tag['name']
        if tag['name'] == '@wip':
            self.wip_tag_flag = True

    def _read_gherkin_step(self, step):
        self.features_list[-1].scenarios[-1].add_step(Step(step['text']))


class Feature:
    def __init__(self, feature_text):
        self.scenarios = []
        self.feature_text = feature_text
        self.tag = ''

    def add_scenario(self, scenario):
        self.scenarios.append(scenario)


class Scenario:
    def __init__(self, scenario_text):
        self.steps = []
        self.tag = ''
        self.scenario_text = scenario_text

    def add_step(self, step):
        self.steps.append(step)


class Step:
    def __init__(self, step):
        self.text = step
        self.parameters = _in_step.find_params(step)
        self.text_without_params = _in_step.find_text_without_params(step)
        self.method = None

    def call_method(self, methods):
        self._find_method(methods)
        self.method(*self.parameters)

    def add_webdriver_to_params(self, webdriver):
        self.parameters = (webdriver, *self.parameters)

    def _find_method(self, methods):
        self.method = methods.find_gherkin(self.text_without_params)
