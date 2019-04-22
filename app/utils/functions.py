from importlib import import_module


def dynamic_import(path):
    module_path = '.'.join(path.split('.')[:-1])
    obj_name = path.split('.')[-1]
    module = import_module(module_path)
    return getattr(module, obj_name)