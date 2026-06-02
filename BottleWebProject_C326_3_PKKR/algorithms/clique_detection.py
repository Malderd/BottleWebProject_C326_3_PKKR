"""
Алгоритм поиска максимальных клик + визуализация графа через matplotlib/networkx.
"""
# Стандартные библиотеки для работы с байтами и кодировками
import io
import base64
import math
import random

# Настройка matplotlib: Agg — рендер в картинку без GUI (для сервера)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
# NetworkX — работа с графами
import networkx as nx

#  Алгоритм поиска клик (битовые маски)
def is_clique(subset, matrix):
    """
    Проверяет, является ли подмножество вершин кликой.
    subset — список вершин (нумерация с 1).
    """
    n = len(subset)
    # Проверяем все пары вершин в подмножестве
    for i in range(n):
        for j in range(i + 1, n):
            # Переводим нумерацию с 1 на 0 для доступа к матрице
            v1 = subset[i] - 1
            v2 = subset[j] - 1
            # Если между вершинами нет ребра — это не клика
            if matrix[v1][v2] == 0:
                return False
    return True

# Нахождение сообществ
def find_all_cliques(matrix, n):
    vertices = list(range(1, n + 1))
    total = 1 << n # количество подмножеств 2^n

    cliques = []

    for mask in range(1, total):
        subset = [vertices[j] for j in range(n) if mask & (1 << j)]

        if len(subset) >= 3 and is_clique(subset, matrix):
            cliques.append(subset)

    truncated = len(cliques) > 100
    return cliques, truncated

#  Визуализация

# Палитра цветов для раскраски разных клик
CLIQUE_COLORS = [
    '#e53935', '#fb8c00', '#fdd835', '#43a047',
    '#039be5', '#8e24aa', '#f06292', '#00acc1',
]

def _circle_positions(n):
    """
    Расставляет вершины по кругу для красивой визуализации.
    Возвращает dict {вершина: (x, y)}.
    """
    pos = {}
    for i in range(n):
        # Угол для равномерного распределения по окружности
        angle = 2 * math.pi * i / n - math.pi / 2
        pos[i + 1] = (math.cos(angle), math.sin(angle))
    return pos

def render_graph(matrix, n, maximal_cliques):
    """
    Рисует граф с раскрашенными кликами, возвращает base64-картинку.
    """
    try:
        # Создаём граф NetworkX
        G = nx.Graph()
        G.add_nodes_from(range(1, n + 1))

        # Добавляем рёбра из матрицы смежности (только верхний треугольник)
        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] == 1:
                    G.add_edge(i + 1, j + 1)

        # Позиции вершин — по кругу
        pos = _circle_positions(n)

        # Раскрашиваем вершины: каждая клика получает свой цвет
        node_colors = {}
        for idx, clique in enumerate(maximal_cliques):
            color = CLIQUE_COLORS[idx % len(CLIQUE_COLORS)]  # циклически берём цвет
            for v in clique:
                # Красим только если вершина ещё не окрашена
                if v not in node_colors:
                    node_colors[v] = color

        # Формируем список цветов для всех вершин графа
        colors = [node_colors.get(v, '#b0bec5') for v in G.nodes()]

        # Создаём фигуру с тёмным фоном (под дизайн сайта)
        fig, ax = plt.subplots(figsize=(7, 4.5), facecolor='#1e1e1e')
        ax.set_facecolor('#1e1e1e')

        # Рисуем рёбра, если они есть
        if G.number_of_edges() > 0:
            nx.draw_networkx_edges(G, pos, ax=ax, edge_color='#78909c', width=1.8, alpha=0.7)
        
        # Рисуем узлы с цветами
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colors, node_size=500,
                               linewidths=1.5, edgecolors='white')
        # Подписи вершин — белые, жирные
        nx.draw_networkx_labels(G, pos, ax=ax, font_color='white',
                                font_size=11, font_weight='bold')

        # Убираем оси и лишние отступы
        ax.axis('off')
        plt.tight_layout()

        # Сохраняем в буфер памяти вместо файла
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=120,
                    facecolor=fig.get_facecolor(), bbox_inches='tight')
        plt.close(fig)  # Освобождаем память
        
        # Готовим данные для передачи в HTML (base64)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')
    except Exception:
        # На всякий случай чистим фигуру при ошибке
        plt.close('all')
        raise

#  Генерация случайного графа
def generate_random_matrix(n, density):
    """
    Генерирует случайную симметричную матрицу смежности n×n.
    density — плотность рёбер в процентах (1–100).
    """
    # Создаём нулевую матрицу n×n
    matrix = [[0] * n for _ in range(n)]
    # Заполняем верхний треугольник, нижний — зеркально
    for i in range(n):
        for j in range(i + 1, n):
            # Ребро добавляется с вероятностью density%
            if random.randint(1, 100) <= density:
                matrix[i][j] = 1
                matrix[j][i] = 1
    return matrix

#  Точка входа для routes.py
def solve_cliques(matrix, n):
    all_cliques, truncated = find_all_cliques(matrix, n)

    graph_png = render_graph(matrix, n, all_cliques)

    return {
        'all_cliques': all_cliques,
        'truncated': truncated,
        'graph_png': graph_png,
    }