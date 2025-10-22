import json
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from django.utils.timezone import now

from apps.audit.models import AuditLog


SENSITIVE_KEYS = {"password", "password1", "password2", "token", "secret", "csrfmiddlewaretoken"}


class AdminAuditMiddleware(MiddlewareMixin):
    """
    Logs admin panel write operations (POST/PUT/PATCH/DELETE).
    Stores actor, action, target model/object, path, IP, user agent, and POST data (sanitized).
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Only audit admin backend writes
        if not request.path.startswith('/admin'):
            return None
        if request.method not in ("POST", "PUT", "PATCH", "DELETE"):
            return None

        # Build changes dict from POST
        data = {}
        if getattr(request, 'POST', None):
            for k, v in request.POST.items():
                if k in SENSITIVE_KEYS:
                    data[k] = "***"
                else:
                    data[k] = v

        # Try to resolve model from admin URL (best-effort)
        model = ''
        object_id = ''
        try:
            match = resolve(request.path)
            # admin:app_model_change -> extract app, model
            if match and match.url_name:
                url_name = match.url_name or ''
                if '_' in url_name:
                    parts = url_name.split('_')
                    if len(parts) >= 3 and parts[0] == 'app' and parts[2] in ('add', 'change', 'delete', 'changelist'):
                        # newer admin URL names look like: admin:app_model_change
                        pass
                # admin resolves provide app/model as kwargs sometimes
                app_label = match.kwargs.get('app_label') if match.kwargs else None
                model_name = match.kwargs.get('model_name') if match.kwargs else None
                if app_label and model_name:
                    model = f"{app_label}.{model_name}"
                obj_id = match.kwargs.get('object_id') if match.kwargs else None
                if obj_id:
                    object_id = str(obj_id)
        except Exception:
            pass

        ip = request.META.get('REMOTE_ADDR')
        ua = request.META.get('HTTP_USER_AGENT', '')
        actor = getattr(request, 'user', None)

        action = f"{request.method} {request.path}"
        AuditLog.objects.create(
            actor=actor if getattr(actor, 'is_authenticated', False) else None,
            action=action,
            model=model,
            object_id=object_id,
            path=request.path,
            method=request.method,
            ip_address=ip,
            user_agent=ua,
            changes=data,
            created_at=now(),
        )
        return None
