"""
Django settings for felicity_threads_base project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import datetime
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

class UTC(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(0)
    def tzname(self, dt):
        return "UTC"
    def dst(self, dt):
        return datetime.timedelta(0)

utc = UTC()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%)&6@k)c5%9zicp4-5wyo(d!3x1mdbjo7kc(4x&k_7qa-qk$kp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
        '.felicity.iiit.ac.in',
        '.felicity.iiit.ac.in.',
        ]


# Application definition

INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'longerusername',
        'base',
        'djcelery',
        'gordian_knot',
        )

MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django_cas.middleware.CASMiddleware',
        'django.contrib.admindocs.middleware.XViewMiddleware',
        'base.middleware.RestrictAccessTillTime'
        )


AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend', 
        'base.backends.PopulatedCASBackend',
        )

ROOT_URLCONF = 'felicity_threads_base.urls'

WSGI_APPLICATION = 'felicity_threads_base.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '<db-name>',
            'USER' : '<user>',
            'PASSWORD' : '<password>',
            'HOST' : '<host>',
            }
        }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/contest/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')

MEDIA_URL = '/contest/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
TEMPLATE_DIRS = (TEMPLATE_PATH,)

# CAS settings

CAS_SERVER_URL = 'http://felicity.iiit.ac.in/cas/'
CAS_VERSION = '3'
CAS_LOGOUT_COMPLETLY = True
CAS_LOGOUT_URL = 'http://felicity.iiit.ac.in/logout'
CAS_DISPLAY_MESSAGES = False

LOGIN_URL = '/contest/accounts/login'
LOGOUT_URL = '/contest/accounts/logout'
LOGIN_REDIRECT_URL = '/'

#Add start and end datetime in the format year, month, day, hour, minute, second, milisecond, utc
CONTEST_START_DATETIME = datetime.datetime() 
CONTEST_END_DATETIME = datetime.datetime()

LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': '/tmp/django-debug.log',
                },
            },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'ERROR',
                'propagate': True,
                },
            },
        }

# Celery Specific Variables.
BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend'
~                                                                 
