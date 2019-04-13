from django.db import models
from django.contrib.auth.models import User, Group


class FileStorageService(object):
    LOCAL = "LOCAL"
    AWS_S3 = "AWS S3"
    AWS_GLACIER = "AWS GLACIER"
    AZURE_BLOB = "AZURE BLOB STORAGE"


class FileSyncState(object):
    NOT_STARTED = 0
    IN_PROGRESS = 10
    SUCCESS = 20
    ERROR = 40


class File(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, db_column="id")
    name = models.CharField(max_length=255, db_column="name")
    path = models.CharField(max_length=1023, db_column="path")
    current_version = models.OneToOneField("FileVersion", on_delete=models.CASCADE,
        null=True, blank=True, db_column="current_version_id", related_name="current_version_of")

    class Meta:
        db_table = 'Files'


class FileVersion(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, db_column="id")
    created_date = models.DateTimeField(auto_now_add=True, db_column="created_date")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column="created_by", related_name="file_edits")
    size = models.DecimalField(max_digits=128, decimal_places=32, db_column="size")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_column="owner", related_name="file_versions_owned")
    file = models.ForeignKey(File, on_delete=models.CASCADE, db_column="file_id", related_name="versions")

    class Meta:
        db_table = "FileVersions"


class FileSyncStatus(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, db_column="id")
    storage_service = models.CharField(max_length=32)
    file = models.ForeignKey(File, on_delete=models.CASCADE, db_column="file_id", related_name="sync_states")
    status = models.IntegerField(default=FileSyncState.NOT_STARTED)
    message = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "FileSyncStates"


class FileUserAccessPermission(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, db_column="id")
    file = models.ForeignKey(File, on_delete=models.CASCADE, db_column="file_id", related_name="user_permissions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", related_name="user_files")
    can_read = models.BooleanField()
    can_write = models.BooleanField()

    class Meta:
        db_table = "FileUserAccessPermissions"


class FileGroupAccessPermission(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, db_column="id")
    file = models.ForeignKey(File, on_delete=models.CASCADE, db_column="file_id", related_name="group_permissions")
    group = models.ForeignKey(User, on_delete=models.CASCADE, db_column="group_id", related_name="group_files")
    can_read = models.BooleanField()
    can_write = models.BooleanField()

    class Meta:
        db_table = "FileGroupAccessPermissions"
