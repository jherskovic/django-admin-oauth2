from django.conf import settings as global_settings

defaults = {
    # default values for all django-oauth2-admin settings
    "GET_USER": 'oauthadmin.utils.default_get_user',
    "PING_INTERVAL": 300,
    "DEFAULT_NEXT_URL": "/admin/",
    "SCOPE": ["email"],
    "USER_PK_ATTRIBUTE": "email",
    "USER_FIRST_NAME_ATTRIBUTE": "given_name",
    "USER_LAST_NAME_ATTRIBUTE": "family_name",
    "USER_EMAIL_ATTRIBUTE": "email",
    "USER_ROLES_ATTRIBUTE": "role",
    "ADMIN_ROLE_NAME": "Django Administrator",
    "FIRST_AUTH_PARAMETERS": {},
}

global_prefix = 'OAUTHADMIN_'

def app_setting(name):
    return getattr(global_settings, global_prefix+name, defaults.get(name))
