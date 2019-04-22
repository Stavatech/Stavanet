from rest_framework.views import APIView

from files.apps import FilesConfig

import functools

def inject_config(cls):
    class ClassWrapper(APIView):
        def __init__(self):
            self.decorated_class = cls

        def __call__(self,*cls_ars):
            decorated_class = self.decorated_class(*cls_ars)
            setattr(decorated_class, 'settings', FilesConfig.settings)
            return decorated_class

    return ClassWrapper
