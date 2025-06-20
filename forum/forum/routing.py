from django.urls import path, re_path
from communications.consumers import ChatConsumer, TestConsumer

websocket_urlpatterns =[
    path("ws/test/", TestConsumer.as_asgi(), name="ws-test"),
    path("ws/chat/<str:room_id>/", ChatConsumer.as_asgi(), name="ws-chat"),
]



    