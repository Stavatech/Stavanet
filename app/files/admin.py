from django.contrib import admin
from .models import Directory, File, FileGroupAccessPermission, FileSyncStatus, FileUserAccessPermission, FileVersion

admin.site.register(Directory)
admin.site.register(File)
admin.site.register(FileGroupAccessPermission)
admin.site.register(FileSyncStatus)
admin.site.register(FileUserAccessPermission)
admin.site.register(FileVersion)
