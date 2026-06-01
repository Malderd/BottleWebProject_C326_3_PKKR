"""
Routes and views for the bottle application.
"""
from bottle import route, view, request, template, response
from datetime import datetime
import json, io, zipfile, base64

from hamillton_graph import hamillton_graph, valid_hamillton
from algorithms.clique_detection import solve_cliques, generate_random_matrix
from validations.valid_clique import validate_n, validate_matrix, validate_density, validate_txt_file


def _load_theory():
    with open('./static/data/cliques_theory.json', encoding='utf-8') as f:
        return json.load(f)


@route('/')
@route('/home')
@view('index')
def home():
    return dict(request=request)


@route('/about')
@view('about')
def about():
    return dict(title='About', request=request)


@route('/euler_graph')
@view('euler_graph')
def euler_grap():
    return dict(title='Euler graph', request=request)


@route('/hamillton_graph')
@view('hamillton_graph')
def hamillton_graph():
    return template('hamillton_graph.tpl', title='Hamilltom graph',
                    result=None, success=False, errors={}, form_data={}, request=request)


@route('/decide_hamillton_graph', method='POST')
@view('hamillton_graph')
def decide_hamillton_graph():
    return template('hamillton_graph.tpl', title='Hamilltom graph',
                    result=None, success=True, errors={}, form_data=request.forms, request=request)


@route('/kosarayu_algorithm')
@view('kosarayu_algorithm')
def kosarayu_algorithm():
    return dict(title='Kosarayu_algorithm', request=request)


# ─── Клики: GET ──────────────────────────────────────────────────────────────

@route('/clique_detection')
def clique_detection():
    tab = request.query.get('tab', 'manual')
    theory = _load_theory()
    n = None
    matrix = None
    errors = {}

    if tab == 'random':
        n_raw       = request.query.get('n_size', '')
        density_raw = request.query.get('density', '')
        if n_raw and density_raw:
            n, n_err = validate_n(n_raw)
            if n_err:
                errors['n'] = n_err
            density, d_err = validate_density(density_raw)
            if d_err:
                errors['density'] = d_err
            if not errors:
                matrix = generate_random_matrix(n, density)

    return template('clique_detection.tpl', title='Clique detection',
                    request=request, theory=theory, tab=tab,
                    n=n, matrix=matrix, result=None, errors=errors,
                    file_name=None)


# ─── Клики: POST (построить граф — ручной и случайный) ───────────────────────

@route('/clique_detection', method='POST')
def clique_detection_post():
    tab = request.forms.get('tab', 'manual')
    theory = _load_theory()

    n, n_err = validate_n(request.forms.get('n'))
    if n_err:
        return template('clique_detection.tpl', title='Clique detection',
                        request=request, theory=theory, tab=tab,
                        n=None, matrix=None, result=None, errors={'n': n_err},
                        file_name=None)

    matrix, matrix_errors = validate_matrix(request.forms, n)
    if matrix_errors:
        return template('clique_detection.tpl', title='Clique detection',
                        request=request, theory=theory, tab=tab,
                        n=n, matrix=None, result=None, errors=matrix_errors,
                        file_name=None)

    try:
        result = solve_cliques(matrix, n)
    except Exception as e:
        return template('clique_detection.tpl', title='Clique detection',
                        request=request, theory=theory, tab=tab,
                        n=n, matrix=matrix, result=None,
                        errors={'solve': f'Ошибка при построении графа: {e}'},
                        file_name=None)
    return template('clique_detection.tpl', title='Clique detection',
                    request=request, theory=theory, tab=tab,
                    n=n, matrix=matrix, result=result, errors={},
                    file_name=None)


# ─── Клики: POST (загрузка TXT-файла) ────────────────────────────────────────

