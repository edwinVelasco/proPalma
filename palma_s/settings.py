"""
Django settings for palma_s project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i)#%-d-&e#p%jnvv5oqc@lh=v-73o#64rx(hzzff@ch#_6sf0s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'noreplypropalma@gmail.com'
EMAIL_HOST_PASSWORD = 'propalma2015'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'palma',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'palma_s.urls'

WSGI_APPLICATION = 'palma_s.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ufps_85',
        'USER': 'ufps_85',
        'PASSWORD': 'ufps_11',
        'HOST': 'sandbox2.ufps.edu.co',
    }
}
'''

    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'edwinvelasco_palma_s',
        'USER': '94403_edwin',
        'PASSWORD': 'Edwin1004',
        'HOST': 'mysql-edwinvelasco.alwaysdata.net',
    }

    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'propalma$palma_s',
        'USER': 'propalma',
        'PASSWORD': 'Edwin1004',
        'HOST': 'mysql.server',
    }


    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ufps_85',
        'USER': 'ufps_85',
        'PASSWORD': 'ufps_11',
        'HOST': 'sandbox2.ufps.edu.co',
    }

    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
    }

    '''
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-Co'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'static'),
)

STATIC_ROOT = '/static/'

'''
STATIC_ROOT = '/palma_s/public/static/'
STATIC_URL = '/static/' if DEBUG else 'http://your.website.url/static/'
'''

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

DATETIME_INPUT_FORMATS = (
    '%Y/%m/%d %H:%M:%S',
)