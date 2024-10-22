from django.http import HttpResponseForbidden

class RoleRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to access this page.")

        # Check if user role is in the allowed roles
        if request.user.role not in self.allowed_roles:
            return HttpResponseForbidden("You do not have permission to access this page.")
        

        return super().dispatch(request, *args, **kwargs)
