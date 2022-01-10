"""
Django settings for LmsWeb project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c85-k0x$o1f=-m=a018tv)vljkmn^e=yx05@ch#&r+*b9g0z03'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['47.100.254.234']
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lms.apps.LmsConfig',
    # 'smart_chart.echart'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # smart需注释
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LmsWeb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'LmsWeb.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': 'lms',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'Zhou@1010'
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# smartcharts 要求false
USE_TZ = True
#
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# simpleui 设置

# 首页配置
# SIMPLEUI_HOME_PAGE = 'https://www.baidu.com'
# 首页标题
# SIMPLEUI_HOME_TITLE = '百度一下你就知道'
# 首页图标,支持element-ui的图标和fontawesome的图标
# SIMPLEUI_HOME_ICON = 'el-icon-date'

# 设置simpleui 点击首页图标跳转的地址
# SIMPLEUI_INDEX = 'https://www.88cto.com'

# 首页显示服务器、python、django、simpleui相关信息
SIMPLEUI_HOME_INFO = False

# 首页显示快速操作
# SIMPLEUI_HOME_QUICK = False

# 首页显示最近动作
# SIMPLEUI_HOME_ACTION = False

# 自定义SIMPLEUI的Logo
# SIMPLEUI_LOGO = 'https://avatars2.githubusercontent.com/u/13655483?s=60&v=4'

# 登录页粒子动画，默认开启，False关闭
# SIMPLEUI_LOGIN_PARTICLES = False

# 让simpleui 不要收集相关信息
SIMPLEUI_ANALYSIS = True

# 自定义simpleui 菜单
SIMPLEUI_CONFIG = {
    # 在自定义菜单的基础上保留系统模块
    'system_keep': True,
    'menus': [

        #     {
        #     # 自2021.02.01+ 支持多级菜单，models 为子菜单名，理论上可以无限级
        #     'name': '多级菜单测试',
        #     'icon': 'fa fa-file',
        #     'models': [{
        #         'name': 'Baidu',
        #         'icon': 'far fa-surprise',
        #         'models': [
        #             {
        #                 'name': '爱奇艺',
        #                 'models': [
        #                     {'name': '视频直播'},
        #
        #                     {'name': 'TV直播',
        #                      'models': [
        #                          {'name': '视频直播'}
        #                      ]},
        #
        #                 ]
        #             }, {
        #                 'name': '百度问答'
        #             }
        #         ]
        #     }, {
        #         'name': 'Google',
        #         'icon': 'far fa-surprise',
        #         'models': [{
        #             'name': 'Youtube',
        #             'icon': 'far fa-surprise'
        #         }, {
        #             'name': 'Gmail',
        #             'icon': 'far fa-surprise'
        #         }, {
        #             'name': 'Search',
        #             'url': 'https://www.google.com'
        #         }]
        #     }]
        # },

        {
            'name': '可视化',
            'icon': 'fa fa-file',
            'models': [{
                'name': '总览',
                'url': 'chart1',
                'icon': 'far fa-surprise'
            }, {
                'name': '近一月',
                'url': 'chart2',
                'icon': 'fab fa-github'
            }, {
                'name': '预警页面',
                'url': 'predict',
                'icon': 'fab fa-github'
            }]
        }]
}

# 是否显示默认图标，默认=True
# SIMPLEUI_DEFAULT_ICON = False

# 图标设置，图标参考：
# SIMPLEUI_ICON = {
#     '系统管理': 'fab fa-apple',
#     '员工管理': 'fas fa-user-tie'
# }

# 指定simpleui 是否以脱机模式加载静态资源，为True的时候将默认从本地读取所有资源，即使没有联网一样可以。适合内网项目
# 不填该项或者为False的时候，默认从第三方的cdn获取

# SIMPLEUI_STATIC_OFFLINE = True
