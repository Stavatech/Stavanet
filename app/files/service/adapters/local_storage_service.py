from files.service.adapters.storage_adapter import StorageAdapter

from _io import TextIOWrapper

import os


class LocalStorageAdapter(StorageAdapter):
    def list_directory(self, path: str) -> list:
        path, directories, files = next(os.walk(path))

        directories = map(lambda x: {"name": x, "is_dir": True}, directories)
        files = map(lambda x: {"name": x, "is_dir": False}, files)

        return list(directories) + list(files)
    
    def write_file(self, path: str, content: bytes) -> None:
        dirname = os.path.dirname(path)
        self.create_dir(dirname)
        
        with open(path, 'wb') as destination:
            for chunk in content.chunks():
                destination.write(chunk)

        return self.describe_file(path)
    
    def get_file(self, path: str) -> TextIOWrapper:
        return open(path, 'rb')
    
    def describe_file(self, path: str) -> dict:
        metadata = os.stat(path)
        return {
            'size': metadata.st_size,
            'user_id': metadata.st_uid,
            'group_id': metadata.st_gid,
            'content_modified_date': metadata.st_mtime,
            'metadata_modified_date': metadata.st_ctime
        }
    
    def create_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
