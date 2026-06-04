def valid_hamillton(matrix):

    errors = {}

    n = len(matrix)

    if n < 3:
        errors['matrix'] = 'Количество вершин не должно быть больше 3.'
        return errors

    if n > 15:
        errors['matrix'] = 'Количество вершин не должно превышать 15.'
        return errors

    for i in range(n):

        for j in range(n):

            value = matrix[i][j]

            if value == '':
                errors[f'{i}_{j}'] = 'Заполните ячейки.'
                return errors

            if value not in ('0', '1'):
                errors[f'{i}_{j}'] = 'Допустимы только значения 0 или 1.'
                return errors

    for i in range(n):

        if matrix[i][i] != '0':
            errors[f'{i}_{i}'] = 'На главной диагонали должны быть нули.'
            return errors

    for i in range(n):

        for j in range(n):

            if matrix[i][j] != matrix[j][i]:
                errors['matrix'] = 'Матрица должна быть симметричной.'
                return errors

    return errors

def validate_txt_file(text):

    rows = [
        row.strip().split()
        for row in text.strip().splitlines()
        if row.strip()
    ]

    n = len(rows)

    if n < 3 or n > 15:
        return None, 'Размер матрицы должен быть от 3 до 15.'

    for row in rows:

        if len(row) != n:
            return None, 'Матрица должна быть квадратной.'

    for i in range(n):

        for j in range(n):

            if rows[i][j] not in ('0', '1'):
                return None, 'Допустимы только значения 0 или 1.'

    for i in range(n):

        if rows[i][i] != '0':
            return None, 'На главной диагонали должны быть нули.'

    for i in range(n):

        for j in range(n):

            if rows[i][j] != rows[j][i]:
                return None, 'Матрица должна быть симметричной.'

    matrix = [
        [int(cell) for cell in row]
        for row in rows
    ]

    return matrix, None
