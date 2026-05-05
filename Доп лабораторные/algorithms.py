from collections import deque


def bfs(graph, start):
    """Обход графа в ширину (для невзвешенного графа)"""
    if not graph or start not in graph:
        return []

    visited = set()
    order = []
    queue = deque([start])
    visited.add(start)

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in sorted(graph.get(node, set())):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


def dfs_iterative(graph, start):
    """Итеративный обход графа в глубину (для невзвешенного графа)"""
    if not graph or start not in graph:
        return []

    visited = set()
    order = []
    stack = [start]

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            order.append(node)
            for neighbor in sorted(graph.get(node, set()), reverse=True):
                if neighbor not in visited:
                    stack.append(neighbor)

    return order


def dfs_recursive(graph, start, visited=None, order=None):
    """Рекурсивный обход графа в глубину (для невзвешенных графов)"""
    if visited is None:
        visited = set()
    if order is None:
        order = []

    visited.add(start)
    order.append(start)

    for neighbor in sorted(graph.get(start, set())):
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited, order)

    return order


def dfs(graph, start):
    """Обход графа в глубину (итеративная версия по умолчанию)"""
    return dfs_iterative(graph, start)


def connected_components(graph):
    """Поиск компонент связности (для невзвешенного графа)"""
    if not graph:
        return []

    visited = set()
    components = []

    for node in sorted(graph.keys()):
        if node not in visited:
            component = dfs_recursive(graph, node, visited=visited)
            components.append(component)

    return components


def bellman_ford(weighted_graph, start):
    """
    Алгоритм Беллмана-Форда с корректной обработкой отрицательных циклов.
    """
    if not weighted_graph or start not in weighted_graph:
        return {}, {}, False, [], set()

    # Собираем все вершины и рёбра
    vertices = set()
    edges = []

    for u, neighbors in weighted_graph.items():
        vertices.add(u)
        for v, w in neighbors:
            vertices.add(v)
            edges.append((u, v, w))

    V = len(vertices)

    # Инициализация
    distance = {v: float("inf") for v in vertices}
    predecessor = {v: None for v in vertices}
    distance[start] = 0

    # Основная релаксация
    for _ in range(V - 1):
        relaxed = False

        for u, v, w in edges:
            if distance[u] != float("inf") and distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                predecessor[v] = u
                relaxed = True

        if not relaxed:
            break

    # Сохраняем корректные расстояния до обнаружения цикла
    final_distance = distance.copy()
    final_predecessor = predecessor.copy()

    # Вершины, которые можно улучшить ещё раз (V-я итерация)
    changed_vertices = set()

    for u, v, w in edges:
        if distance[u] != float("inf") and distance[u] + w < distance[v]:
            changed_vertices.add(v)

    affected_vertices = set()
    cycle_path = []

    if changed_vertices:
        reachable_from_start = _get_reachable(vertices, edges, start)

        # Только достижимые из start вершины могут иметь значение
        changed_vertices &= reachable_from_start

        if changed_vertices:
            # Строим список смежности
            adj_list = {v: [] for v in vertices}
            for u, v, w in edges:
                adj_list[u].append(v)

            # Все вершины, достижимые из отрицательного цикла
            queue = deque(changed_vertices)
            affected_vertices = set(changed_vertices)

            while queue:
                u = queue.popleft()

                for v in adj_list[u]:
                    if v not in affected_vertices:
                        affected_vertices.add(v)
                        queue.append(v)

            cycle_path = _find_negative_cycle(predecessor, edges, changed_vertices, V)

    has_negative_cycle = len(affected_vertices) > 0

    # Формируем итоговые расстояния
    result_distance = {}

    for v in vertices:
        if v in affected_vertices:
            result_distance[v] = float("-inf")
        else:
            result_distance[v] = final_distance[v]

    return (
        result_distance,
        final_predecessor,
        has_negative_cycle,
        cycle_path,
        affected_vertices,
    )


def _get_reachable(vertices, edges, start):
    """Возвращает множество вершин, достижимых из start."""
    adj_list = {v: [] for v in vertices}

    for u, v, w in edges:
        adj_list[u].append(v)

    visited = {start}
    queue = deque([start])

    while queue:
        u = queue.popleft()

        for v in adj_list[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)

    return visited


def _find_negative_cycle(predecessor, edges, cycle_vertices, V):
    """Восстанавливает отрицательный цикл."""
    if not cycle_vertices:
        return []

    x = next(iter(cycle_vertices))

    # Заходим внутрь цикла
    for _ in range(V):
        x = predecessor.get(x)
        if x is None:
            return []

    # Восстанавливаем цикл
    cycle = [x]
    current = predecessor[x]

    while current is not None and current != x:
        cycle.append(current)
        current = predecessor[current]

        if len(cycle) > V + 1:
            return []

    if current is None:
        return []

    cycle.append(x)
    cycle.reverse()

    return cycle


def get_path(predecessors, start, end):
    """Восстановление кратчайшего пути."""
    if start == end:
        return [start]

    if end not in predecessors or predecessors[end] is None:
        return []

    path = []
    current = end
    visited = set()

    while current is not None and current not in visited:
        path.append(current)

        if current == start:
            path.reverse()
            return path

        visited.add(current)
        current = predecessors.get(current)

    return []
