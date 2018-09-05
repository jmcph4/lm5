class Input(object):
    def __init__(self, type, data):
        self.__type = type
        self.__data = deepcopy(data)

    def __repr__(self):
        return repr(self.__data)

    def __str__(self):
        return str(self.__type) + str(self.__data)

