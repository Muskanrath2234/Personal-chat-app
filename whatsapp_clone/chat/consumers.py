import json
from channels.generic.websocket import AsyncWebsocketConsumer

from channels.db import database_sync_to_async

class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.my_id = self.scope['user'].id
        self.other_user_id = self.scope['url_route']['kwargs']['id']
        if int(self.my_id) > int(self.other_user_id):
            self.room_name = f'{self.my_id}-{self.other_user_id}'
        else:
            self.room_name = f'{self.other_user_id}-{self.my_id}'

        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        # Save message to the database
      

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

   