# services/graph_algorithms.py

from collections import deque

def bfs_shortest_path(start_peer_id, peer_dict):
    """Perform BFS to calculate shortest path distances from the start_peer."""
    visited = {peer_id: False for peer_id in peer_dict}  # Visited uses peer IDs
    distance = {peer_id: float('inf') for peer_id in peer_dict}  # Distance uses peer IDs
    queue = deque([start_peer_id])
    visited[start_peer_id] = True
    distance[start_peer_id] = 0

    while queue:
        current_peer_id = queue.popleft()

        # Iterate through the neighbors of the current peer (peer_dict maps peer IDs to Peer objects)
        for neighbor_port in peer_dict[current_peer_id].neighbors:
            # Find the peer ID associated with this neighbor's port
            neighbor_peer_id = next(peer.peer_id for peer in peer_dict.values() if peer.port == neighbor_port)

            if not visited[neighbor_peer_id]:
                visited[neighbor_peer_id] = True
                distance[neighbor_peer_id] = distance[current_peer_id] + 1
                queue.append(neighbor_peer_id)

    return distance


def calculate_graph_diameter(peers):
    """Calculate the graph diameter, which is the longest shortest path between any two peers."""
    max_diameter = 0
    for peer in peers:
        # Calculate the shortest paths from this peer using BFS
        distances = bfs_shortest_path(peer.peer_id, {p.peer_id: p for p in peers})
        max_diameter = max(max_diameter, max(distances.values()))  # Find the maximum shortest path

    return max_diameter