@route('/clique_detection_file', method='POST')
def clique_detection_file():
    theory = _load_theory()
    upload = request.files.get('matrix_file')

    if not upload or not upload.filename:
        return template('clique_detection.tpl', title='Clique detection',
                        request=request, theory=theory, tab='file',
                        n=None, matrix=None, result=None,
                        errors={'file': 'Выберите файл.'}, file_name=None)

    filename = upload.filename
    if isinstance(filename, bytes):
        filename = filename.decode('utf-8', errors='replace')
    if not filename.lower().endswith('.txt'):
        return template('clique_detection.tpl', title='Clique detection',
                        request=request, theory=theory, tab='file',
                        n=None, matrix=None, result=None,
                        errors={'file': 'Допускается только .txt файл.'}, file_name=None)

    content = upload.file.read().decode('utf-8', errors='replace')
    matrix, err = validate_txt_file(content)

    if err:
        return template('clique_detection.tpl', title='Clique detection',
                        request=request, theory=theory, tab='file',
                        n=None, matrix=None, result=None,
                        errors={'file': err}, file_name=upload.filename)

    n = len(matrix)
    return template('clique_detection.tpl', title='Clique detection',
                    request=request, theory=theory, tab='file',
                    n=n, matrix=matrix, result=None, errors={},
                    file_name=upload.filename)


# ─── Клики: POST (построить граф из файла) ───────────────────────────────────

@route('/clique_detection_file_solve', method='POST')
def clique_detection_file_solve():
    theory = _load_theory()

    n, n_err = validate_n(request.forms.get('n'))
    if n_err:
        return template('clique_detection.tpl', title='Clique detection',
                        request=request, theory=theory, tab='file',
                        n=None, matrix=None, result=None, errors={'n': n_err},
                        file_name=None)

    matrix, matrix_errors = validate_matrix(request.forms, n)
    if matrix_errors:
        return template('clique_detection.tpl', title='Clique detection',
                        request=request, theory=theory, tab='file',
                        n=n, matrix=None, result=None, errors=matrix_errors,
                        file_name=None)

    try:
        result = solve_cliques(matrix, n)
    except Exception as e:
        return template('clique_detection.tpl', title='Clique detection',
                        request=request, theory=theory, tab='file',
                        n=n, matrix=matrix, result=None,
                        errors={'file': f'Ошибка при построении графа: {e}'},
                        file_name=None)
    return template('clique_detection.tpl', title='Clique detection',
                    request=request, theory=theory, tab='file',
                    n=n, matrix=matrix, result=result, errors={},
                    file_name=None)


# ─── Клики: POST (сохранить ZIP) ─────────────────────────────────────────────

@route('/clique_save', method='POST')
def clique_save():
    n, n_err = validate_n(request.forms.get('n'))
    if n_err:
        return f'Ошибка: {n_err}'

    matrix, matrix_errors = validate_matrix(request.forms, n)
    if matrix_errors:
        return 'Ошибка в данных матрицы.'

    result = solve_cliques(matrix, n)

    current_time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    lines = [f'Количество вершин: {n}', '']
    lines.append(f'Дата и время сохранения: {current_time}')
    lines.append('\nМатрица смежности:')
    lines.append('   ' + '  '.join(str(j + 1).rjust(2) for j in range(n)))
    for i in range(n):
        lines.append(str(i + 1).rjust(2) + ' ' + '  '.join(str(matrix[i][j]).rjust(2) for j in range(n)))
    lines.append('')
    cliques = result['maximal_cliques']
    if cliques:
        lines.append(f'Максимальных клик найдено: {len(cliques)}')
        for idx, clique in enumerate(cliques):
            lines.append(f'{idx + 1}) {{{", ".join(map(str, clique))}}}')
    else:
        lines.append('Максимальных клик не найдено.')

    txt_bytes = '\n'.join(lines).encode('utf-8')
    png_bytes = base64.b64decode(result['graph_png'])

    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('graph.png', png_bytes)
        zf.writestr('results.txt', txt_bytes)
    zip_buf.seek(0)

    response.content_type = 'application/zip'
    response.headers['Content-Disposition'] = 'attachment; filename="clique_results.zip"'
    return zip_buf.read()