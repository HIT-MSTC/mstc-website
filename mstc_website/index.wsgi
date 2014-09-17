import sae

from mstc_website import wsgi

application = sae.create_wsgi_app(wsgi.application)