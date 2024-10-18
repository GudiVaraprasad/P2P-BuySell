# protocol/handler.py
import json
from protocol.message import Message

class MessageHandler:
    def __init__(self, peer):
        self.peer = peer

    def handle_message(self, conn):
        data = conn.recv(1024)
        message = json.loads(data.decode())
        
        if message['type'] == 'lookup':
            self.handle_lookup(message)
        elif message['type'] == 'reply':
            self.handle_reply(message)
        elif message['type'] == 'buy':
            self.handle_buy(message)

    def handle_lookup(self, message):
        if self.peer.role == "seller" and self.peer.product_name == message['product_name']:
            reply = Message.reply(self.peer.peer_id, message['buyer_id'], message['product_name'], message['path'])
            self.send_message(reply, message['buyer_id'])

        elif message['hop_count'] > 0:
            message['hop_count'] -= 1
            message['path'].append(self.peer.peer_id)
            self.propagate(message)

    def propagate(self, message):
        for neighbor in self.peer.neighbors:
            self.send_message(message, neighbor)

    def send_message(self, message, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(('localhost', port))
            sock.send(json.dumps(message).encode())
