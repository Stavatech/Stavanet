class StorageAdapter(object):
    def __new__(cls, *args, **kwargs):
        if cls is StorageAdapter:
            raise StorageAdapter("StorageAdapter class may not be instantiated")
        return object.__new__(cls, *args, **kwargs)

    def list_directory(self, path: str) -> list:
        raise NotImplementedError()
    
    def write_file(self, path: str, content: bytes) -> None:
        raise NotImplementedError()
    
    def get_file(self, path: str) -> bytes:
        raise NotImplementedError()
    
    def describe_file(self, path: str) -> dict:
        raise NotImplementedError()
