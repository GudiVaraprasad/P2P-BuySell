# peer.py
import socket
import threading

class Peer:
    def __init__(self, peer_id, role, port, neighbors, product_name=None, stock=0):
        self.peer_id = peer_id
        self.role = role
        self.port = port
        self.neighbors = neighbors
        self.product_name = product_name
        self.stock = stock  # Add stock attribute for sellers
        self.running = True

        print(f"Peer {self.peer_id} initialized as {self.role} with product {self.product_name} and stock {self.stock}")

    def start(self):
        # Start listening for requests
        threading.Thread(target=self.listen_for_requests).start()

    def listen_for_requests(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            try:
                server.bind(('localhost', self.port))
                server.listen(5)
                print(f"Peer {self.peer_id} is listening on port {self.port}")
                
                while self.running:
                    conn, addr = server.accept()
                    print(f"Peer {self.peer_id} received connection from {addr}")
                    threading.Thread(target=self.handle_request, args=(conn,)).start()
            except OSError as e:
                print(f"Error binding Peer {self.peer_id} to port {self.port}: {e}")
            finally:
                server.close()

    def handle_request(self, conn):
        from protocol.handler import MessageHandler
        handler = MessageHandler(self)  # Create a message handler
        handler.handle_message(conn)  # Pass the connection to handle_message
        conn.close()  # Close the connection after handling

    
    def send_message(self, neighbor_port, message):
        try:
            # Create a socket and connect to the neighbor's port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('localhost', neighbor_port))
                sock.send(message.encode())
                print(f"Peer {self.peer_id} sent message: {message}")
        except Exception as e:
            print(f"Error sending message to peer on port {neighbor_port}: {e}")
