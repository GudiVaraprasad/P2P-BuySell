# peer.py
import socket
import threading

class Peer:
    def __init__(self, peer_id, role, port, neighbors):
        self.peer_id = peer_id
        self.role = role  # "buyer" or "seller"
        self.port = port
        self.neighbors = neighbors
        self.running = True

    def start(self):
        # Start listening for requests
        threading.Thread(target=self.listen_for_requests).start()

    def listen_for_requests(self):
        # 1. Create a socket and bind it to the port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(('localhost', self.port))
            server.listen(5)  # Listen for up to 5 connections
            print(f"Peer {self.peer_id} is listening on port {self.port}")

            while self.running:
                # 2. Accept a connection
                conn, addr = server.accept()
                print(f"Peer {self.peer_id} received connection from {addr}")
                # 3. Handle the request (in a new thread)
                threading.Thread(target=self.handle_request, args=(conn,)).start()

    def handle_request(self, conn):
        # Receive the incoming message
        message = conn.recv(1024).decode()
        print(f"Peer {self.peer_id} received message: {message}")
        conn.close()
    
    def send_message(self, neighbor_port, message):
        try:
            # Create a socket and connect to the neighbor's port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('localhost', neighbor_port))
                sock.send(message.encode())
                print(f"Peer {self.peer_id} sent message: {message}")
        except Exception as e:
            print(f"Error sending message to peer on port {neighbor_port}: {e}")
