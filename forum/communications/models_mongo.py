from django.utils import timezone
import mongoengine as me
from django.contrib.auth import get_user_model

User = get_user_model()

class Room(me.Document):
    meta = {
        "db_alias": "chat",
        "collection": "rooms",
        "indexes": ["participants", "updated_at"]
    }
    room_id = me.StringField(primary_key=True, required=True)
    participants = me.ListField(me.IntField(), default=list, required=True)
    created_at = me.DateTimeField(required=True, default=timezone.now)
    updated_at = me.DateTimeField(required=True, default=timezone.now)

class Message(me.Document):
    meta = {
        "db_alias": "chat",
        "collection": "messages",
        "indexes": [
            {"fields": ["room", "timestamp"]},
        ]
    }
    room = me.ReferenceField(Room, required=True, reverse_delete_rule=me.CASCADE)
    sender_id = me.IntField(required=True)
    text = me.StringField(required=True)
    timestamp = me.DateTimeField(required=True, default=timezone.now)
    