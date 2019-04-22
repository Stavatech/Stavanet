from django.db import models
from django.contrib.auth.models import User, Group

from files.service.models.files import FileSyncState

import uuid


class Directory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column="id")
    name = models.CharField(max_length=255, db_column="name")
    path = models.CharField(max_length=1023, unique=True)
    parent = models.ForeignKey('Directory', on_delete=models.CASCADE, null=True, blank=True, related_name='directories')

    def __str__(self):
        return self.path
    
    # class Meta:
    #     db_table = "Directories"


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column="id")
    current_version = models.OneToOneField("FileVersion", on_delete=models.CASCADE,
        null=True, blank=True, db_column="current_version_id", related_name="current_version_of")

    class Meta:
        db_table = 'Files'


class FileVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column="id")
    name = models.CharField(max_length=255, db_column="name")
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE, db_column="directory_id", related_name='files')
    created_date = models.DateTimeField(auto_now_add=True, db_column="created_date")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column="created_by", related_name="file_edits")
    size = models.IntegerField(db_column="size")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_column="owner", related_name="file_versions_owned")
    file = models.ForeignKey(File, on_delete=models.CASCADE, db_column="file_id", related_name="versions")

    def __str__(self):
        return self.directory.path + '/' + self.name

    class Meta:
        db_table = "FileVersions"


class FileSyncStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column="id")
    storage_service = models.CharField(max_length=32)
    file_version = models.ForeignKey(FileVersion, on_delete=models.CASCADE, db_column="file_version_id", related_name="sync_states")
    status = models.IntegerField(default=FileSyncState.NOT_STARTED)
    message = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "FileSyncStates"
        unique_together = (('storage_service', 'file_version'),)


class FileUserAccessPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column="id")
    file = models.ForeignKey(File, on_delete=models.CASCADE, db_column="file_id", related_name="user_permissions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", related_name="user_files")
    can_read = models.BooleanField()
    can_write = models.BooleanField()

    class Meta:
        db_table = "FileUserAccessPermissions"


class FileGroupAccessPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column="id")
    file = models.ForeignKey(File, on_delete=models.CASCADE, db_column="file_id", related_name="group_permissions")
    group = models.ForeignKey(User, on_delete=models.CASCADE, db_column="group_id", related_name="group_files")
    can_read = models.BooleanField()
    can_write = models.BooleanField()

    class Meta:
        db_table = "FileGroupAccessPermissions"
