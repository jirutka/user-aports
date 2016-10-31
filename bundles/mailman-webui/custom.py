from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import settings


class CloseableRegistrationAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return settings.get('REGISTRATION_OPEN', True)


class AuthenticationRequiredMiddleware(object):
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL.
    """

    def __init__(self):
        self.login_url = reverse(getattr(settings, 'LOGIN_URL', 'account_login'))

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated():
            return None

        if request.path_info == self.login_url:
            return None

        return login_required(view_func)(request, *view_args, **view_kwargs)
