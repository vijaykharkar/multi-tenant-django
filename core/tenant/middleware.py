from .models import Tenant_User
from django.utils.deprecation import MiddlewareMixin

class TenantUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        domain = request.headers.get('X-Tenant-Domain')
        if domain:
            try:
                request.tenant = Tenant_User.objects.get(domain=domain)
            except Tenant_User.DoesNotExist:
                request.tenant = None
        else:
            request.tenant = None