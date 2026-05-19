import heapq
from typing import List, Tuple

def dijkstra(start: int, graph: dict[int, List[Tuple[int, int]]]) -> dict[int, float]:
    dist = {node: float("inf") for node in graph}
    dist[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_dist, u = heapq.heappop(priority_queue)

        if current_dist > dist[u]:
            continue

        for v, weight in graph[u]:
            new_dist = current_dist + weight

            if dist[v] > new_dist:
                dist[v] = new_dist
                heapq.heappush(priority_queue, (new_dist, v))

    return dist

def build_graph(nodes: List[int], edges: List[Tuple[int, int, int]]):
    graph = {node: [] for node in nodes}
    for u, v, w in edges:
        if u in graph and v in graph:
            graph[u].append((v, w))
            graph[v].append((u, w))
    return graph
 
def find_best_server(nodes: List[int], clients: List[int], edges: List[Tuple[int, int, int]]) -> int:
    graph = build_graph(nodes, edges)

    clients_set = set(clients)
    best_result = float("inf")

    for server in nodes:
        if server in clients_set:
            continue

        dist = dijkstra(server, graph)
        max_latency = max(dist[c] for c in clients)

        best_result = min(best_result, max_latency)
    
    return int(best_result) if best_result != float("inf") else -1

def find_best_server_steps(nodes: List[int], clients: List[int], edges: List[Tuple[int, int, int]]) -> Tuple[int, List[Tuple[int, int, int]]]:
    graph = build_graph(nodes, edges)

    clients_set = set(clients)
    best_result = float("inf")
    steps = []

    for server in nodes:
        if server in clients_set:
            continue

        dist = dijkstra(server, graph)
        max_latency = max(dist[c] for c in clients)

        best_result = min(best_result, max_latency)
        steps.append((server, max_latency, best_result))

    return best_result, steps

def compute_server_latency(server: int, clients: List[int], edges: List[Tuple[int, int, int]], nodes: List[int]) -> int:
    graph = build_graph(nodes, edges)
    dist = dijkstra(server, graph)
    if any(dist[c] == float('inf') for c in clients):
        return -1
    return int(max(dist[c] for c in clients))
    