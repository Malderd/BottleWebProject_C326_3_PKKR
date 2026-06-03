def dfs1(vertex, matrix, visited, order):

    visited[vertex] = True

    for i in range(len(matrix)):

        if matrix[vertex][i] == 1 and not visited[i]:
            dfs1(i, matrix, visited, order)

    order.append(vertex)


def dfs2(vertex, transpose, visited, component):

    visited[vertex] = True
    component.append(vertex)

    for i in range(len(transpose)):

        if transpose[vertex][i] == 1 and not visited[i]:
            dfs2(i, transpose, visited, component)


def find_components(matrix):

    n = len(matrix)

    visited = [False] * n
    order = []

    # Первый DFS
    for vertex in range(n):

        if not visited[vertex]:
            dfs1(vertex, matrix, visited, order)

    # Транспонирование графа
    transpose = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            transpose[j][i] = matrix[i][j]

    # Второй DFS
    visited = [False] * n

    components = []

    while order:

        vertex = order.pop()

        if not visited[vertex]:

            component = []

            dfs2(vertex, transpose, visited, component)

            components.append(component)

    return components
