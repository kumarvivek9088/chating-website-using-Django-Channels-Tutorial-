# Channels and ASGI splitup incoming connection into two components - scope,events
# scope- (similiar to django's request), is a set of details about a single incoming connecton such as the path a web request was made from ,Ip address of a websocket, user
# events - handle connect, disconnect, recieve message events
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
class Chating(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,self.channel_name
        )
        self.accept()
    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,self.channel_name
        )
    
    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        msg = data["message"]
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,{"type":"chat_messages","messages":msg ,"user": str(self.scope['user'])}
        )
    def chat_messages(self,event):
        msg = event["messages"]
        self.send(text_data=json.dumps({"message": msg,"user":event["user"]}))
