from .base import *
SECRET_KEY='&kzg)(b_xt1*nyp-s97ibt01b7p+67#&-brmb_nqj&dn_%q6tc'
#Note: For security purposes, Django’s DEBUG output will never display 
# any settings that may contain the strings: API, KEY, PASS, SECRET, 
# SIGNATURE, or TOKEN.
DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }
    },
]