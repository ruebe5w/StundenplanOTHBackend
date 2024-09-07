"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

#from django.contrib.auth.handlers.modwsgi import check_password
#from django.core.handlers.wsgi import WSGIHandler
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
