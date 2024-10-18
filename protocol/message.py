# protocol/message.py
class Message:
    @staticmethod
    def lookup(buyer_id, product_name, hop_count):
        return {
            "type": "lookup",
            "buyer_id": buyer_id,
            "product_name": product_name,
            "hop_count": hop_count,
            "path": []
        }

    @staticmethod
    def reply(seller_id, buyer_id, product_name, path):
        return {
            "type": "reply",
            "seller_id": seller_id,
            "buyer_id": buyer_id,
            "product_name": product_name,
            "path": path
        }

    @staticmethod
    def buy(buyer_id, seller_id, product_name):
        return {
            "type": "buy",
            "buyer_id": buyer_id,
            "seller_id": seller_id,
            "product_name": product_name
        }
