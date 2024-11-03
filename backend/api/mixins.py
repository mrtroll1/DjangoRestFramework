from rest_framework import permissions 

from .permissions import IsSatffEditorPermission

class StaffEditorPermissionMixin():
    permission_classes = [permissions.IsAdminUser, IsSatffEditorPermission]