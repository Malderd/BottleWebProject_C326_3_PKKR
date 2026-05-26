def validate_matrix(matrix):

    errors = {}

    n = len(matrix)

    if n == 0:
        errors['matrix'] = 'Матрица пуста.'
        return errors

    if n > 15:
        errors['matrix'] = 'Количество вершин не должно превышать 15.'
        return errors

    for i in range(n):

        if len(matrix[i]) != n:
            errors['matrix'] = 'Матрица должна быть квадратной.'
            return errors

        for j in range(n):

            value = matrix[i][j]

            if value not in (0, 1):
                errors[f'cell_{i}_{j}'] = \
                    'Допустимы только значения 0 или 1.'

    for i in range(n):

        if matrix[i][i] != 0:
            errors[f'cell_{i}_{i}'] = \
                'На главной диагонали должны быть нули.'

    for i in range(n):

        for j in range(n):

            if matrix[i][j] != matrix[j][i]:
                errors['matrix'] = \
                    'Матрица должна быть симметричной.'
                return errors

    return errors
