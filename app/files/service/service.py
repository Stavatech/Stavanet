from files.service.adapters.storage_adapter import StorageAdapter
from files.service.dao.django.files import DjangoFileDAO

from files.service.models.files import File, FileStorageService, FileSyncState

from django.contrib.auth.models import User

import os, uuid


class FileService(object):
    def __init__(self, storage_adapter: StorageAdapter, file_dao: DjangoFileDAO, root_path: str):
        self.storage_adapter = storage_adapter
        self.file_dao = file_dao
        self.root_path = root_path
    
    def create_directory(self, path: str):
        path = path.strip()

        if not path.startswith('/'):
            path = '/' + path

        current_directory = None
        current_path = '/'

        for directory in path.split('/'):
            current_path = os.path.join(current_path, directory)
            current_directory = self.file_dao.put_directory(current_path)

        return current_directory
    
    def put_file(self, file_name: str, directory_path: str, file_stream: bytes, user: User) -> File:
        file_id = str(uuid.uuid4())

        self.create_directory(directory_path)

        file_size = self.storage_adapter.write_file(
            os.path.join(self.root_path, file_id),
            file_stream
        ).get('size', 0)

        return self.file_dao.put_file(file_id, file_name, directory_path, file_size, user)
    
    def list_directory(self, path) -> list:
        return self.file_dao.list_directory(path)
       