# peer.py
import socket
import threading

class Peer:
    def __init__(self, peer_id, role, neighbors, product_name=None, stock=0):
        self.peer_id = peer_id
        self.role = role
        self.port = None  # Dynamically assigned later
        self.neighbors = neighbors
        self.product_name = product_name
        self.stock = stock
        self.running = True


    def start(self):
        # Start listening for requests
        threading.Thread(target=self.listen_for_requests).start()

    def listen_for_requests(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(('localhost', 0))  # Bind to port 0 to let the OS choose an available port
            self.port = server.getsockname()[1]  # Retrieve the dynamically assigned port
            print(f"Peer {self.peer_id} is listening on dynamically assigned port {self.port}")
            
            server.listen(5)
            try:
                while self.running:
                    conn, addr = server.accept()
                    print(f"Peer {self.peer_id} received connection from {addr}")
                    threading.Thread(target=self.handle_request, args=(conn,)).start()
            except Exception as e:
                print(f"Error in Peer {self.peer_id}: {e}")
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
