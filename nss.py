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
            for _ in range(k):
                shortest_paths = []
                for cdn_server in cdn_servers:
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
                    network_copy.remove_nodes_from(best_path [1:])  # Keep the source node
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


paths = different_servers(network, cdn_servers, 3)
print_paths("Different CDN servers", paths)
paths = same_server(network, cdn_servers, 3)
print_paths("Same CDN server", paths)