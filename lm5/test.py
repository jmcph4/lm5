from copy import deepcopy

from .inputtype import InputType
from .errors import UnsupportedInputTypeError


class Test(object):
    def __init__(self, target, supported_types, name=None):
        self.__target = deepcopy(target)
        self.__types = set(deepcopy(supported_types))
        self.__inputs = {}

        if name is None:
            self.__name = "Test"
        else:
            self.__name = name

    @property
    def name(self):
        return self.__name

    @property
    def types(self):
        return self.__types

    def add_input(self, type, data):
        if type in self.__types:
            self.__inputs[type] = data
        else:
            raise UnsupportedInputTypeError()

    def remove_input(self, type):
        if type in self.__types:
            self.__inputs.pop(type)
        else:
            raise UnsupportedInputTypeError()

    def run(self):
        target = self.__init_target()
        target.exec()

        return (target.retval, target.stdout, target.stderr)

    def from_config(self, config_data):
        fields = config_data.keys()
        
        if InputType.ARGV in fields:
            self.add_input(InputType.ARGV, config_data[InputType.ARGV])

        if InputType.STDIN in fields:
            self.add_input(InputType.STDIN, config_data[InputType.STDIN])

    def __init_target(self):
        target = deepcopy(self.__target)

        if InputType.ARGV in self.__inputs.keys():
            args = self.__inputs[InputType.ARGV]

            for i in range(len(args)):
                arg = args[i]
                target.add_arg(i, arg)

        if InputType.STDIN in self.__inputs.keys():
            target.append_string_stdin(self.__inputs[InputType.STDIN])

        return target

