import os
from time import time
from gherkin.parser import Parser
from gherkin.pickles.compiler import compile
from gherkin.errors import CompositeParserException
from . import _in_step
from ._custom_exceptions import ParserException, print_error, CustomException
from ._enums import Type, Status, Colours, Tags
from ._project_config import config


class StepsQueue:
    def __init__(self, methods, webdriver):
        self.features = []
        self.queue_list = []
        self.methods = methods
        self.parser = Parser()
        self.webdriver = webdriver
        self.passed_steps = 0
        self.passed_scenarios = 0
        self.failed_steps = 0
        self.failed_scenarios = 0
        self.wip_tag_flag = False
        self.first_scenario_flag = True
        self.log = ''

    def prepare_steps(self):
        try:
            self._load_features_files()
            self._status_update()

        except ParserException as e:
            raise ParserException(e)

        except CompositeParserException as e:
            print_error(e)
            raise ParserException

    def start(self):
        start = time()
        for feature in self.features:
            if feature.status is Status.PENDING:
                self._each_feature(feature)

        finish_time = '%.2f' % (time() - start)
        self._print_summary(finish_time)

    def _each_feature(self, feature):
        self._print_gherkin(Type.FEATURE, feature.text)
        for scenario in feature.scenarios:
            if scenario.status is Status.PENDING:
                self._each_scenario(scenario)

    def _each_scenario(self, scenario):
        if self.first_scenario_flag:
            self.first_scenario_flag = False

        else:
            self.webdriver.refresh_webdriver()

        self._print_gherkin(Type.SCENARIO, scenario.text)
        for step in scenario.steps:
            if self._each_step(step) is not Status.SUCCESS:
                scenario.status = Status.FAILED
                self.failed_scenarios += 1
                return

        scenario.status = Status.SUCCESS
        self.passed_scenarios += 1

    def _each_step(self, step):
        try:
            step.add_webdriver_to_params(self.webdriver)
            step.call_method(self.methods)
            step.status = Status.SUCCESS

        except CustomException as e:
            step.status = Status.FAILED
            step.error = e

        except Exception as e:  #todo
            step.status = Status.FAILED
            step.error = e

        finally:
            self._print_gherkin(Type.STEP, step.text, status=step.status)
            if step.error is not None:
                print_error(step.error)

            if step.status is None:
                raise

            if step.status is Status.SUCCESS:
                self.passed_steps += 1

            elif step.status is Status.FAILED:
                self.failed_steps += 1

            return step.status

    def _print_gherkin(self, type, text, status=None):
        tab = '    '
        if type == Type.FEATURE:
            self._print_and_log()
            self._print_and_log(Colours.CYAN + text + Colours.DEFAULT)

        elif type == Type.SCENARIO:
            self._print_and_log(Colours.CYAN + tab + text + Colours.DEFAULT)

        elif type == Type.STEP:
            if status == Status.SUCCESS:
                self._print_and_log(tab + tab + Colours.GREEN + text + Colours.DEFAULT, status)

            elif status == Status.FAILED:
                self._print_and_log(tab + tab + Colours.RED + text + Colours.DEFAULT, status)

    def _print_summary(self, finish_time):
        self._print_and_log()
        self._print_and_log()
        self._print_and_log(Colours.GREEN + 'PASSED SCENARIOS: ' + str(self.passed_scenarios) + Colours.DEFAULT)
        self._print_and_log(Colours.RED + 'FAILED SCENARIOS: ' + str(self.failed_scenarios) + Colours.DEFAULT)
        self._print_and_log()
        self._print_and_log(Colours.GREEN + 'PASSED STEPS: ' + str(self.passed_steps) + Colours.DEFAULT)
        self._print_and_log(Colours.RED + 'FAILED STEPS: ' + str(self.failed_steps) + Colours.DEFAULT)
        self._print_and_log()
        self._print_and_log(Colours.GREEN + 'Finished in: ' + finish_time + 'sec' + Colours.DEFAULT)

    def _print_and_log(self, text='', status=''):
        if status != '':
            status = ' (' + status + ')'
        print(text)
        self.log = '\n'.join((self.log, text + status))

    def _load_features_files(self):
        try:
            if not os.listdir(config['directory_path']['paths']['features']):
                raise ParserException('features directory is empty')

        except FileNotFoundError:
            raise ParserException('features directory not found')

        for feature_file in os.listdir(config['directory_path']['paths']['features']):
            self._open_feature_file(config['directory_path']['paths']['features'] + feature_file)

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
        self.features.append(Feature(feature))
        for scenario in pickles:
            self._read_gherkin_scenario(scenario)

    def _read_gherkin_scenario(self, scenario_object):
        scenario = scenario_object['name']
        self.features[-1].add_scenario(Scenario(scenario))
        tags = scenario_object['tags']
        for tag in tags:
            self._read_gherkin_tag(tag)

        steps = scenario_object['steps']
        for step in steps:
            self._read_gherkin_step(step)

    def _read_gherkin_tag(self, tag):
        self.features[-1].tag = tag['name']
        self.features[-1].scenarios[-1].tag = tag['name']
        if tag['name'] == Tags.WIP:
            self.wip_tag_flag = True

    def _read_gherkin_step(self, step):
        self.features[-1].scenarios[-1].add_step(Step(step['text']))

    def _status_update(self):
        for feature in self.features:
            self._status_update_feature(feature)

    def _status_update_feature(self, feature):
        feature.status = Status.SKIPPED
        for scenario in feature.scenarios:
            self._status_update_scenario(feature, scenario)

    def _status_update_scenario(self,feature, scenario):
        self._skip_or_pending(scenario)
        for step in scenario.steps:
            self._status_update_step(scenario, step)

        if scenario.status is Status.PENDING:
            feature.status = Status.PENDING

    def _status_update_step(self, scenario, step):
        if scenario.status is Status.SKIPPED:
            step.status = Status.SKIPPED

        else:
            step.status = Status.PENDING

    def _skip_or_pending(self, item):
        if self.wip_tag_flag and item.tag == Tags.WIP:
            item.status = Status.PENDING
            return

        if not self.wip_tag_flag and (item.tag != Tags.DISABLED):  # todo != or is not
            item.status = Status.PENDING
            return

        item.status = Status.SKIPPED


class Feature:
    def __init__(self, text):
        self.scenarios = []
        self.text = text
        self.tag = ''
        self.status = None

    def add_scenario(self, scenario):
        self.scenarios.append(scenario)


class Scenario:
    def __init__(self, text):
        self.steps = []
        self.tag = ''
        self.text = text
        self.status = None

    def add_step(self, step):
        self.steps.append(step)


class Step:
    def __init__(self, step):
        self.text = step
        self.parameters = _in_step.find_params(step)
        self.text_without_params = _in_step.find_text_without_params(step)
        self.method = None
        self.status = None
        self.error = None

    def call_method(self, methods):
        self._find_method(methods)
        self.method(*self.parameters)

    def add_webdriver_to_params(self, webdriver):
        self.parameters = (webdriver, *self.parameters)

    def _find_method(self, methods):
        self.method = methods.find_gherkin(self.text_without_params)
