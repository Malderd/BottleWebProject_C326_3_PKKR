def find_hamiltonian(adj):
    n = len(adj)

    path = [0]
    visited = [False] * n
    visited[0] = True

    def backtrack():

        if len(path) == n:

            if adj[path[-1]][0]:
                return "cycle", path.copy()

            return "chain", path.copy()

        current = path[-1]

        for neighbor in range(n):

            if adj[current][neighbor] and not visited[neighbor]:

                path.append(neighbor)
                visited[neighbor] = True

                result = backtrack()

                if result is not None:
                    return result

                path.pop()
                visited[neighbor] = False

        return None

    return backtrack()
