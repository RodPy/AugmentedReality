"""
Django settings for AugmentedReality project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, socket
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_DIR = os.path.join(BASE_DIR, 'AugmentedReality')

def cast_type(str_value):
    if str_value == "False":
        return False
    elif str_value == "True":
        return True
    elif type(str_value) == str:
        return str_value
    elif int(str_value) == int:
        return int(str_value)
    elif str_value[0:2] == "[]":
        return []
    return None

def cast_type_by_list(t_list):
    new_list = []
    for i in t_list:
        new_list.append(cast_type(i))
    return new_list
            
def get_config(file_path):
    dic = {}
    if os.path.isfile(file_path):
        file = open(file_path, 'r')
        lines = file.read().splitlines();
        for line in lines:
            dictionary_file_line = line.split('=')
            if "," in dictionary_file_line[1]: # the value will be a list
                VALUES_LIST = dictionary_file_line[1].split(';')
                final_value_list = []
                for item in VALUES_LIST:
                    temp_list = cast_type_by_list(item.split(','))
                    final_value_list.append(temp_list)
                dic[dictionary_file_line[0]] = final_value_list
            else: # there isn't list in the value side
                dic[dictionary_file_line[0]] = cast_type(dictionary_file_line[1])
    return dic

my_config = get_config(os.path.join(ROOT_DIR,'my-config'))


# Staticfiles directory
STATICFILES_DIRS = (os.path.join(ROOT_DIR, 'STATIC').replace('\\','/'),
                 )


# Templates directory
TEMPLATE_DIRS = (
    os.path.join(STATICFILES_DIRS[0], 'frontend','app').replace('\\','/'),
)


ADMINS = my_config.get("ADMINS",((),))
MANAGERS = my_config.get("MANAGERS",((),))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = my_config["SECRET_KEY"]

DEBUG = my_config.get("DEBUG_GENERAL_STAGE",False)

TEMPLATE_DEBUG = my_config.get("TEMPLATE_DEBUD_GENERAL_STATE",False)

ALLOWED_HOSTS = my_config.get("ALLOWED_HOSTS",[])

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'presentation',
)

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
         'rest_framework.permissions.IsAdminUser'
    ),
    'PAGINATE_BY': 10,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',

        # Required by `allauth` template tags
    "django.core.context_processors.request",
    # `allauth` specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

ROOT_URLCONF = 'AugmentedReality.urls'

WSGI_APPLICATION = 'AugmentedReality.wsgi.application'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

if (socket.gethostname() == my_config.get("HOST_NAME","")):
    DATABASES = {
        'default': {
            'ENGINE': my_config.get('HOST_ENGINE_DATABASE','mysql.connector.django'),
            'NAME': my_config["HOST_DATABASE_NAME"],
            'USER': my_config["HOST_DATABASE_USER"],
            'PASSWORD': my_config["HOST_DATABASE_PASSWORD"],
            'HOST': my_config.get("HOST_DATABASE_HOST",""),
            'PORT': my_config.get("HOST_DATABASE_PORT","")
        }
    }
    DEBUG = TEMPLATE_DEBUG = my_config.get("HOST_DEBUG_TEMPLATE_DEBUG_STATE",False)
     
    STATIC_ROOT = os.path.join(STATICFILES_DIRS[0],'frontend', 'app').replace("\\",'/')
    
    MEDIA_ROOT = os.path.join(STATICFILES_DIRS[0], 'media').replace('\\','/')
    
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': my_config.get("MEMCACHEDCACHE_LOCATION","127.0.0.1:11211"),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True