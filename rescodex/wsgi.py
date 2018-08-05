"""
WSGI config for rescodex project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rescodex.settings")

"""
05/08/2018 -- correction partie 1
Mise en place d'un correctif pour palier à un bug de passenger. Passenger étant l'outil utilisé sur A2hosting pour
permettre à Apache d'utiliser un service Python.
Le but est de revaloriser la varible PATH_INFO qui n'est pas correctement valorisé lors d'appel de type POST
"""
SCRIPT_NAME = ''

class PassengerPathInfoFix(object):
    """
    Sets PATH_INFO from REQUEST_URI since Passenger doesn't provide it.
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        from urllib.parse import unquote
        environ['SCRIPT_NAME'] = SCRIPT_NAME

        request_uri = unquote(environ['REQUEST_URI'])
        script_name = unquote(environ.get('SCRIPT_NAME', ''))
        offset = request_uri.startswith(script_name) and len(environ['SCRIPT_NAME']) or 0
        environ['PATH_INFO'] = request_uri[offset:].split('?', 1)[0]
        return self.app(environ, start_response)
"""
fin correction partie 1
"""

application = get_wsgi_application()

#Correction partie 2
application = PassengerPathInfoFix(application)
#Fin correction partie 2