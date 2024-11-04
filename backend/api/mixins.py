from rest_framework import permissions 

from .permissions import IsSatffEditorPermission

class StaffEditorPermissionMixin():
    permission_classes = [permissions.IsAdminUser, IsSatffEditorPermission]

class UserQuerySetMixin():
    user_field = 'user'
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        lookup_data = {}
        lookup_data[self.user_field] = user
        qs = super().get_queryset(*args, **kwargs)
        if user.is_staff: # can, for exmaple, define a helper to check if user.groups contains a certain group
            return qs
        return qs.filter(**lookup_data)