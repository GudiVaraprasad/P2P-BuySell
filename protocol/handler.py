# protocol/handler.py
import json
from protocol.message import Message

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
        # Check if this peer is a seller and has the requested product
        if self.peer.role == "seller" and message['product_name'] == self.peer.product_name:
            print(f"Seller {self.peer.peer_id} has the product: {message['product_name']}")
            
            # Send a reply message back to the buyer
            reply_message = Message.reply(
                seller_id=self.peer.peer_id,
                buyer_id=message['buyer_id'],
                product_name=message['product_name'],
                path=message['path']
            )
            # Dynamically determine the buyer's port instead of hardcoding
            buyer_port = self.peer.neighbors[0]  # Assuming neighbors[0] is the buyer's port (adjust if needed)
            self.send_message(reply_message, buyer_port)
            print(f"Seller {self.peer.peer_id} sent reply to Buyer {message['buyer_id']} on port {buyer_port}")
        else:
            print(f"Seller {self.peer.peer_id} does not have the product or is not a seller")


    def propagate(self, message):
        # Propagate the message to all neighbors
        for neighbor_port in self.peer.neighbors:
            self.send_message(message, neighbor_port)

    def send_message(self, message, port):
        print(f"Attempting to send message to port {port}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('localhost', port))
                sock.send(json.dumps(message).encode())
                print(f"Message sent to port {port}: {message}")
        except Exception as e:
            print(f"Error sending message to peer on port {port}: {e}")



    def handle_reply(self, message):
        print(f"Peer {self.peer.peer_id} (buyer) received reply from seller {message['seller_id']}")
        if self.peer.role == "buyer":
            # The buyer sends a buy message to the chosen seller
            buy_message = Message.buy(
                buyer_id=self.peer.peer_id,
                seller_id=message['seller_id'],
                product_name=message['product_name']
            )
            self.send_message(buy_message, message['seller_id'])

    def handle_buy(self, message):
        print(f"Peer {self.peer.peer_id} (seller) received buy request from buyer {message['buyer_id']}")
        if self.peer.role == "seller" and self.peer.product_name == message['product_name']:
            # Check if the seller has stock
            if self.peer.stock > 0:
                self.peer.stock -= 1
                print(f"Seller {self.peer.peer_id} sold {message['product_name']} to Buyer {message['buyer_id']}")
            else:
                print(f"Seller {self.peer.peer_id} is out of stock!")

