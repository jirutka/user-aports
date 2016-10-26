from allauth.account.adapter import DefaultAccountAdapter
import settings


class CloseableRegistrationAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return settings.get('REGISTRATION_OPEN', True)
