import networkx as nx
import matplotlib.pyplot as plt

# Create the network graph
network = nx.Graph()
edges = [
        (1, 2), (1, 4),
        (2, 3), (2, 5),
        (3, 5), (3, 8),
        (4, 6), (4, 7),
        (5, 7),
        (6, 9),
        (7, 8), (7, 11),
        (8, 13),
        (9, 10), (9, 11),
        (10, 14),
        (11, 12), (11, 14),
        (12, 13), (12, 15),
        (13, 16), (13, 18),
        (14, 15), (14, 17), (14, 23),
        (15, 17),
        (16, 19),
        (17, 18), (17, 23), (17, 20),
        (18, 19), (18, 20),
        (19, 21), (19, 22),
        (20, 21), (20, 25),
        (21, 22),
        (23, 24), (23, 26), (23, 28),
        (24, 25), (24, 27), (24, 28),
        (26, 27),
        (27, 28)
]
network.add_edges_from(edges)

# cdn_server servers
cdn_servers = [7,14,19,24]

def different_servers(network, cdn_servers, k) -> dict[int, list[(list[int],int, int)]]:
    ''' Find the k shortest paths from each node to the cdn_servers, but all paths must end at different cdn_servers.
    The paths must be node disjoint, meaning that they cannot share any nodes except for the source and target nodes.
    return a dictionary where the keys are the nodes in the network and the values are lists of tuples, 
    where each tuple contains a path (as a list of nodes), its length, and the target cdn_server. 
    The paths in each list should be ordered by length, with the shortest path first.
    The first path is the primary path and the rest are backup paths.
    '''
    result = {}
    for node in network.nodes():
        if node not in cdn_servers:
            network_copy = network.copy()
            cdn_servers_copy = cdn_servers.copy()
            for _ in range(k):
                shortest_paths = []
                for cdn_server in cdn_servers_copy:
                    try:
                        path = nx.dijkstra_path(network_copy, source=node, target=cdn_server)
                        path_length = nx.dijkstra_path_length(network_copy, source=node, target=cdn_server)
                        shortest_paths.append((path, path_length, cdn_server))
                    except nx.NetworkXNoPath:
                        continue
                if shortest_paths:
                    shortest_paths.sort(key=lambda x: x[1])  # Sort by path length
                    best_path, best_length, target_cdn_server = shortest_paths[0]
                    result.setdefault(node, []).append((best_path, best_length, target_cdn_server))
                    # Remove the nodes in the best path from the network copy
                    network_copy.remove_nodes_from(best_path[1:-1])  # Keep the source and target nodes
                    cdn_servers_copy.remove(target_cdn_server)  # Remove the target cdn_server from the list to ensure different servers
                else:
                    result.setdefault(node, []).append(([], float('inf'), None))  # No path found   
    return result

def same_server(network, cdn_servers, k) -> dict[int, list[(list[int],int, int)]]:
    ''' Find the k shortest paths from each node to the cdn_servers, but all paths must end at the same cdn_server. 
    The paths must be node disjoint, meaning that they cannot share any nodes except for the source and target nodes.
    return a dictionary where the keys are the nodes in the network and the values are lists of tuples, 
    where each tuple contains a path (as a list of nodes), its length, and the target cdn_server. 
    The paths in each list should be ordered by length, with the shortest path first.
    The first path is the primary path and the rest are backup paths.
    '''
    result = {}
    for node in network.nodes():
        if node not in cdn_servers:
            network_copy = network.copy()
            cdn_servers_copy = cdn_servers.copy()
            for _ in range(k):
                shortest_paths = []
                for cdn_server in cdn_servers_copy:
                    try:
                        path = nx.dijkstra_path(network_copy, source=node, target=cdn_server)
                        path_length = nx.dijkstra_path_length(network_copy, source=node, target=cdn_server)
                        shortest_paths.append((path, path_length, cdn_server))
                    except nx.NetworkXNoPath:
                        continue
                if shortest_paths:
                    shortest_paths.sort(key=lambda x: x[1])  # Sort by path length
                    best_path, best_length, target_cdn_server = shortest_paths[0]
                    result.setdefault(node, []).append((best_path, best_length, target_cdn_server))
                    # Remove the nodes in the best path from the network copy
                    network_copy.remove_nodes_from(best_path[1:-1])  # Keep the source and target nodes
                    # If path length is 1, it means the source node is directly connected to the target cdn_server, so we remove the edge instead of the node
                    if best_length == 1:
                        network_copy.remove_edge(node, target_cdn_server)
                    # Remove all non target cdn_server servers from the copy list
                    cdn_servers_copy = [target_cdn_server]
                else:
                    result.setdefault(node, []).append(([], float('inf'), None))  # No path found
    return result

