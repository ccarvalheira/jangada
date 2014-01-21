"""
Django settings for meta project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import environ
root = environ.Path(__file__) -1
env = environ.Env(DEBUG=(bool, False),)
env.read_env(root('../.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'apps.core',
    'django_jinja',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_LOADERS = (
    'django_jinja.loaders.AppLoader',
    'django_jinja.loaders.FileSystemLoader',
)

TEMPLATE_DIRS = (
	root("../templates"),
)

ROOT_URLCONF = 'confs.urls'

WSGI_APPLICATION = 'confs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

if env("DATABASE_URL"):
	DATABASES = {
		'default': env.db('DATABASE_URL'),
	}
else:
	DATABASES = {
	    	'default': {
        		'ENGINE': 'django.db.backends.sqlite3',
	 	        'NAME': root('../../db.sqlite3'),
    		}
	}



# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = "pt-pt"

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = root('../../media')
DEV_MEDIA_ROOT = root('../dev_media')

MEDIA_URL = 'media/'

STATIC_ROOT = root('../../static')
STATIC_URL = '/static/'


print env("DATABASE_URL")
print STATIC_ROOT
print MEDIA_ROOT
print root()

