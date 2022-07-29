from .base import *
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = False

ALLOWED_HOSTS = ['192.168.20.30']

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('SQL_DATABASE', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.environ.get('SQL_USER', 'user'),
        'PASSWORD': os.environ.get('SQL_PASSWORD', 'password'),
        'HOST': os.environ.get('SQL_HOST', 'localhost'),
        'PORT': os.environ.get('SQL_PORT', ''),
    }
}
"""
|If you’ve enabled all the recommended security components and re-implemented settings as directed, your project has these key features:
|
|SSL/HTTPS for all communications (for example, subdomains, cookies, CSRF).
|XSS (cross-site scripting) attacks prevention.
|CSRF (cross-site request forgery) attacks prevention.
|Concealed project secret key.
|Concealed admin login URL preventing brute-force attacks.
|Separate settings for development and production.
"""
########################Security########################
SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True

################HTTPS
SECURE_HSTS_SECONDS=3600 #31536000 1 hour
 
SECURE_HSTS_INCLUDE_SUBDOMAINS=True

SECURE_HSTS_PRELOAD=True