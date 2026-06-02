"""
Валидация входных данных для задачи поиска максимальных клик.
Каждая функция возвращает пару (значение, ошибка) — если ошибки нет, второй элемент None.
"""


def validate_n(n_str):
    """Проверяет количество вершин: целое число от 3 до 12."""
    if n_str is None or str(n_str).strip() == '':
        return None, 'Введите количество вершин.'
    try:
        n = int(n_str)
    except (ValueError, TypeError):
        return None, 'Количество вершин должно быть целым числом.'
    if n < 3:
        return None, 'Количество вершин должно быть не менее 3.'
    if n > 12:
        return None, 'Количество вершин не должно превышать 12.'
    return n, None


def validate_matrix_cell(value_str):
    """Проверяет одну ячейку матрицы: допустимы только 0 и 1. Пустая ячейка = 0."""
    if value_str is None or str(value_str).strip() == '':
        return 0, None
    try:
        v = int(value_str)
    except (ValueError, TypeError):
        return None, 'Ячейка матрицы должна содержать 0 или 1.'
    if v not in (0, 1):
        return None, 'Ячейка матрицы должна содержать 0 или 1.'
    return v, None


def validate_density(density_str):
    """Проверяет плотность рёбер: целое число от 1 до 100."""
    if density_str is None or str(density_str).strip() == '':
        return None, 'Введите плотность рёбер.'
    try:
        d = int(density_str)
    except (ValueError, TypeError):
        return None, 'Плотность должна быть целым числом от 1 до 100.'
    if d < 1 or d > 100:
        return None, 'Плотность должна быть от 1 до 100.'
    return d, None


def validate_matrix(form, n):
    """
    Считывает верхний треугольник матрицы из данных формы (поля m_i_j),
    зеркалит его и строит полную симметричную матрицу n×n.
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


def validate_txt_file(file_content):
    """
    Парсит содержимое TXT-файла с матрицей смежности.
    Формат: каждая строка — строка матрицы, числа разделены пробелами.
    Проверяет: размер (3–12), только 0/1, нулевая диагональ, симметричность.
    """
    # Убираем пустые строки
    lines = [l.strip() for l in file_content.strip().splitlines() if l.strip()]

    if not lines:
        return None, 'Файл пустой.'

    n = len(lines)

    if n < 3:
        return None, 'Матрица должна быть не менее 3×3.'
    if n > 12:
        return None, f'Матрица слишком большая: {n} строк. Максимум 12×12.'

    # Парсим строки и проверяем значения
    matrix = []
    for idx, line in enumerate(lines):
        parts = line.split()
        if len(parts) != n:
            return None, f'Строка {idx + 1}: ожидается {n} чисел, найдено {len(parts)}.'
        row = []
        for val in parts:
            if val not in ('0', '1'):
                return None, f'Строка {idx + 1}: недопустимое значение «{val}». Только 0 или 1.'
            row.append(int(val))
        matrix.append(row)

    # Проверяем диагональ и симметричность
    for i in range(n):
        if matrix[i][i] != 0:
            return None, f'Диагональный элемент [{i+1}][{i+1}] должен быть 0.'
        for j in range(i + 1, n):
            if matrix[i][j] != matrix[j][i]:
                return None, f'Матрица не симметрична: [{i+1}][{j+1}] ≠ [{j+1}][{i+1}].'

    return matrix, None