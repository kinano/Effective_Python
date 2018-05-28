
class ValidateBusinessClass(type):
    def __new__(meta, name, bases, class_dict):
        print((meta, name, bases, class_dict))
        if bases != (object,):
            if 'validate' not in class_dict:
                raise Exception('{} must implement validate()'.format(name))

            if class_dict['sides'] < 3:
                raise Exception('{} must have at least 3 sides'.format(name))

        return type.__new__(meta, name, bases, class_dict)

class AbstractClass(object):
    __metaclass__ = ValidateBusinessClass
    sides = None

    def commonMethod():
        pass

class BadBusinessClass(AbstractClass):
    sides = 4
    def validate():
        pass

class GoodBusinessClass(AbstractClass):
    sides = 3
    def validate():
        pass
