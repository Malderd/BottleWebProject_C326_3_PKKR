import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import base64
from io import BytesIO

def draw_graph(matrix):
    """Рисует граф и возвращает base64 строку изображения"""
    N = len(matrix)
    G = nx.Graph()
    
    # Добавляем все вершины
    for i in range(N):
        G.add_node(i + 1)
    
    # Добавляем рёбра
    for i in range(N):
        for j in range(i + 1, N):
            if matrix[i][j] > 0:
                G.add_edge(i + 1, j + 1)
    
    # Создаём рисунок
    plt.figure(figsize=(10, 8))
    
    # Используем разные цвета для изолированных вершин
    pos = nx.spring_layout(G, k=2, iterations=50) if N > 0 else {}
    
    # Определяем цвета для вершин
    node_colors = []
    for i in range(N):
        if G.degree(i + 1) == 0:
            node_colors.append('#ffcccc')  # Светло-красный для изолированных
        else:
            node_colors.append('#a5d6a7')  # Зелёный для связных
    
    nx.draw(G, pos, with_labels=True, node_color=node_colors,
            node_size=500, font_size=16, font_weight='bold',
            edge_color='#666666', width=2)
    
    # Сохраняем в буфер
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    plt.close()
    
    return image_base64

def check_connectivity(matrix):
    """Проверяет связность графа (все вершины с рёбрами должны быть связны)"""
    N = len(matrix)
    
    # Находим все вершины, у которых есть рёбра (степень > 0)
    vertices_with_edges = [i for i in range(N) if sum(matrix[i]) > 0]
    
    # Если нет ни одной вершины с рёбрами или только одна вершина с рёбрами
    if len(vertices_with_edges) <= 1:
        return True, []
    
    # BFS для проверки связности только между вершинами с рёбрами
    start = vertices_with_edges[0]
    visited = [False] * N
    queue = [start]
    visited[start] = True
    
    while queue:
        v = queue.pop(0)
        for u in range(N):
            if matrix[v][u] > 0 and not visited[u]:
                visited[u] = True
                queue.append(u)
    
    # Находим непосещённые вершины, у которых есть рёбра
    isolated_components = []
    for i in vertices_with_edges:
        if not visited[i]:
            isolated_components.append(i + 1)
    
    return len(isolated_components) == 0, isolated_components

def find_eulerian_path(matrix):
    """Находит Эйлеров цикл или цепь в графе"""
    N = len(matrix)
    
    # Степени вершин
    degrees = [sum(row) for row in matrix]
    isolated_vertices = [i + 1 for i, deg in enumerate(degrees) if deg == 0]

    if isolated_vertices:
        return {
            "type": "isolated_vertex",
            "message": f"Нельзя посчитать граф, потому что есть несвязная вершина: {', '.join(map(str, isolated_vertices))}",
            "degrees": degrees,
            "odd_vertices": [],
            "path": [],
            "is_connected": False,
            "isolated_vertices": isolated_vertices,
            "has_edges": True
        }
    
    # Проверка на существование рёбер
    has_edges = any(deg > 0 for deg in degrees)
    
    # Если нет рёбер
    if not has_edges:
        result_type = "no_edges"
        result_message = "В графе нет рёбер. Эйлеров маршрут не существует."
        return {
            "type": result_type,
            "message": result_message,
            "degrees": degrees,
            "odd_vertices": [],
            "path": [],
            "is_connected": True,
            "has_edges": False
        }
    
    # Проверка связности (только вершины с рёбрами должны быть связны)
    is_connected, isolated_components = check_connectivity(matrix)
    
    # Если граф не связный (есть несколько компонент с рёбрами)
    if not is_connected:
        result_type = "disconnected"
        result_message = f"Граф не связный! Обнаружены изолированные компоненты: вершины {', '.join(map(str, isolated_components))}"
        return {
            "type": result_type,
            "message": result_message,
            "degrees": degrees,
            "odd_vertices": [],
            "path": [],
            "is_connected": False,
            "isolated_components": isolated_components,
            "has_edges": True
        }
    
    # Проверка на существование Эйлерова цикла/цепи
    odd_vertices = [i for i, deg in enumerate(degrees) if deg % 2 == 1]
    odd_count = len(odd_vertices)
    
    if odd_count == 0:
        result_type = "cycle"
        result_message = "В графе существует Эйлеров цикл"
    elif odd_count == 2:
        result_type = "path"
        result_message = "В графе существует Эйлерова цепь"
    else:
        result_type = "none"
        result_message = f"В графе нет Эйлерова цикла или цепи (нечётных вершин: {odd_count})"
        return {
            "type": result_type,
            "message": result_message,
            "degrees": degrees,
            "odd_vertices": odd_vertices,
            "path": [],
            "is_connected": True,
            "has_edges": True
        }
    
    # Находим стартовую вершину
    if odd_count == 0:
        # Для цикла начинаем с любой вершины, у которой есть рёбра
        start_vertex = next((i for i, deg in enumerate(degrees) if deg > 0), 0)
    else:
        # Для цепи начинаем с нечётной вершины
        start_vertex = odd_vertices[0]
    
    # Алгоритм Иерхольцера
    graph = [row[:] for row in matrix]
    stack = [start_vertex]
    result_path = []
    
    while stack:
        v = stack[-1]
        has_edge = False
        for u in range(N):
            if graph[v][u] > 0:
                graph[v][u] -= 1
                graph[u][v] -= 1
                stack.append(u)
                has_edge = True
                break
        if not has_edge:
            result_path.append(stack.pop() + 1)  # Приводим к 1-индексации
    
    result_path.reverse()
    
    return {
        "type": result_type,
        "message": result_message,
        "degrees": degrees,
        "odd_vertices": odd_vertices,
        "path": result_path,
        "start_vertex": start_vertex + 1,
        "is_connected": True,
        "has_edges": True
    }