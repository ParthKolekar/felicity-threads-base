from django_cas.backends import CASBackend
from base.models import User as Profile

class PopulatedCASBackend(CASBackend):
    """
        CAS authentication backend with user data populated from AD
    """

    def __init__(self):
        super(PopulatedCASBackend, self).__init__()

    def authenticate(self, ticket, service, request):
        """
            Authenticates CAS ticket and retrieves user data
        """

        user = super(PopulatedCASBackend, self).authenticate(ticket, service, request)
        attributes = request.session['attr'] or None
        request.session['attr'] = None
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        profile, created = Profile.objects.get_or_create(user_username=user.username)

        if created is not None and attributes is not None:
            profile.user_email = attributes['mail']
            profile.user_nick = attributes['displayName']

        profile.user_last_ip = ip_address
        profile.save()
        return user
