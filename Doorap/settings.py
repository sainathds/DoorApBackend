"""
Django settings for Doorap project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

print(BASE_DIR)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^f6f3ws77!6qzs%qshz)7rkrkauwlfzr_^!^6#^78e&ol^-ccw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
        'django_crontab',
		'Doorap_App',
		'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Doorap.urls'

AUTH_USER_MODEL = 'Doorap_App.MyUser'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Doorap.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
			'default': {
					'ENGINE': 'django.db.backends.mysql',
					'NAME': 'Doorap_DB',
					'USER': 'root',
					'PORT': '3306',
					'PASSWORD':'Root1234',
					'HOST': 'doorap.chbcgxahrtcf.us-east-1.rds.amazonaws.com',
					'OPTIONS': {
							'charset': 'utf8mb4',
							'use_unicode': True,
					}
			
			}
} 


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'


USE_I18N = True

USE_TZ = True

# TIME_ZONE = 'Asia/Kolkata'
# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'Asia/Kolkata'

# USE_I18N = True

# USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (os.path.join(BASE_DIR,"static"),)

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # for collect static

print("---------",STATICFILES_DIRS)

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

print(PROJECT_ROOT)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AWS_ACCESS_KEY_ID = 'AKIA5JXESFTJCPNJMEVX'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'doorap-s3-bucket'
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_FILE_OVERWRITE = False

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
# DEFAULT_FILE_STORAGE = 'hello_django.storage_backends.Publi



############### jwt settings ###################

SIMPLE_JWT = {
'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
'REFRESH_TOKEN_LIFETIME': timedelta(days=60),
}


#### Disabling Browsable Api ####

REST_FRAMEWORK = {
	'DEFAULT_RENDERER_CLASSES':('rest_framework.renderers.JSONRenderer',)
}


#Send Mail Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'noreplydoorap@gmail.com'
EMAIL_HOST_PASSWORD = 'ifkyamuzkafnhxfp' 
EMAIL_PORT = 587 
EMAIL_USE_TLS = True



###### FCM Server Key ######

API_KEY_NOTIFICATION = "AAAAkmWW0vg:APA91bGcSLvDBl1IpdJ98UJ8aj7bE_kj2kclBvHs6pSpbHeIH9-SkXVMtJ6Nh5wENUmDOaKIBW-gvSqRdj8p7mCdLqI8vfIO9RfucKeUKBM-Xx6IXLWvisBBSLwOP6bgFmXLK9WNOL7y"

# API_KEY_NOTIFICATION = "AAAADSVQKAk:APA91bGEXzqX16ZPptV0FLkSsTvLcC5wq6GLguU31Ii8YQnvpiTpatf_t2lacj8yH35o2cxFsdipPWqXK5FAqId_iGww71DNyKHY9b45GnvNw4hyzbJw5CQSc9rSHIsmLF-VAgs-mlTu"





# cron setting for subscription expiry
CRONJOBS = [
    ('01 00 * * *', 'Doorap_App.cron.Update_Status'), # fire cron in every day 12:01 AM.
    ('59 23 * * *', 'Doorap_App.cron.Update_Status'), # fire cron in every day 23:50 PM
     
]