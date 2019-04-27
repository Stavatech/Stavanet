from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from django.conf import settings
from django.http import HttpResponse

from files.service.service import FileService
from utils.functions import dynamic_import

from wsgiref.util import FileWrapper

import json


files_dao = dynamic_import(settings.FILE_SVC['service_args']['files_dao'])()
storage_adapter = dynamic_import(settings.FILE_SVC['service_args']['storage_adapter'])()
file_svc = FileService(storage_adapter, files_dao, settings.FILE_SVC['service_args']['root_path'])


class FileList(APIView):
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request):
        file_obj = request.FILES['file']
        path = request.POST.get('path', '/')
        file_entry = file_svc.put_file(file_name=file_obj.name, directory_path=path, file_stream=file_obj, user=request.user)
        return Response(data=file_entry.to_dict())

    def get(self, request):
        path = request.GET.get('path', '/')
        files = file_svc.list_directory(path)
        files_dict = list(map(lambda o: o.to_dict(), files))
        return Response(data=files_dict)
    

class FileDownload(APIView):
    def get(self, request, id):
        file_entry, file_handle = file_svc.get_file(id)

        wrapper = FileWrapper(file_handle)
        response = HttpResponse(wrapper)
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_entry.name
        response['Content-Length'] = file_entry.size
        
        return response
