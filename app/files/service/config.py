


def configure(cls):
    class ConfiguredService(object):
        def __init__(self):
            self.decorated_class = cls

        def __call__(self,*cls_ars):
            decorated_class = self.decorated_class(**settings['service_args'])
            return decorated_class

    return ConfiguredService
