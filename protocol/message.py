# protocol/message.py
import json
import socket
from services.seller_service import SellerService
class Message:
    @staticmethod
    def lookup(buyer_id, product_name, hop_count):
        return {
            "type": "lookup",
            "buyer_id": buyer_id,
            "product": product_name,
            "hop_count": hop_count
        }

    @staticmethod
    def reply(seller_id, buyer_id, product_name):
        return {
            "type": "reply",
            "seller_id": seller_id,
            "buyer_id": buyer_id,
            "product": product_name
        }

    @staticmethod
    def buy(buyer_id, seller_id):
        return {
            "type": "buy",
            "buyer_id": buyer_id,
            "seller_id": seller_id
        }