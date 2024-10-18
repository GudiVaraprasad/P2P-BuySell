# network/peer.py
import socket
import threading
from protocol.message_handler import MessageHandler

class Peer:
    def __init__(self, peer_id, role, port, neighbors):
        self.peer_id = peer_id
        self.role = role  # "buyer" or "seller"
        self.port = port
        self.neighbors = neighbors
        self.items = 5 if role == "seller" else 0
        self.running = True
        self.message_handler = MessageHandler(self)

    def start(self):
        # Start server to listen for requests
        server_thread = threading.Thread(target=self.listen_for_requests)
        server_thread.start()

        # Buyers will initiate the buying process
        if self.role == "buyer":
            from services.buyer_service import BuyerService
            buyer = BuyerService(self)
            buyer.start_buying()

    def listen_for_requests(self):
        # Listen for incoming connections and handle requests
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(('localhost', self.port))
            server.listen(5)
            print(f"Peer {self.peer_id} listening on port {self.port}")

            while self.running:
                conn, addr = server.accept()
                threading.Thread(target=self.handle_request, args=(conn,)).start()

    def handle_request(self, conn):
        # Delegate the message handling to MessageHandler
        self.message_handler.handle(conn)
        conn.close()

    def stop(self):
        self.running = False
