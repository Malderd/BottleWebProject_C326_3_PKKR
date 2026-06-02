import io
import base64
import matplotlib
# Используем невизуальный бэкэнд, чтобы matplotlib работал на сервере без GUI
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

def solve_euler(matrix):
    """
    Основная функция анализа графа на наличие Эйлерова маршрута.
    Возвращает словарь с результатами, который ожидает JS-фронтенд.
    """
    n = len(matrix)
    
    # 1. Расчёт степеней вершин
    degrees = [sum(row) for row in matrix]
    odd_vertices = [i + 1 for i, deg in enumerate(degrees) if deg % 2 != 0]
    
    # Подсчёт количества рёбер (для неориентированного графа сумма степеней / 2)
    total_edges = sum(degrees) // 2
    if total_edges == 0:
        return {
            "exists": False,
            "message": "В графе нет рёбер. Эйлеров маршрут не существует."
        }

    # 2. Проверка связности (проверяем только вершины со степенью > 0)
    visited = [False] * n
    # Находим первую вершину с рёбрами для старта DFS
    start_dfs = next((i for i, deg in enumerate(degrees) if deg > 0), None)
    
    if start_dfs is not None:
        def dfs(v):
            visited[v] = True
            for to, connected in enumerate(matrix[v]):
                if connected and not visited[to]:
                    dfs(to)
        dfs(start_dfs)
        
    # Если есть вершина с рёбрами, которую мы не посетили — граф несвязен
    for i in range(n):
        if degrees[i] > 0 and not visited[i]:
            return {
                "exists": False,
                "message": "Граф несвязен (компоненты с рёбрами изолированы друг от друга)."
            }

    # 3. Валидация условий Эйлера
    # Цикл: все степени чётные. Цепь: ровно 2 нечётные вершины.
    if len(odd_vertices) == 0:
        graph_type = "Эйлеров цикл"
        # Стартовать можно с любой вершины, где есть рёбра
        start_vertex = start_dfs
    elif len(odd_vertices) == 2:
        graph_type = "Эйлерова цепь"
        # Стартовать обязаны из одной из нечётных вершин
        start_vertex = odd_vertices[0] - 1
    else:
        return {
            "exists": False,
            "message": f"Найдено нечётное количество вершин с нечётной степенью ({len(odd_vertices)}). Маршрут невозможен.",
            "odd_vertices": odd_vertices
        }

    # 4. Поиск маршрута (Алгоритм Иерхольцера)
    # Копируем матрицу, так как в процессе мы будем стирать рёбра
    temp_matrix = [row[:] for row in matrix]
    stack = [start_vertex]
    path = []

    while stack:
        v = stack[-1]
        # Ищем первое доступное ребро из текущей вершины
        has_edge = False
        for to in range(n):
            if temp_matrix[v][to] > 0:
                # Удаляем ребро в обоих направлениях
                temp_matrix[v][to] -= 1
                temp_matrix[to][v] -= 1
                stack.append(to)
                has_edge = True
                break
        if not has_edge:
            # Если идти некуда, выталкиваем вершину в финальный путь
            path.append(stack.pop() + 1) # Переводим в 1-индексацию для пользователя

    # Разворачиваем путь, так как сборка шла с конца
    path.reverse()

    # 5. Построение матрицы достижимости (Транзитивное замыкание по алгоритму Уоршелла)
    closure = [row[:] for row in matrix]
    # Диагональ матрицы достижимости всегда 1 (вершина достижима из самой себя)
    for i in range(n):
        closure[i][i] = 1
        
    for k in range(n):
        for i in range(n):
            for j in range(n):
                closure[i][j] = closure[i][j] or (closure[i][k] and closure[k][j])

    # 6. Генерация изображения графа через NetworkX
    img_base64 = ""
    try:
        plt.figure(figsize=(5, 4))
        G = nx.Graph()
        
        # Добавляем только вершины, у которых есть связи, чтобы не перегружать экран
        for i in range(n):
            G.add_node(i + 1)
            
        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] > 0:
                    G.add_edge(i + 1, j + 1)

        pos = nx.spring_layout(G, seed=42)
        
        # Отрисовка
        nx.draw_networkx_nodes(G, pos, node_color='#3498db', node_size=500)
        nx.draw_networkx_labels(G, pos, font_color='white', font_weight='bold')
        nx.draw_networkx_edges(G, pos, width=2, edge_color='#bdc3c7')
        
        plt.axis('off')
        plt.tight_layout()

        # Сохраняем в буфер памяти
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
    except Exception as e:
        print(f"Ошибка визуализации: {e}")

    # Возвращаем полный набор данных, который затребовал наш euler.js
    return {
        "exists": True,
        "type": graph_type,
        "start_vertex": start_vertex + 1,
        "odd_vertices": odd_vertices,
        "degrees": degrees,
        "path": path,
        "closure": closure,
        "image": img_base64
    }