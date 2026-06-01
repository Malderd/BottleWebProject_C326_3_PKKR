"""
Алгоритм поиска максимальных клик + визуализация графа через matplotlib/networkx.
"""
import io
import base64
import math
import random

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx


# ───────────────────────────────────────────────
#  Алгоритм поиска клик (битовые маски)
# ───────────────────────────────────────────────

def is_clique(subset, matrix):
    """
    Проверяет, является ли подмножество вершин кликой.
    subset — список вершин (нумерация с 1).
    """
    n = len(subset)
    for i in range(n):
        for j in range(i + 1, n):
            v1 = subset[i] - 1
            v2 = subset[j] - 1
            if matrix[v1][v2] == 0:
                return False
    return True


def find_all_cliques(matrix, n):
    """
    Перебирает все подмножества вершин через битовые маски.
    Возвращает список клик размером >= 3.
    """
    vertices = list(range(1, n + 1))
    total = 1 << n
    cliques = []

    for mask in range(1, total):
        subset = [vertices[j] for j in range(n) if mask & (1 << j)]
        if len(subset) >= 3 and is_clique(subset, matrix):
            cliques.append(subset)

    return cliques


def find_maximal_cliques(all_cliques):
    """
    Из всех клик оставляет только максимальные —
    те, которые не являются подмножеством другой клики.
    """
    maximal = []
    for clique in all_cliques:
        clique_set = set(clique)
        dominated = False
        for other in all_cliques:
            if set(other) != clique_set and clique_set.issubset(set(other)):
                dominated = True
                break
        if not dominated:
            maximal.append(clique)
    return maximal


# ───────────────────────────────────────────────
#  Визуализация
# ───────────────────────────────────────────────

CLIQUE_COLORS = [
    '#e53935', '#fb8c00', '#fdd835', '#43a047',
    '#039be5', '#8e24aa', '#f06292', '#00acc1',
]


def _circle_positions(n):
    pos = {}
    for i in range(n):
        angle = 2 * math.pi * i / n - math.pi / 2
        pos[i + 1] = (math.cos(angle), math.sin(angle))
    return pos


def render_graph(matrix, n, maximal_cliques):
    try:
        G = nx.Graph()
        G.add_nodes_from(range(1, n + 1))

        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] == 1:
                    G.add_edge(i + 1, j + 1)

        pos = _circle_positions(n)

        node_colors = {}
        for idx, clique in enumerate(maximal_cliques):
            color = CLIQUE_COLORS[idx % len(CLIQUE_COLORS)]
            for v in clique:
                if v not in node_colors:
                    node_colors[v] = color

        colors = [node_colors.get(v, '#b0bec5') for v in G.nodes()]

        fig, ax = plt.subplots(figsize=(7, 4.5), facecolor='#1e1e1e')
        ax.set_facecolor('#1e1e1e')

        if G.number_of_edges() > 0:
            nx.draw_networkx_edges(G, pos, ax=ax, edge_color='#78909c', width=1.8, alpha=0.7)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colors, node_size=500,
                               linewidths=1.5, edgecolors='white')
        nx.draw_networkx_labels(G, pos, ax=ax, font_color='white',
                                font_size=11, font_weight='bold')

        ax.axis('off')
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=120,
                    facecolor=fig.get_facecolor(), bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')
    except Exception:
        plt.close('all')
        raise


# ───────────────────────────────────────────────
#  Генерация случайного графа
# ───────────────────────────────────────────────

def generate_random_matrix(n, density):
    """
    Генерирует случайную симметричную матрицу смежности n×n.
    density — плотность рёбер в процентах (1–100).
    """
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.randint(1, 100) <= density:
                matrix[i][j] = 1
                matrix[j][i] = 1
    return matrix


# ───────────────────────────────────────────────
#  Точка входа для routes.py
# ───────────────────────────────────────────────

def solve_cliques(matrix, n):
    all_cliques = find_all_cliques(matrix, n)
    maximal = find_maximal_cliques(all_cliques)
    graph_png = render_graph(matrix, n, maximal)

    return {
        'all_cliques': all_cliques,
        'maximal_cliques': maximal,
        'graph_png': graph_png,
    }