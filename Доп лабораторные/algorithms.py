from collections import deque


def bfs(graph, start):
    visited = set()
    order = []
    queue = deque([start])

    visited.add(start)

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


def dfs(graph, start, visited=None, order=None):
    if visited is None:
        visited = set()
    if order is None:
        order = []

    visited.add(start)
    order.append(start)

    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited, order)

    return order


def connected_components(graph):
    visited = set()
    components = []

    for node in graph:
        if node not in visited:
            component = dfs(graph, node, visited=set())
            visited.update(component)
            components.append(component)

    return components
