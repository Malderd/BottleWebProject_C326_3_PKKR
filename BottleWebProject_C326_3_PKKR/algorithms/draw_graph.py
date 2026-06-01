import io
import uuid
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import networkx as nx


def draw_graph(matrix):

    graph = nx.Graph()

    n = len(matrix)

    for i in range(n):
        graph.add_node(i)

    for i in range(n):
        for j in range(i + 1, n):

            if matrix[i][j] == 1:
                graph.add_edge(i, j)

    plt.figure(figsize=(8, 6))

    pos = nx.spring_layout(
        graph,
        seed=42
    )

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_size=1000,
        font_size=12
    )

    filename = f"graph_{uuid.uuid4().hex}.png"

    filepath = f"static/images/{filename}"

    plt.savefig(
        filepath,
        bbox_inches='tight'
    )

    plt.close()

    return f"/static/images/{filename}"
