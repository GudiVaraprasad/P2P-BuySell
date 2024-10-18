# services/buyer_service.py
import time
import random
from protocol.message import Message

class BuyerService:
    def __init__(self, peer):
        self.peer = peer

    def start_buying(self):
        while self.peer.running:
            time.sleep(random.randint(5, 10))
            product = random.choice(['fish', 'salt', 'boars'])
            print(f"Buyer {self.peer.peer_id} is looking for {product}")
            # Send lookup message to neighbors
            lookup_message = Message.lookup(self.peer.peer_id, product, hop_count=3)
            self.peer.message_handler.propagate(lookup_message)
