from .settings import *

DEBUG = False

ADMINS = (
    ('José Neto', 'jbsneto@intmed.com'),
)

HOST_NAME = 'https://medicar.intmed.com'

# CORS HOSTS
CORS_ALLOWED_ORIGINS = [
    'https://*.intmed.com',
    'https://*.ngrok.io',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'medicar',
        'USER': 'medicar',
        'PASSWORD': 'xxxxxxx',
        'HOST': '',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
            'charset': 'utf8mb4',
        }
    }
}

# Editar configurações de acordo com a necessidade
# https://pypi.org/project/djangorestframework-simplejwt/
SIMPLE_JWT = {
    'ALGORITHM': 'RS256',
    'VERIFYING_KEY': 'ssh-rsa XXXXXX',

    'AUTH_HEADER_TYPES': ('Token',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}
