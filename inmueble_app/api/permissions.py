from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        # print('User' in str(request.user.groups.all()))
        if request.method == 'GET':
            return True

        staff_permissions = bool(request.user and request.user.is_staff)
        return staff_permissions


class IsCommentUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.user == request.user or obj.user.is_staff
