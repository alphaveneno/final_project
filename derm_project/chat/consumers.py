"""
consumers for chat room
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    """
    chat consumer
    """

    async def connect(self):
        """
        connect to chat room via socket
        """
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        """
        disconnect will close the socket
        """
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Receive message from WebSocket
        """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # message passed to room group,
        # author's username is added here: self.scope["user"].username
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "username": self.scope["user"].username,
                "message": message,
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        """
        ultimately sends message to
        the textarea element in room.html,
        for rendering
        """
        message = event["message"]
        # Send message to WebSocket, include author's name before the message
        await self.send(
            text_data=json.dumps({"username": event["username"], "message": message})
        )
