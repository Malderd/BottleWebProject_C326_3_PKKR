import re
def validate_matrix(matrix):
    n = len(matrix)
    errors = []

    isolated = []
    for i in range(n):

        # 1. петли
        if matrix[i][i] == 1:
            errors.append(f"Вершина {i}: есть петля")

        # 2. изоляция
        out_deg = sum(matrix[i])
        in_deg = sum(matrix[j][i] for j in range(n))

        if out_deg == 0 and in_deg == 0:
            isolated.append(i)

        # 3. антисимметрия (взаимные ребра)
        for j in range(i + 1, n):

            if matrix[i][j] == 1 and matrix[j][i] == 1:
                errors.append(f"Вершины {i} ↔ {j}: взаимные ребра (нарушение антисимметрии)")

    if isolated:
        errors.append(f"Изолированные вершины: {isolated}")

    return errors

def validate_matrix_text(text: str):

    lines = text.strip().splitlines()

    n = len(lines)
    
    if n == 0:
        return False, "Файл пустой"
    
    matrix = []
    for i, line in enumerate(lines):
        if not re.match(r"^[0 1]{5,27}$", line):
            return False, "Данные в файле не в корректном формате"
        parts = line.strip().split()
        if len(parts) != n:
            return False, f"Строка {i+1} имеет длину {len(parts)}, ожидалось {n}"
        row = []
        for j, p in enumerate(parts):
            if p not in ('0', '1'):
                return False, f"Элемент ({i+1},{j+1}) = '{p}' не 0 или 1"
            row.append(int(p))
        matrix.append(row)
    
    return True, matrix