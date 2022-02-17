"""
This class converts dictionaries to have hierarchical random access.
it is used to make the configuration easier to edit
"""

class DictionaryRepresentor(object):
    def __init__(self, d):
        for key, value in d.items():
            d[key] = self.__make_representable(value)
        super(DictionaryRepresentor, self).__setattr__('__dict__', d)

    def __hash__(self):
        raise TypeError(f"unhashable type: {self.__class__.__name__}")

    def __eq__(self, other):
        if isinstance(other, DictionaryRepresentor):
            return self.as_dict() == other.as_dict()
        elif isinstance(other, dict):
            return self.as_dict() == other
        return False

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()

    def __setattr__(self, key, value):
        super(DictionaryRepresentor, self).__setattr__(key, self.__make_representable(value))

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, item):
        d = dict(self.__dict__)
        return d[item]

    def as_dict(self):
        converted_dict = dict(self.__dict__)
        for key, value in converted_dict.items():
            converted_dict[key] = self.__unrepresent_dictionary(value)
        return converted_dict

    def __make_representable(self, value):
        if isinstance(value, list):
            return [self.__make_representable(current_list_entry) for current_list_entry in value]
        if isinstance(value, dict):
            return DictionaryRepresentor(value)
        return value

    def __unrepresent_dictionary(self, value):
        if isinstance(value, list):
            return [self.__unrepresent_dictionary(current_list_entry) for current_list_entry in value]
        if isinstance(value, DictionaryRepresentor):
            return value.as_dict()
        return value
