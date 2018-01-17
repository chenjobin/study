"""
Django settings for study project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import socket   #关闭DEBUG引入
#导入模块 日志配置
import logging
import django.utils.log
import logging.handlers

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dcs^-wyqx)h9iw7hig_+-vvy07k48k(e)u759p!xqvi9fy+p72'

# SECURITY WARNING: don't run with debug turned on in production!

# 服务器端修改debug为False
DEBUG = TEMPLATE_DEBUG = True
# DEBUG = TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['chenzhibin.vip','www.chenzhibin.vip','127.0.0.1','localhost']
#DEBUG动态开启

# Application definition

INSTALLED_APPS = [
    'courses',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bootstrap3',
    'DjangoUeditor',
    'django_comments',
    'django.contrib.sites',

    'blog',
    'users',
    'subject',
    'exam',
    'shop',
    'cart',
    'orders',
]

SITE_ID = 1 #django-contrib-comments模块引入

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'study.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',    # 把购物车添加进请求上下文中
            ],
        },
    },
]

WSGI_APPLICATION = 'study.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

#我的设置
LOGIN_URL='/users/login/'

#django-bootstrap3的设置
BOOTSTRAP3={
    'include_jquery':True,
}

#DjangoUeditor额外引入-------------------------------------------------
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# 公共的 static 文件，比如 jquery.js 可以放这里，这里面的文件夹不能包含 STATIC_ROOT
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static_common"),
)

# upload folder
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#DjangoUeditor额外引入-------------------------------------------------

#这个日志配置，主要分为4个部分，formater(格式器)、handle(处理器)、filter(过滤器)、logger(日志管理器实例)，
# 在handles和filters分别设置处理器和过滤器是给loggers使用的，都可以设置多个。
# 至于可以在views里面调用什么就暂时不用管了。设置写到文件中要注意写好路径。我是如下配置的：
# 把所有的debug信息输出到控制台，把error级别错误信息输出到文件。当然要先在django网站创建我设置的日志目录：log，要不然会出错。

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {#日志格式
       'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}
    },
    'filters': {#过滤器
    },
    'handlers': {#处理器
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'debug': {#输出到文件
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "log",'debug.log'),#日志输出文件
            'maxBytes':1024*1024*5,#文件大小
            'backupCount': 5,#备份份数
            'formatter':'standard',#使用哪种formatters日志格式
        },
        'console':{#输出到控制台
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    'loggers': {#logging管理器
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['debug','mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        # 对于不在 ALLOWED_HOSTS 中的请求不发送报错邮件
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    }
}
#邮箱部分
ADMINS = (
    ('zhibin chen','923869955@qq.com'),#设置管理员邮箱
)

#Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST= 'smtp.qq.com'#QQ邮箱SMTP服务器
EMAIL_PORT= 587		 #QQ邮箱SMTP服务端口
EMAIL_HOST_USER = '923869988@qq.com'  #我的邮箱帐号
EMAIL_HOST_PASSWORD = 'tekgzsgjnijwbcjj' #密码
EMAIL_SUBJECT_PREFIX = 'chenzhibin.vip' #为邮件标题的前缀,默认是'[django]'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = SERVER_EMAIL = EMAIL_HOST_USER
#日志配置- 包括邮箱---实现邮箱发送错误日志---------------------------------------------------

# shop模型添加购物车
CART_SESSION_ID = 'cart'
