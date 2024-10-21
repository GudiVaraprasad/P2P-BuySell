# peer.py
import socket
import threading
from network.peer_registry import register_peer, wait_for_all_peers

class Peer:
    def __init__(self, peer_id, role, neighbors, product_name=None, stock=0, ip=None, total_peers=6):
        self.peer_id = peer_id
        self.role = role
        self.ip = ip if ip is not None else self.get_local_ip()  # Use provided IP or get local IP dynamically
        self.port = None  # Dynamically assigned later
        self.neighbors = neighbors
        self.product_name = product_name
        self.stock = stock
        self.running = True
        self.lock = threading.Lock()  # Lock for synchronization
        self.processed_requests = set()  # Initialize a set to track processed requests

        # Register the peer in the central registry and wait for all peers
        register_peer(self.peer_id, self.ip)  # Notify central registry of this peer
        wait_for_all_peers(total_peers)  # Wait until all peers have joined the network
    
    def get_local_ip(self):
        """Function to get the local IP address of the machine."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))  # Google DNS address to trigger IP lookup
                return s.getsockname()[0]
        except Exception as e:
            print(f"Error getting local IP address: {e}")
            return "127.0.0.1"  # Fallback to localhost if any issues

    def start(self):
        # Start listening for requests
        threading.Thread(target=self.listen_for_requests).start()

    def listen_for_requests(self):
        # Bind the socket to the peer's IP and a dynamic port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self.ip, 0))  # Bind to the peer's IP and let the OS choose a port
            self.port = server.getsockname()[1]  # Retrieve the dynamically assigned port
            print(f"Peer {self.peer_id} is listening on {self.ip}:{self.port}")
            
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

    
    def send_message(self, peer_ip, peer_port, message):
        """Send a message to a peer at the given IP and port."""
        try:
            # Create a socket and connect to the neighbor's IP and port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((peer_ip, peer_port))  # Use peer's IP and port
                sock.sendall(message.encode())
                print(f"Peer {self.peer_id} sent message to {peer_ip}:{peer_port}: {message}")
        except Exception as e:
            print(f"Error sending message to {peer_ip}:{peer_port}: {e}")