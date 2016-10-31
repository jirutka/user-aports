from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
import django_auth_ldap.backend as ldap_backend
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


class LDAPBackend(ldap_backend.LDAPBackend):
    """
    Customized LDAPBackend that automatically sets user's email address
    obtained from LDAP as verified and primary address.
    """

    def __init__(self):
        super(LDAPBackend, self).__init__()
        # Register receiver of populate_user signal.
        ldap_backend.populate_user.connect(self._on_populate_user)

    @staticmethod
    def _on_populate_user(sender, user=None, ldap_user=None, **_kwargs):
        if user._state.adding:
            user.save()
        try:
            email = EmailAddress.objects.get(user=user, email=user.email)
            email.verified = True
            if not EmailAddress.objects.filter(user=user, primary=True).exists():
                email.primary = True
            email.save()
        except ObjectDoesNotExist as e:
            ldap_backend.logger.warning(u'EmailAddress %s does not exist' % user.email)
