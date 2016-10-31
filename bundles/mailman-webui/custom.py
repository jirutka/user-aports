from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from django.core.exceptions import ObjectDoesNotExist
import django_auth_ldap.backend as ldap_backend
import settings


class CloseableRegistrationAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return settings.get('REGISTRATION_OPEN', True)


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
