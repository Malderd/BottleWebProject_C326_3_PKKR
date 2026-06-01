import io
import uuid
import matplotlib
from datetime import datetime

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import networkx as nx


def build_graph(matrix):
    graph = nx.Graph()
    n = len(matrix)

    for i in range(n):
        graph.add_node(i)

    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] == 1:
                graph.add_edge(i, j)

    pos = nx.spring_layout(graph, seed=42)

    graph1 = plt.figure(figsize=(8, 6))
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_size=1000,
        font_size=12
    )

    return graph1


def draw_graph(matrix, save=False):
    graph = build_graph(matrix)

    if not save:
        import io
        import base64

        buf = io.BytesIO()
        graph.savefig(buf, format='png', bbox_inches='tight')
        plt.close(graph)

        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')

        return f"data:image/png;base64,{img_base64}"

    filename = datetime.now().strftime('graph_%Y%m%d_%H%M%S.png')
    filepath = f"static/images/{filename}"

    graph.savefig(filepath, bbox_inches='tight')
    plt.close(graph)

    return f"/static/images/{filename}"