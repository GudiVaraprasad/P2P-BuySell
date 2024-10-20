import random

def switch_product(seller_peer, products):
    """Switch the product a seller is selling after depleting the stock."""
    new_product = random.choice(products)
    seller_peer.product_name = new_product
    seller_peer.stock = random.randint(2, 5)
    print(f"Seller {seller_peer.peer_id} now sells {new_product} with {seller_peer.stock} items remaining")
