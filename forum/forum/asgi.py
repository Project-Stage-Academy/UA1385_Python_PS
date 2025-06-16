"""
ASGI config for forum project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/

# ASGI application supporting both HTTP and WebSocket protocols via Channels
==================================

Protocols:

 - http : default Django stack, connected via get_asgi_application
 - ws : WebSocket real-time stack, using URLRouter(websocket_urlpatterns) and AuthMiddlewareStack 
    so every WebSocket user (Consumer) will be authorized 

==================================

try/except imports: secure check so if it fails the import falls back to an empty list
    and the app continues to work only with http protocol

==================================

'DJANGO_SETTINGS_MODULE' : set by default with 'forum.settings'

==================================

ProtocolTypeRouter : gives us single ASGI entry-point for several protocols 
    so there is no need to create different ASGI apps for different protocols

==================================

URLRouter : works as "urls.py" for websockets

==================================
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forum.settings")

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from communications.middleware import JwtAuthMiddleware
try:
    from forum.routing import websocket_urlpatterns
except ImportError:
    websocket_urlpatterns = []


application = ProtocolTypeRouter({

    "http": get_asgi_application(),

    "websocket": JwtAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),

})
