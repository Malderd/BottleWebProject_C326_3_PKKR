"""
Роут /clique_save — принимает данные матрицы, пересчитывает клики,
собирает ZIP-архив (graph.png + results.txt) и отдаёт на скачивание.
Добавьте в ваш routes.py.
"""
import io
import zipfile
from bottle import route, request, response
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'algorithms'))

from algorithms.clique_detection import solve_cliques
from validations.valid_clique import validate_n, validate_matrix


@route('/clique_save', method='POST')
def clique_save():
    # 1. Валидируем N и матрицу (те же проверки что и при построении)
    n, n_err = validate_n(request.forms.get('n'))
    if n_err:
        return f'Ошибка: {n_err}'

    matrix, matrix_errors = validate_matrix(request.forms, n)
    if matrix_errors:
        return 'Ошибка в данных матрицы.'

    # 2. Пересчитываем клики и граф
    result = solve_cliques(matrix, n)

    # 3. Формируем results.txt
    lines = []
    lines.append(f'Количество вершин: {n}')
    lines.append('')

    # Матрица смежности
    lines.append('Матрица смежности:')
    header = '   ' + '  '.join(str(j + 1).rjust(2) for j in range(n))
    lines.append(header)
    for i in range(n):
        row = str(i + 1).rjust(2) + ' ' + '  '.join(str(matrix[i][j]).rjust(2) for j in range(n))
        lines.append(row)
    lines.append('')

    # Найденные клики
    cliques = result['maximal_cliques']
    if cliques:
        lines.append(f'Максимальных клик найдено: {len(cliques)}')
        for idx, clique in enumerate(cliques):
            lines.append(f'{idx + 1}) {{{", ".join(map(str, clique))}}}')
    else:
        lines.append('Максимальных клик не найдено.')

    txt_bytes = '\n'.join(lines).encode('utf-8')

    # 4. Декодируем PNG из base64
    import base64
    png_bytes = base64.b64decode(result['graph_png'])

    # 5. Собираем ZIP в памяти
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('graph.png', png_bytes)
        zf.writestr('results.txt', txt_bytes)
    zip_buf.seek(0)

    # 6. Отдаём архив браузеру
    response.content_type = 'application/zip'
    response.headers['Content-Disposition'] = 'attachment; filename="clique_results.zip"'
    return zip_buf.read()