import json

registry = {}

def register_class(target_class):
    print 'Registering {}'.format(target_class.__name__)
    registry[target_class.__name__] = target_class

class SerializableMeta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(
            target_class=cls
        )
        return cls

def deserialize(data):
    params = json.loads(data)
    target_class = registry[params['class']]
    return target_class(*params['args'])

class Serializable(object):
    __metaclass__ = SerializableMeta

    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({
            'args': self.args,
            'class': self.__class__.__name__
        })

class Point2D(Serializable):
    def __init__(self, x, y):
        super(Point2D, self).__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point2D({}, {})'.format(self.x, self.y)

class Point3D(Serializable):
    def __init__(self, x, y, z):
        super(Point3D, self).__init__(x, y, z)
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return 'Point3D({}, {}, {})'.format(self.x, self.y, self.z)
