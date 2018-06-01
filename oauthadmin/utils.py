from django.core.exceptions import ImproperlyConfigured
from importlib import import_module
from requests_oauthlib import OAuth2Session
from oauthadmin.settings import app_setting
import pprint

# Note: This is a copy-paste from django 1.6 for backwards-compat reasons

def import_by_path(dotted_path, error_prefix=''):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImproperlyConfigured if something goes wrong.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise ImproperlyConfigured("%s%s doesn't look like a module path" % (
            error_prefix, dotted_path))

    module = import_module(module_path)

    try:
        attr = getattr(module, class_name)
    except AttributeError:
        raise ImproperlyConfigured('%sModule "%s" does not define a "%s" attribute/class' % (
            error_prefix, module_path, class_name))
    return attr


def userinfo(token):
    oauth = OAuth2Session(app_setting('CLIENT_ID'), token=token)
    req=oauth.request('GET', app_setting('USERINFO'))

    return req.json()


def default_get_user(token):
    # This import needs to be deferred
    from django.contrib.auth.models import User
    ui = userinfo(token)
    pprint.pprint(ui)

    pk = ui[app_setting('USER_PK_ATTRIBUTE')]
    roles = ui[app_setting('USER_ROLES_ATTRIBUTE')]

    try:
        user = User.objects.get(username=pk)
    except User.DoesNotExist:
        user = User(username=pk)
        user.is_superuser = app_setting('ADMIN_ROLE_NAME') in roles
        user.is_staff = True
        user.email = ui[app_setting('USER_EMAIL_ATTRIBUTE')]
        user.first_name = ui[app_setting('USER_FIRST_NAME_ATTRIBUTE')]
        user.last_name = ui[app_setting('USER_LAST_NAME_ATTRIBUTE')]

        user.save()
    return user

