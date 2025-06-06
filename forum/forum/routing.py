from django.urls import path
from channels.generic.websocket import AsyncWebsocketConsumer


class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_authenticated:
            await self.accept()
            await self.send(text_data="WebSocket connected.")
        else:
            await self.close()

    async def receive(self, text_data):
        await self.send(text_data=f"You sent: {text_data}")

    async def disconnect(self, code):
        print(f"WebSocket disconnected with code: {code}")

websocket_urlpatterns =[
    path("ws/test/", Consumer.as_asgi()),
]



    