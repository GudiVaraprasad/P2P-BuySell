# protocol/handler.py
import json
from protocol.message import Message
import socket

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
        print(f"DEBUG: Entered handle_lookup for Peer {self.peer.peer_id} with message: {message}")

        # Check if peer is a seller
        if self.peer.role == "seller":
            print(f"DEBUG: Peer {self.peer.peer_id} is a seller. Proceeding to product check.")

            # Check if product matches
            if message['product_name'] == self.peer.product_name:
                print(f"DEBUG: Peer {self.peer.peer_id} found the product {self.peer.product_name}.")

                # Send reply
                reply_message = Message.reply(
                    seller_id=self.peer.peer_id,
                    buyer_id=message['buyer_id'],
                    product_name=message['product_name'],
                    path=message['path']
                )
                buyer_port = 5000
                print(f"DEBUG: Peer {self.peer.peer_id} preparing to send reply: {reply_message}")
                self.send_message(reply_message, buyer_port)
                print(f"DEBUG: Peer {self.peer.peer_id} successfully sent reply.")
            else:
                print(f"DEBUG: Peer {self.peer.peer_id} does not have the requested product.")
        else:
            print(f"DEBUG: Peer {self.peer.peer_id} is not a seller.")


    def propagate(self, message):
        # Propagate the message to all neighbors
        for neighbor_port in self.peer.neighbors:
            self.send_message(message, neighbor_port)

    def send_message(self, message, port):
        print(f"Peer {self.peer.peer_id} is attempting to send message to port {port}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('localhost', port))
                sock.send(json.dumps(message).encode())
                print(f"Message sent to port {port}: {message}")
        except Exception as e:
            print(f"Error sending message to port {port}: {e}")

    def handle_reply(self, message):
        print(f"Peer {self.peer.peer_id} (buyer) received reply from seller {message['seller_id']}")
        if self.peer.role == "buyer":
            # Send a buy message to the seller
            buy_message = Message.buy(
                buyer_id=self.peer.peer_id,
                seller_id=message['seller_id'],
                product_name=message['product_name']
            )
            seller_port = 5001  # Ensure the correct port for Peer 1
            print(f"Peer {self.peer.peer_id} is preparing to send buy message to Seller {message['seller_id']}")
            self.send_message(buy_message, seller_port)


    def handle_buy(self, message):
        print(f"Peer {self.peer.peer_id} (seller) received buy request from buyer {message['buyer_id']}")
        if self.peer.role == "seller" and self.peer.product_name == message['product_name']:
            # Check if the seller has stock
            if self.peer.stock > 0:
                self.peer.stock -= 1
                print(f"Seller {self.peer.peer_id} sold {message['product_name']} to Buyer {message['buyer_id']}")
            else:
                print(f"Seller {self.peer.peer_id} is out of stock!")

