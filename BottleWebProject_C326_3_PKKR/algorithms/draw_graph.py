import io
import os
import zipfile
import tempfile
import matplotlib
import base64
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


def draw_graph(matrix):
    graph = build_graph(matrix)

    buf = io.BytesIO()
    graph.savefig(buf, format='png', bbox_inches='tight')
    plt.close(graph)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return f"data:image/png;base64,{img_base64}"


def save_graph_archive(matrix):
    temp_dir = tempfile.mkdtemp()

    png_path = os.path.join(temp_dir,'graph.png')
    txt_path = os.path.join(temp_dir,'matrix.txt')
    zip_name = datetime.now().strftime('graph_%Y%m%d_%H%M%S.zip')
    zip_path = os.path.join(temp_dir,zip_name)
    graph = build_graph(matrix)

    graph.savefig(png_path,bbox_inches='tight')

    plt.close(graph)

    with open(txt_path, 'w',
             encoding='utf-8') as f:

        for row in matrix:
            f.write(' '.join(map(str, row)) + '\n')

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.write(png_path, arcname='graph.png')
        archive.write(txt_path, arcname='matrix.txt')

    return zip_name, temp_dir