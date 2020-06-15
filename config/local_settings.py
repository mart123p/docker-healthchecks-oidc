import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType


# Baseline configuration.
AUTH_LDAP_SERVER_URI = 'ldap://openldap'

AUTH_LDAP_BIND_DN = 'cn=admin,dc=example,dc=com'
AUTH_LDAP_BIND_PASSWORD = 'admin'
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    'ou=testusers,dc=example,dc=com',
    ldap.SCOPE_SUBTREE,
    '(mail=%(user)s)',
)

# Set up the basic group parameters.
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    'ou=testgroups,dc=example,dc=com',
    ldap.SCOPE_SUBTREE,
    '(objectClass=groupOfNames)',
)
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr='cn')

# Simple group restrictions
AUTH_LDAP_REQUIRE_GROUP = 'cn=executive,ou=testgroups,dc=example,dc=com'

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail',
}

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    'is_staff': 'cn=executive,ou=testgroups,dc=example,dc=com',
    'is_superuser': 'cn=executive,ou=testgroups,dc=example,dc=com',
}

# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Use LDAP group membership to calculate group permissions.
AUTH_LDAP_FIND_GROUP_PERMS = True

# Cache distinguised names and group memberships for an hour to minimize
# LDAP traffic.
AUTH_LDAP_CACHE_TIMEOUT = 3600

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "hc.accounts.middleware.TeamAccessMiddleware",
    "hc.accounts.memberassignment.MemberAssignmentMiddleware"
)

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

ALLOWED_HOSTS = ["localhost"]
CSRF_TRUSTED_ORIGINS = ["localhost"]

PING_ENDPOINT = SITE_ROOT + "/ping/"
