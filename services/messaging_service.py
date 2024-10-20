import socket
import json

class MessagingService:
    def __init__(self, peer):
        self.peer = peer

    def send_message(self, message, port):
        """Send a message to the specified port."""
        print(f"Peer {self.peer.peer_id} is attempting to send message to port {port}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('localhost', port))
                sock.send(json.dumps(message).encode())
                print(f"Message sent to port {port}: {message}")
        except Exception as e:
            print(f"Error sending message to port {port}: {e}")
