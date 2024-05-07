"""
WSGI config for majorinBE project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

from dotenv import load_dotenv
import os 

from django.core.wsgi import get_wsgi_application

ENV_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(ENV_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'majorinBE.settings')

application = get_wsgi_application()