def print_paths(title, paths) -> None:
    print(f"\n{title}")
    print("=" * len(title))
    for node in sorted(paths):
        print(f"Node {node}:")
        for index, (path, length, target) in enumerate(paths[node], start=1):
            if not path:
                print(f"  Route {index}: no path available")
                continue
            route = " -> ".join(str(step) for step in path)
            print(
                f"  Route {index}: target_server = {target}, length = {length}, path = {route}"
            )

def calculate_average_lengths(node_paths, k) -> tuple[float, float, float, float]:
    primary_path_length = 0
    backup_paths_lengths = [0] * (k - 1)
    primary_count = 0
    backup_counts = [0] * (k - 1)
    for node in node_paths:
        for i, (path, length, target) in enumerate(node_paths[node]):
            if path:  # Only consider valid paths
                if i == 0:
                    primary_path_length += length
                    primary_count += 1
                else:
                    backup_paths_lengths[i - 1] += length
                    backup_counts[i - 1] += 1
    primary_avg = primary_path_length / primary_count if primary_count > 0 else float('inf')
    backup_avg = [length / count if count > 0 else float('inf') for length, count in zip(backup_paths_lengths, backup_counts)]
    total_avg = (primary_path_length + sum(backup_paths_lengths)) / (primary_count + sum(backup_counts)) if (primary_count + sum(backup_counts)) > 0 else float('inf')
    return (primary_avg, *backup_avg, total_avg)

def average_lengths_to_pretty_str(averages, k) -> str:
    result = []
    result.append(f"\nAverage Path Lengths (k={k}):")
    result.append("=" * 30)
    result.append(f"Primary Path Average Length: {averages[0]:.2f}")
    for i in range(1, k):
        result.append(f"Backup Path {i} Average Length: {averages[i]:.2f}")
    result.append(f"Overall Average Length: {averages[-1]:.2f}")
    return "\n".join(result)

def calculate_rejection_rate(node_paths, k) -> float:
    nodes = len(node_paths)
    reject_nodes = 0
    for node in node_paths:
        if any(not path for path, length, target in node_paths[node]):
            reject_nodes += 1
    return reject_nodes / nodes if nodes > 0 else 0.0

for k in [2, 3]:
    print(f"\nCalculating paths for k={k}...")
    same_server_paths = same_server(network, cdn_servers, k)
    print_paths(f"Same Server Paths (k={k})", same_server_paths)
    different_servers_paths = different_servers(network, cdn_servers, k)
    print_paths(f"Different Servers Paths (k={k})", different_servers_paths)
    same_avg = calculate_average_lengths(same_server_paths, k)
    same_rejection_rate = calculate_rejection_rate(same_server_paths, k)
    different_avg = calculate_average_lengths(different_servers_paths, k)
    different_rejection_rate = calculate_rejection_rate(different_servers_paths, k)
    print(f"\nSame Server {average_lengths_to_pretty_str(same_avg, k)}")
    print(f"Same Server Rejection Rate: {same_rejection_rate:.2%}")
    print(f"\nDifferent Servers {average_lengths_to_pretty_str(different_avg, k)}")
    print(f"Different Servers Rejection Rate: {different_rejection_rate:.2%}")