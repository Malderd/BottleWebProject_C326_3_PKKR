"""
Валидация входных данных для задачи поиска максимальных клик.
"""


def validate_n(n_str):
    """
    Проверяет корректность введённого количества вершин.
    Возвращает (int или None, str или None) — (значение, сообщение об ошибке).
    """
    if n_str is None or str(n_str).strip() == '':
        return None, 'Введите количество вершин.'

    try:
        n = int(n_str)
    except (ValueError, TypeError):
        return None, 'Количество вершин должно быть целым числом.'

    if n < 3:
        return None, 'Количество вершин должно быть не менее 3.'

    if n > 16:
        return None, 'Количество вершин не должно превышать 16.'

    return n, None


def validate_matrix_cell(value_str):
    """
    Проверяет одну ячейку матрицы смежности.
    Допустимые значения: 0 или 1.
    Возвращает (int или None, str или None).
    """
    if value_str is None or str(value_str).strip() == '':
        return 0, None  # пустая ячейка трактуется как 0

    try:
        v = int(value_str)
    except (ValueError, TypeError):
        return None, 'Ячейка матрицы должна содержать 0 или 1.'

    if v not in (0, 1):
        return None, 'Ячейка матрицы должна содержать 0 или 1.'

    return v, None


def validate_matrix(form, n):
    """
    Считывает верхний треугольник матрицы из данных формы,
    строит полную симметричную матрицу n×n.

    Ожидает поля с именами вида 'm_i_j' (i < j, индексы от 0).

    Возвращает (matrix или None, errors dict).
    """
    matrix = [[0] * n for _ in range(n)]
    errors = {}

    for i in range(n):
        for j in range(i + 1, n):
            key = f'm_{i}_{j}'
            raw = form.get(key, '0')
            value, err = validate_matrix_cell(raw)
            if err:
                errors[key] = err
            else:
                matrix[i][j] = value
                matrix[j][i] = value  # симметрия

    return (None if errors else matrix), errors