from protocol.message import Message

def handle_reply(peer, message):
    """Handle incoming reply messages."""
    print(f"DEBUG: Peer {peer.peer_id} (buyer) received reply from seller {message['seller_id']}")
    if peer.role == "buyer":
        buy_message = Message.buy(
            buyer_id=peer.peer_id,
            seller_id=message['seller_id'],
            product_name=message['product_name']
        )
        seller_port = peer.port_mapping.get(message['seller_id'])
        if seller_port:
            # print(f"DEBUG: Peer {peer.peer_id} is preparing to send buy message to Seller {message['seller_id']} on port {seller_port}")
            peer.messaging_service.send_message(buy_message, seller_port)
        else:
            print(f"ERROR: Could not find port for Seller {message['seller_id']}")
