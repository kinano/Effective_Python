class Lazy(object):
    def __init__(self):
        self.exists = 5

    # def __getattr__(self, name):
    #     print '__getattr__ was called for {}'.format(name)
    #     value = 'wahaha {}'.format(name)
    #     setattr(self, name, value)
    #     return value

    def __getattribute__(self, name):
        print 'Called __getattribute__({})'.format(name)
        try:
            return super(Lazy, self).__getattribute__(name)
        except Exception:
            print 'Exception for {}'.format(name)
            setattr(self, name, 'wahahahahaha')
            return value

    def __setattr__(self, name, value):
        print 'Called __setattr__ {} {}'.format(name, value)
        super(Lazy, self).__setattr__(name, value)

def main():

    data = Lazy()
    print 'Before {}'.format(data.__dict__)
    # print 'booo exists? {}'.format(hasattr(data, 'booo'))
    # print 'After {}'.format(data.__dict__)
    # print 'One more {}'.format(data.booo)
    print 'BEFORE {}'.format(data.__dict__)
    data.booo = 'wahahahaha'
    print 'AFTER {}'.format(data.__dict__)
    data.booo = 'wehehehee'
    print 'AFTER2 {}'.format(data.__dict__)
