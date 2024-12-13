import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from home.models import Chat,User , Channel
# from django.core.exceptions import ObjectDoesNotExist
class ChatConsumer(AsyncWebsocketConsumer):
    """
    A consumer does three things:
    1. Accepts connections.
    2. Receives messages from client.
    3. Disconnects when the job is done.
    """

    async def connect(self):
        """
        Connect to a room
        """
        # Connect only if the user is authenticated
        user = self.scope['user']

        if user.is_authenticated:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            # Make sure to use a valid group name
            self.room_group_name = f"chat_{self.room_name.replace(' ', '_')}"
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        """
        Disconnect from channel
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive messages from WebSocket
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        room = text_data_json['room']
        profile_pic = text_data_json.get('profile_pic', None)  # Ensure it handles the profile pic if provided

        # Save message to DB
        await self.save_message(message, username, room, profile_pic)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room': room,
                'profile_pic': profile_pic,  # Include profile pic in the event
            }
        )

    async def chat_message(self, event):
        """
        Receive messages from room group
        """
        message = event['message']
        username = event['username']
        room = event['room']
        profile_pic = event.get('profile_pic', None)  # Get profile_pic if available

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room': room,
            'profile_pic': profile_pic,  # Send profile pic to the client
        }))

    @sync_to_async
    def save_message(self, message, username, room, profile_pic):
        """
        Save message to the database, ensuring that the user is a User instance and
        the room is a valid Channel instance.
        """
        from django.core.exceptions import ObjectDoesNotExist

        try:
            # Fetch the User instance using the username
            user_instance = User.objects.get(username=username)
            print(f"USER:+{user_instance}" )
        except ObjectDoesNotExist:
            print(f"User with username {username} does not exist.")
            return  # Optionally handle the missing user error

        try:
            # Fetch the Channel instance using the room name
            channel_instance = Channel.objects.get(channel_name=room)
            print(f"CHANNEL:+{channel_instance}")
        except Channel.DoesNotExist:
            print(f"Channel with name {room} does not exist.")
            return  # Optionally handle the missing channel error

        # Create the chat object with the User and Channel instances
        Chat.objects.create(
            chats=message, 
            user=user_instance,  # Ensure that the user field gets the User instance
            channel=channel_instance,  # Use the Channel instance
            
        )
