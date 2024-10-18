# services/seller_service.py
from protocol.message import Message
from utils.logger import Logger
import threading

class SellerService:
    def __init__(self, peer):
        self.peer = peer
        self.inventory = {"fish": 5, "salt": 5, "boars": 5}
        self.lock = threading.Lock()

    def handle_buy_request(self, product_name, buyer_id):
        with self.lock:
            if self.inventory.get(product_name, 0) > 0:
                print(f"Seller {self.peer.peer_id} selling {product_name} to buyer {buyer_id}")
                self.inventory[product_name] -= 1
                Logger.log_event("buy", self.peer.peer_id, f"Sold {product_name} to {buyer_id}")
                return True
            else:
                Logger.log_event("stock_empty", self.peer.peer_id, f"No {product_name} in stock")
                return False
