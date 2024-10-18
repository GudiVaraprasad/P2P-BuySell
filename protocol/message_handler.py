# protocol/message_handler.py
import json
import socket
from services.seller_service import SellerService

class MessageHandler:
    def __init__(self, peer):
        self.peer = peer

    def handle(self, conn):
        data = conn.recv(1024)
        message = json.loads(data.decode())
        
        if message['type'] == 'lookup':
            self.handle_lookup(message)
        elif message['type'] == 'reply':
            self.handle_reply(message)
        elif message['type'] == 'buy':
            self.handle_buy(message)

    def handle_lookup(self, message):
        # Seller responds if they have the requested product
        if self.peer.role == "seller":
            reply = Message.reply(self.peer.peer_id, message['buyer_id'], message['product'])
            self.send_message(reply, message['buyer_id'])

    def handle_reply(self, message):
        if self.peer.role == "buyer":
            print(f"Buyer {self.peer.peer_id} received a reply from Seller {message['seller_id']}")

    def handle_buy(self, message):
        if self.peer.role == "seller":
            seller_service = SellerService(self.peer)
            seller_service.handle_buy(message['buyer_id'])

    def propagate(self, message):
        # Send the message to all neighbors
        for neighbor in self.peer.neighbors:
            self.send_message(message, neighbor[1])

    def send_message(self, message, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('localhost', port))
                sock.send(json.dumps(message).encode())
        except Exception as e:
            print(f"Error sending message to {port}: {e}")
