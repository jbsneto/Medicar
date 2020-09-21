from .settings import *

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

HOST_NAME = MEET_HOST_NAME = 'http://127.0.0.1:8000'
INTERNAL_IPS = ['127.0.0.1', ]
ALLOWED_HOSTS = ['*', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

'''DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'medicar',
       'USER': xxxx,
       'PASSWORD': xxxx,
   }
}'''

