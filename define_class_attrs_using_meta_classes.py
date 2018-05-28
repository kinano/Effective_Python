
class Field(object):
    name = None
    internal_name = None

class FieldMeta(type):
    def __new__(meta, name, bases, class_dict):
        for k, v in class_dict.iteritems():
            print 'checking {}'.format(v)
            if isinstance(v, Field):
                print 'v is field!!!'
                v.name = k
                v.internal_name = '_' + v.name

        cls = type.__new__(meta, name, bases, class_dict)

        return cls

class DBRow(object):
    __metaclass__ = FieldMeta

class Customer(DBRow):
    first_name = Field()
    last_name = Field()
