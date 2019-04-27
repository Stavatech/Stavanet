from django.db import transaction
from django.contrib.auth.models import User, Group

from files.service.models.files import (
    FileSyncStatus as FileSyncStatusModel, 
    File as FileModel,
    Directory as DirectoryModel,
    FileSyncState,
    FileStorageService
)
from files.models import (
    File, 
    FileGroupAccessPermission, 
    FileSyncStatus, 
    FileUserAccessPermission, 
    FileVersion,
    Directory
)


class DjangoFileDAO(object):
    def put_directory(self, path) -> list:
        dirs = path.split('/')
        name = dirs[-1]

        parent_path = '/'.join(dirs[:-1]) if len(dirs) > 2 else '/'
        parent = Directory.objects.get(path=parent_path) if path is not '/' else None

        current_dir, created = Directory.objects.get_or_create(
            name=name,
            path=path,
            parent=parent
        )
        print("Created '%s'" % path if created else "Directory '%s' already exists" % path)
        
        return self.list_directory(path)
    
    def list_directory(self, path) -> list:
        directories = self.get_directories(path)
        files = self.get_files(path)
        return directories + files
    
    def get_directory(self, path) -> DirectoryModel:
        directory = Directory.objects.get(path=path)
        return self._transform_directory(directory)
    
    def get_directories(self, path) -> list:
        directories = Directory.objects.filter(parent__path=path)
        return self._transform_directories(directories)
    
    def get_file(self, id) -> FileModel:
        file_obj = File.objects.get(current_version__id=id)
        return self._transform_file(file_obj)

    def get_files(self, path) -> list:
        files = File.objects.filter(current_version__directory__path=path)
        return self._transform_files(files)

    def put_file(self, id, name: str, directory_path: str, file_size: int, user: User) -> FileModel:
        user = User.objects.all()[0]

        with transaction.atomic():
            try:
                file_obj = File.objects.get(current_version__name=name, current_version__directory__path=directory_path)
            except Exception as ex:
                file_obj = File.objects.create()

            new_version = FileVersion.objects.create(
                id=id,
                name=name,
                directory=Directory.objects.get(path=self.get_directory(directory_path).path),
                created_by=user,
                size=file_size,
                owner=user,
                file=file_obj
            )

            sync_status = self.update_sync_status(new_version.id, FileStorageService.LOCAL, FileSyncState.SUCCESS)

            file_obj.current_version = new_version
            file_obj.save()

        return self._transform_file(file_obj)
    
    def update_file_size(self, file_version_id: str, size: int) -> None:
        file_version = FileVersion.objects.get(id=file_version_id)
        file_version.size = size
        file_version.save()
    
    def update_sync_status(self, file_version_id: str, storage_service: str, status: str):
        file_version = FileVersion.objects.get(id=file_version_id)

        try:
            sync_status = FileSyncStatus.objects.get(
                storage_service=storage_service,
                file=root_file
            )
        except Exception as ex:
            sync_status = FileSyncStatus.objects.create(
                storage_service=FileStorageService.LOCAL,
                file_version=file_version,
                status=status
            )
        
        sync_status.status = status
        sync_status.save()

        return self._transform_sync_states(file_version_id, [sync_status])[0]

    def _transform_file(self, file_obj: File) -> FileModel:
        current_version = file_obj.current_version
        sync_states = self._transform_sync_states(current_version.id, current_version.sync_states.all())
        return FileModel(
            id=str(current_version.id),
            path=current_version.directory.path,
            name=current_version.name,
            created_date=str(file_obj.current_version.created_date),
            created_by=current_version.created_by.username,
            owner=current_version.owner.username,
            size=current_version.size,
            sync_states=sync_states
        )
    
    def _transform_files(self, file_objs: list) -> list:
        return list(map(lambda x: self._transform_file(x), file_objs))
    
    def _transform_directory(self, directory: Directory) -> DirectoryModel:
        return DirectoryModel(id=str(directory.id), name=directory.name, path=directory.path, parent=directory.parent.path)
    
    def _transform_directories(self, directories: list) -> list:
        return list(map(lambda x: self._transform_directory(x), directories))

    def _transform_sync_state(self, file_version_id, sync_state) -> FileSyncStatusModel:
        return FileSyncStatusModel(file_id=str(file_version_id), storage_service=sync_state.storage_service, status=sync_state.status)

    def _transform_sync_states(self, file_version_id, sync_states) -> list:
        return list(map(lambda x: self._transform_sync_state(file_version_id, x), sync_states))