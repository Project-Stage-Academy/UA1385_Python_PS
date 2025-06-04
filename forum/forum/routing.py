from django.urls import path
from channels.generic.websocket import AsyncWebsocketConsumer


class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data="Websocket connected.")

    async def receive(self, text_data):
        await self.send(text_data=f"You sent: {text_data}")

    async def disconnect(self, code):
        pass

websocket_urlpatterns =[
    path("ws/test/", Consumer.as_asgi()),
]



    