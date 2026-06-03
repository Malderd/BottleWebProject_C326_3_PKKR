import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(matrix, components, filename):
    G = nx.DiGraph()

    n = len(matrix)

    for i in range(n):
        G.add_node(i)

    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1:
                G.add_edge(i, j)

    pos = nx.circular_layout(G)

    component_colors = [
        "#e74c3c",  # красный
        "#3498db",  # синий
        "#2ecc71",  # зелёный
        "#f1c40f",  # жёлтый
        "#9b59b6",  # фиолетовый
        "#1abc9c",  # бирюзовый
        "#e67e22",  # оранжевый
        "#5d6d7e",  # черничный
        "#ff6b6b",  # светло-красный
        "#74b9ff",  # светло-синий
        "#55efc4",  # мятный
        "#fdcb6e",  # светло-жёлтый
        "#a29bfe",  # светло-фиолетовый
        "#fab1a0"   # персиковый
    ]

    colors = ["lightgray"] * n
    vertex_colors = {}

    for component_index, component in enumerate(components):

        color = component_colors[
            component_index % len(component_colors)
        ]

        for vertex in component:
            colors[vertex] = color
            vertex_colors[vertex] = color

    edge_colors = []
    edge_widths = []

    for u, v in G.edges():

        if vertex_colors.get(u) == vertex_colors.get(v):
            edge_colors.append(vertex_colors[u])
            edge_widths.append(3)
        else:
            edge_colors.append("#4a4a4a")
            edge_widths.append(1.5)

    plt.figure(figsize=(16, 12))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2500,
        node_color=colors,
        edge_color=edge_colors,
        width=edge_widths,
        arrows=True,
        font_size=18,
        arrowsize = 20
    )

    plt.savefig(
        filename,
        bbox_inches="tight"
    )

    plt.close()