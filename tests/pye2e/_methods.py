import os
import sys
from importlib import import_module
from ._enums import Directories
from ._custom_exceptions import MethodsException


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
        if not os.listdir(Directories.PAGES):
            raise MethodsException('pages directory is empty')

        for step_file in os.listdir(Directories.PAGES):
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
        class_vars = [attr for attr in dir(Directories) if
                      not callable(getattr(Directories, attr)) and not attr.startswith('__')]
        for var in class_vars:
            path = getattr(Directories, var)
            sys.path.append(path) # todo sys.path.insert(1, path)
