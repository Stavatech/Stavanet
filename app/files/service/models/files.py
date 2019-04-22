import json, pickle


class SerializableObject(object):
    def pickle(self):
        return pickle.dumps(self)
    
    def to_JSON(self):
        return json.dumps(self, default=lambda o: self._try(o), sort_keys=True, indent=4, separators=[",", ":"])
    
    def to_dict(self):
        return json.loads(self.to_JSON())
    
    def _try(self, field):
        try:
            return vars(field)
        except:
            return str(field)


class FileStorageService(SerializableObject):
    LOCAL = "LOCAL"
    AWS_S3 = "AWS S3"
    AWS_GLACIER = "AWS GLACIER"
    AZURE_BLOB = "AZURE BLOB STORAGE"


class FileSyncState(SerializableObject):
    NOT_STARTED = 0
    IN_PROGRESS = 10
    SUCCESS = 20
    ERROR = 40


class File(SerializableObject):
    def __init__(self, id: str, path: str, name: str, created_by: float, 
                 created_date: str, size: int, owner: str, sync_states: list):
        self.id = id
        self.path = path
        self.name = name
        self.created_date = created_date
        self.created_by = created_by
        self.size = size
        self.owner = owner
        self.sync_states = sync_states
        self.type = "file"


class Directory(SerializableObject):
    def __init__(self, id: str, path: str, name: str, parent: str):
        self.id = id
        self.path = path
        self.name = name
        self.parent = parent
        self.type = "directory"


class FileSyncStatus(SerializableObject):
    def __init__(self, file_id: str, storage_service: str, status: str):
        self.file_id = file_id
        self.storage_service = storage_service
        self.status = status
