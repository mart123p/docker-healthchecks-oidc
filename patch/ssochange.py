from django.shortcuts import render
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from hc.accounts.models import Profile

def fail(request):
    return render(request, "try_later.html")

class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def get_or_create_user(self, access_token, id_token, payload):
        self.ms_upn = payload["upn"]
        return super(CustomOIDCAuthenticationBackend, self).get_or_create_user(access_token, id_token, payload)

    def verify_claims(self, claims):
        print(claims)
        return True

    def filter_users_by_claims(self, claims):
        """Return all users matching the specified email."""
        username = claims.get('sub')
        if not username:
            return self.UserModel.objects.none()
        return self.UserModel.objects.filter(username__iexact=username)    
    
    def create_user(self, claims):
        username = claims.get('sub')
        email = claims.get('email')
        if not email:
            email = self.ms_upn
        user = self.UserModel.objects.create_user(username, email)
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user

    def update_user(self, user, claims):
        email = claims.get('email')
        if not email:
            email = self.ms_upn

        user.email = email
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user
