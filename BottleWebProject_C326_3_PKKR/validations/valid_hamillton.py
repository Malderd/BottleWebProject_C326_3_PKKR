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
                errors[f'{i}_{j}'] = \
                    'Допустимы только значения 0 или 1.'
                return errors

    for i in range(n):

        if matrix[i][i] != '0':
            errors[f'{i}_{i}'] = \
                'На главной диагонали должны быть нули.'
            return errors

    for i in range(n):

        for j in range(n):

            if matrix[i][j] != matrix[j][i]:
                errors['matrix'] = \
                    'Матрица должна быть симметричной.'
                return errors

    return errors
