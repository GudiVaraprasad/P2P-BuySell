import networkx as nx  # Import NetworkX
import matplotlib.pyplot as plt  # Import Matplotlib for plotting

def visualize_network(peers):
    """Visualize the peer network using NetworkX and Matplotlib."""
    G = nx.Graph()

    # Add nodes (peers) to the graph with labels (peer ID and role)
    for peer in peers:
        G.add_node(peer.peer_id, label=f"Peer {peer.peer_id} ({peer.role})")

    # Add edges (connections between peers) based on neighbors
    added_edges = set()  # To avoid duplicate edges
    for peer in peers:
        for neighbor_port in peer.neighbors:
            # Find the peer ID based on the neighbor's port
            neighbor_id = next(p.peer_id for p in peers if p.port == neighbor_port)

            # Ensure we don't add duplicate edges in an undirected graph
            edge = tuple(sorted((peer.peer_id, neighbor_id)))
            if edge not in added_edges:
                G.add_edge(peer.peer_id, neighbor_id)
                added_edges.add(edge)

    # Draw the graph
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)  # Layout for positioning nodes

    # Draw nodes with labels
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold')

    # Add labels to indicate peer roles (label as Peer ID and Role)
    labels = {peer.peer_id: f"Peer {peer.peer_id}\n({peer.role})" for peer in peers}
    nx.draw_networkx_labels(G, pos, labels=labels)

    plt.title("P2P Network Structure")
    plt.show()
