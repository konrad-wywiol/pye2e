import os
import sys
from importlib import import_module
from ._custom_exceptions import MethodsException
from ._project_config import config


class Methods:
    def __init__(self):
        self.methods_list = []

    def find_gherkin(self, text):
        try:
            for method in self.methods_list:
                if method.step_text_without_params == text:
                    return method

        except MethodsException as e:
            raise MethodsException(e)

    def load_all_methods(self):
        try:
            self._fix_sys_paths()
            modules = self._import_all_steps_files()
            for module in modules:
                self._find_all_methods_in_module(module)

        except MethodsException as e:
            raise MethodsException(e)

    def _import_all_steps_files(self):
        steps_files = []
        try:
            if not os.listdir(config['directory_path']['paths']['steps']):
                raise MethodsException('steps directory is empty')

        except FileNotFoundError:
            raise MethodsException('steps directory not found')

        for step_file in os.listdir(config['directory_path']['paths']['steps']):
            if step_file == '__init__.py' or step_file[-3:] != '.py':
                continue
            steps_files.append(import_module(step_file[:-3]))
        return steps_files

    def _find_all_methods_in_module(self, module):
        for item in dir(module):
            maybe_method = getattr(module, item)
            if callable(maybe_method) and hasattr(maybe_method, 'decorator'):
                self.methods_list.append(maybe_method)

    def _fix_sys_paths(self):
        sys.path.append(config['directory_path']['paths']['features'])  # todo sys.path.insert(1, path)
        sys.path.append(config['directory_path']['paths']['steps'])
