import json
import logging, traceback
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from .models_mongo import Room, Message

logger = logging.getLogger("communications")

class TestConsumer(AsyncWebsocketConsumer):
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

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if not user.is_authenticated:
            return await self.close()
        
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_name = f"room_{self.room_id}"
        
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        print(f"WebSocket disconnected with code: {code}")

    async def receive(self, text_data, bytes_data=None):
        try:
            user = self.scope["user"]
            payload = json.loads(text_data or "{}")
            text = payload.get("text", "").strip()
            if not text:
                return
            
            user_pk = user.pk
            
            room = Room.objects(room_id=self.room_id).first()

            if room is None:
                room = Room(room_id=self.room_id, participants=[user_pk])
            else:
                if user_pk not in room.participants:
                    room.participants.append(user_pk)
                    room.updated_at = timezone.now()
            
            room.save() 

            Message(
                room=room,
                sender_id=user_pk,
                text=text,
                timestamp=timezone.now()
            ).save()

            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "chat.message", 
                    "user": user.user_name, 
                    "text": text
                }
            )
        except Exception as e:
            logging.error(f"Error in ChatConsumer.receive: {e} \n{traceback.format_exc()}")
            await self.close()
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "user": event["user"],
            "text": event["text"]
        }))