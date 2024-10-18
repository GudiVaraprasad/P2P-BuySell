# services/seller_service.py
import time
import random
from protocol.message import Message

class SellerService:
    def __init__(self, peer):
        self.peer = peer

    def handle_buy(self, buyer_id):
        if self.peer.items > 0:
            print(f"Seller {self.peer.peer_id} sold an item to Buyer {buyer_id}")
            self.peer.items -= 1
        else:
            print(f"Seller {self.peer.peer_id} has no items left")
