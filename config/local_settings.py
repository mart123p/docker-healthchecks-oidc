# Start of OIDC
from .settings import INSTALLED_APPS as settings_ia
from .settings import AUTHENTICATION_BACKENDS as settings_ab
from .settings import ROOT_URLCONF as settings_ru

INSTALLED_APPS = list(settings_ia)
INSTALLED_APPS.insert(INSTALLED_APPS.index("django.contrib.auth")+1, "mozilla_django_oidc")
INSTALLED_APPS = tuple(INSTALLED_APPS)

AUTHENTICATION_BACKENDS = settings_ab + ("hc.accounts.ssochange.CustomOIDCAuthenticationBackend",)

ENABLE_OIDC = True
OIDC_RP_SCOPES = 'openid email profile'
OIDC_RP_CLIENT_ID = ""
OIDC_RP_CLIENT_SECRET = ""
OIDC_OP_AUTHORIZATION_ENDPOINT = "https://login.microsoftonline.com/TENANT-ID/oauth2/v2.0/authorize"
OIDC_OP_TOKEN_ENDPOINT = "https://login.microsoftonline.com/TENANT-ID/oauth2/v2.0/token"
OIDC_OP_USER_ENDPOINT = "https://graph.microsoft.com/oidc/userinfo"
OIDC_OP_JWKS_ENDPOINT = "https://login.microsoftonline.com/TENANT-ID/discovery/v2.0/keys"
OIDC_RP_SIGN_ALGO = "RS256"
LOGIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL_FAILURE = '/oidc/fail'

import sys
from django.urls import path,include
from django.views.generic.base import RedirectView
from types import ModuleType
from hc.accounts import ssoview

# Create a dynamic module that injects some additional routes before HC's
sys.modules['sneaky_url'] = ModuleType('sneaky_url')
class _Sneaky(ModuleType):
  @property
  def urlpatterns(self):
    return [
      path('oidc/fail', ssoview.fail),
      path('oidc/', include('mozilla_django_oidc.urls')),
      path('accounts/login/', RedirectView.as_view(url='/oidc/authenticate', permanent=True)),
      path('', include(settings_ru))
    ]
sys.modules['sneaky_url'].__class__ = _Sneaky
ROOT_URLCONF = 'sneaky_url'
# End of OIDC

# Inject of the middleware for project assignement
MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "mozilla_django_oidc.middleware.SessionRefresh",
    "hc.accounts.middleware.TeamAccessMiddleware",
    "hc.accounts.memberassignment.MemberAssignmentMiddleware"
)


# Default setting for Healthchecks.io
BASE_URL = "localhost"
EMAIL_PORT = "587"
EMAIL_HOST = "smtp.example.com"
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "user"
EMAIL_HOST_PASSWORD = "password"

SITE_ROOT = "http://localhost:8000"
SITE_NAME = "Example Healthchecks"

DEBUG = False
DEFAULT_FROM_EMAIL = "alert@example.com"

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ["*"]

PING_ENDPOINT = SITE_ROOT + "/ping/"
