from email import message
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(matrix):
    plt.figure(figsize=(5, 4))
    G = nx.Graph()

    N = len(matrix)

    for i in range(N):
        G.add_node(i + 1)

    for i in range(N):
        for j in range(i + 1, N):
            if matrix[i][j] > 0:
                G.add_edge(i + 1, j + 1)

    pos = nx.spring_layout(G, seed=42)

    nx.draw_networkx_nodes(G, pos, node_color='#3498db', node_size=500)
    nx.draw_networkx_labels(G, pos, font_color='white')
    nx.draw_networkx_edges(G, pos, width=2)

    plt.axis('off')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    img = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()

    return img

def solve_euler(matrix):
    N = len(matrix)
    # Генерируем картинку СРАЗУ, чтобы отдать её фронтенду при любом раскладе!
    img_base64 = draw_graph(matrix)
    
    degrees = [sum(row) for row in matrix]
    isolated_vertices = [i + 1 for i, deg in enumerate(degrees) if deg == 0]
    
    # ПРОВЕРКА 1: Изолированные вершины (выводим ошибку, но КАРТИНКУ ПЕРЕДАЕМ)
    if isolated_vertices:
        return {
            "exists": False,
            "message": f"Обнаружены изолированные вершины: {isolated_vertices}. Некоторые вершины отделены!",
            "image": img_base64, # <- Граф построится!
            "degrees": degrees
        }
        
    total_edges = sum(degrees) // 2
    if total_edges == 0:
        return {
            "exists": False,
            "message": "В графе нет рёбер. Эйлеров маршрут не существует.",
            "image": img_base64
        }

    # Считаем матрицу достижимости (транзитивное замыкание)
    closure = [row[:] for row in matrix]
    for i in range(N):
        closure[i][i] = 1

    for k in range(N):
        for i in range(N):
            for j in range(N):
                closure[i][j] = closure[i][j] or (closure[i][k] and closure[k][j])

    # Проверяем связность графа для вершин с рёбрами
    start_vertex = next((i for i, deg in enumerate(degrees) if deg > 0), None)
    is_connected = True

    if start_vertex is not None:
        for i in range(N):
            if not closure[start_vertex][i]:
                is_connected = False
                break

    # ПРОВЕРКА 2: Граф несвязен (выводим ошибку, но КАРТИНКУ ПЕРЕДАЕМ)
    if not is_connected:
        return {
            "exists": False,
            "message": "Граф несвязен (компоненты с рёбрами изолированы друг от друга).",
            "image": img_base64, # <- Граф построится!
            "degrees": degrees,
            "closure": closure
        }
    
    # Проверяем условия Эйлеровости (чётность степеней)
    odd_vertices = [i + 1 for i, deg in enumerate(degrees) if deg % 2 != 0]
    
    if len(odd_vertices) == 0:
        graph_type = "Эйлеров цикл"
        start_vertex = next(i for i, deg in enumerate(degrees) if deg > 0)
    elif len(odd_vertices) == 2:
        graph_type = "Эйлерова цепь"
        start_vertex = odd_vertices[0] - 1
    else:
        return {
            "exists": False,
            "message": f"Найдено нечётное количество вершин с нечётной степенью ({len(odd_vertices)}). Маршрут невозможен.",
            "odd_vertices": odd_vertices,
            "image": img_base64 # <- Граф построится!
        }

    # Алгоритм Флёри / Иерархольцера для поиска пути
    graph = [row[:] for row in matrix]
    stack = [start_vertex]
    Result = []

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
            Result.append(stack.pop() + 1)

    Result.reverse()
    
    # УДАЛИЛИ строку img_base64 = "", которая стирала картинку!
    
    return {
        "exists": True,
        "type": graph_type,
        "message": "Маршрут успешно найден",
        "start_vertex": start_vertex + 1,
        "odd_vertices": odd_vertices,
        "path": Result,
        "degrees": degrees,
        "closure": closure,
        "image": img_base64 # Передаем готовую картинку успешного графа
    }
