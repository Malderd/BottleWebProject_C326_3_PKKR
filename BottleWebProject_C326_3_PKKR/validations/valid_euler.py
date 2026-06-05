def validation_euler(matrix):
    """
    Модуль валидации матрицы смежности для поиска Эйлерова маршрута.
    Возвращает кортеж: (is_valid, error_response)
    """
    if not matrix or not isinstance(matrix, list):
        return False, {"exists": False, "message": "Матрица не передана или имеет неверный формат."}

    n = len(matrix)
    if n == 0:
        return False, {"exists": False, "message": "Матрица пуста. Граф не содержит вершин."}

    # 1. Проверка на квадратную матрицу и корректность значений
    for i in range(n):
        if not isinstance(matrix[i], list) or len(matrix[i]) != n:
            return False, {
                "exists": False, 
                "message": f"Ошибка структуры: строка {i + 1} должна содержать ровно {n} элементов."
            }
        
        for j in range(n):
            if i == j and matrix[i][j] != 0:
                return False, {
                    "exists": False,
                    "message": f"Обнаружена петля у вершины {i + 1}. Алгоритм обрабатывает только простые графы без петель."
                }
            if matrix[i][j] not in (0, 1):
                return False, {
                    "exists": False,
                    "message": f"Недопустимое значение ({matrix[i][j]}) в ячейке [{i+1}][{j+1}]. Разрешены только 0 и 1."
                }
            if matrix[i][j] != matrix[j][i]:
                return False, {
                    "exists": False,
                    "message": f"Матрица несимметрична относительно главной диагонали между вершинами {i+1} и {j+1}. Граф должен быть неориентированным."
                }
    active_vertices = {i for i in range(n) if sum(matrix[i]) > 0}
    
    if active_vertices:
        # Стартуем BFS с любой активной вершины
        start_vertex = next(iter(active_vertices))
        visited = set()
        queue = [start_vertex]
        visited.add(start_vertex)
        
        while queue:
            current = queue.pop(0)
            for neighbor in range(n):
                if matrix[current][neighbor] == 1 and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        # Если посетили не все активные вершины — граф несвязный
        if not active_vertices.issubset(visited):
            return False, {
                "exists": False,
                "message": "Граф несвязен (содержит несколько изолированных компонент с ребрами). Эйлеров маршрут невозможен."
            }
    # Если структура матрицы верна — пропускаем к решению!
    return True, None

def validation_random_params(n_param, density_param):
    """
    Валидирует параметры для случайной генерации графа.
    Возвращает кортеж: (is_valid, n_int, density_int, error_response)
    """
    try:
        n = int(n_param)
        density = int(density_param)
    except (ValueError, TypeError):
        return False, None, None, {"error": "Параметры должны быть целыми числами."}

    if not (2 <= n <= 20):
        return False, None, None, {"error": "Количество вершин N должно быть от 2 до 20."}
        
    if not (1 <= density <= 100):
        return False, None, None, {"error": "Плотность должна быть в диапазоне от 1 до 100%."}

    return True, n, density, None

def validation_and_parse_file(file_item):
    """
    Валидирует наличие файла, читает его содержимое и проверяет базовую структуру матрицы.
    Возвращает кортеж: (is_valid, matrix, error_response)
    """
    if not file_item:
        return False, None, {"error": "Файл не передан."}

    try:
        content = file_item.file.read().decode("utf-8")
        matrix = []

        for idx, line in enumerate(content.strip().splitlines()):
            line = line.strip()
            if not line:
                continue
            
            try:
                row = list(map(int, line.split()))
            except ValueError:
                return False, None, {"error": f"Ошибка в строке {idx + 1}: файл должен содержать только числа."}
                
            matrix.append(row)

        n = len(matrix)
        if n == 0:
            return False, None, {"error": "Файл пуст или содержит только пустые строки."}

        for idx, row in enumerate(matrix):
            if len(row) != n:
                return False, None, {
                    "error": f"Строка {idx + 1} содержит {len(row)} элементов. Ожидалось {n} (матрица должна быть квадратной)."
                }

        return True, matrix, None

    except Exception as e:
        return False, None, {"error": f"Не удалось прочитать файл: {str(e)}"}