# # protocol/handler.py
# import json
# from protocol.message import Message
# import socket

# class MessageHandler:
#     def __init__(self, peer):
#         self.peer = peer

#     def handle_message(self, conn):
#         # Receive and decode the incoming message
#         data = conn.recv(1024).decode()
#         message = json.loads(data)
#         print(f"Peer {self.peer.peer_id} received message: {message}")

#         # Handle different message types
#         if message['type'] == 'lookup':
#             self.handle_lookup(message)
#         elif message['type'] == 'reply':
#             self.handle_reply(message)
#         elif message['type'] == 'buy':
#             self.handle_buy(message)

#     def handle_lookup(self, message):
#         """Handle incoming lookup requests."""
#         print(f"DEBUG: Entered handle_lookup for Peer {self.peer.peer_id} with message: {message}")

#         # Prevent handling duplicate lookup requests by tracking request IDs (or timestamps)
#         request_id = (message['buyer_id'], message['product_name'])
#         if request_id in self.peer.processed_requests:
#             print(f"DEBUG: Peer {self.peer.peer_id} has already processed request {request_id}. Ignoring duplicate.")
#             return  # Ignore duplicate request
#         else:
#             self.peer.processed_requests.add(request_id)  # Track this request as processed

#         if self.peer.role == "seller":
#             # Check if the seller has the requested product
#             if message['product_name'] == self.peer.product_name:
#                 with self.peer.lock:  # Synchronize stock checking and modification
#                     if self.peer.stock > 0:
#                         # Seller has the product, send a reply
#                         print(f"DEBUG: Peer {self.peer.peer_id} is a seller. Proceeding to product check.")
#                         reply_message = Message.reply(
#                             seller_id=self.peer.peer_id,
#                             buyer_id=message['buyer_id'],
#                             product_name=message['product_name'],
#                             path=message.get('path', []) + [self.peer.peer_id]  # Append current peer to the path
#                         )
#                         buyer_port = self.peer.port_mapping.get(message['buyer_id'])  # Use port mapping for buyer
#                         if buyer_port:
#                             print(f"DEBUG: Peer {self.peer.peer_id} found the product. Sending reply to Peer {message['buyer_id']} on port {buyer_port}")
#                             self.send_message(reply_message, buyer_port)

#                             # Decrement stock after sending the reply
#                             self.peer.stock -= 1
#                             print(f"DEBUG: Peer {self.peer.peer_id} has sold {message['product_name']}. Stock is now {self.peer.stock}.")
#                         else:
#                             print(f"ERROR: Peer {self.peer.peer_id} could not find port for Buyer {message['buyer_id']}")
#                     else:
#                         print(f"DEBUG: Peer {self.peer.peer_id} is out of stock.")
#             else:
#                 print(f"DEBUG: Peer {self.peer.peer_id} does not have the requested product.")
#         else:
#             # Forward the message to neighbors
#             if message['hop_count'] > 0:
#                 message['hop_count'] -= 1
#                 message['path'].append(self.peer.peer_id)
#                 for neighbor_port in self.peer.neighbors:
#                     if neighbor_port != self.peer.port:  # Avoid sending back to itself
#                         print(f"DEBUG: Peer {self.peer.peer_id} forwarding lookup message to {neighbor_port}")
#                         self.send_message(message, neighbor_port)
#             else:
#                 print(f"DEBUG: Peer {self.peer.peer_id} cannot forward message, hop_count reached 0.")

#     def send_message(self, message, port):
#         print(f"Peer {self.peer.peer_id} is attempting to send message to port {port}")
#         try:
#             with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#                 sock.connect(('localhost', port))
#                 sock.send(json.dumps(message).encode())
#                 print(f"Message sent to port {port}: {message}")
#         except Exception as e:
#             print(f"Error sending message to port {port}: {e}")

#     def handle_reply(self, message):
#         print(f"DEBUG: Peer {self.peer.peer_id} (buyer) received reply from seller {message['seller_id']}")

#         if self.peer.role == "buyer":
#             # Send a buy message to the seller
#             buy_message = Message.buy(
#                 buyer_id=self.peer.peer_id,
#                 seller_id=message['seller_id'],
#                 product_name=message['product_name']
#             )
#             path = message.get('path', [])
#             if path:
#                 seller_port = self.peer.port_mapping.get(message['seller_id'])  # Use port mapping for the seller
#                 if seller_port:
#                     print(f"DEBUG: Peer {self.peer.peer_id} is preparing to send buy message to Seller {message['seller_id']} on port {seller_port}")
#                     self.send_message(buy_message, seller_port)
#                 else:
#                     print(f"ERROR: Could not find port for Seller {message['seller_id']}")
#             else:
#                 print("ERROR: No path found in reply message.")

#     def handle_buy(self, message):
#         print(f"Peer {self.peer.peer_id} (seller) received buy request from buyer {message['buyer_id']} for product {message['product_name']}")

#         # Use the lock to ensure thread-safe stock decrement
#         with self.peer.lock:
#             if self.peer.stock > 0:
#                 self.peer.stock -= 1
#                 print(f"Seller {self.peer.peer_id} sold {message['product_name']} to Buyer {message['buyer_id']}")
#                 print(f"Seller {self.peer.peer_id} now has {self.peer.stock} items remaining")
#             else:
#                 print(f"Seller {self.peer.peer_id} is out of stock!")

from services.lookup_service import handle_lookup
from services.reply_service import handle_reply
from services.buy_service import handle_buy
from services.messaging_service import MessagingService
import json
from protocol.message import Message
import socket

class MessageHandler:
    def __init__(self, peer):
        self.peer = peer
        self.peer.messaging_service = MessagingService(peer)  # Initialize messaging service

    def handle_message(self, conn):
        data = conn.recv(1024).decode()
        message = json.loads(data)
        print(f"Peer {self.peer.peer_id} received message: {message}")

        if message['type'] == 'lookup':
            handle_lookup(self.peer, message)
        elif message['type'] == 'reply':
            handle_reply(self.peer, message)
        elif message['type'] == 'buy':
            handle_buy(self.peer, message)