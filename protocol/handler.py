# protocol/handler.py
import json

class MessageHandler:
    def __init__(self, peer):
        self.peer = peer

    def handle_message(self, conn):
        # Receive and decode the incoming message
        data = conn.recv(1024).decode()
        message = json.loads(data)
        print(f"Peer {self.peer.peer_id} received message: {message}")
        
        # Handle different message types
        if message['type'] == 'lookup':
            self.handle_lookup(message)
        elif message['type'] == 'reply':
            self.handle_reply(message)
        elif message['type'] == 'buy':
            self.handle_buy(message)

    def handle_lookup(self, message):
        print(f"Peer {self.peer.peer_id} handling lookup: {message}")
        # Handle lookup logic (e.g., if seller has product)

    def handle_reply(self, message):
        print(f"Peer {self.peer.peer_id} handling reply: {message}")
        # Handle reply logic (e.g., if buyer receives reply)

    def handle_buy(self, message):
        print(f"Peer {self.peer.peer_id} handling buy: {message}")
        # Handle buy logic (e.g., seller reduces stock)
