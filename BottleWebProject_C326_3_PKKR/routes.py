"""
Routes and views for the bottle application.
"""
from bottle import route, view, request, template, post, static_file, response
from datetime import datetime
import json, io, zipfile, base64
import os
import ast
import random

from algorithms.hamillton_graph import find_hamillton_graph
from validations.valid_hamillton import valid_hamillton
from algorithms.draw_graph import draw_graph, save_graph_archive
from algorithms.clique_detection import solve_cliques, generate_random_matrix
from validations.valid_clique import validate_n, validate_matrix, validate_density, validate_txt_file
from algorithms.euler_graph import solve_euler
from validations.valid_euler import validation_euler,validation_random_params, validation_and_parse_file
from algorithms.kosarayu_algorithm import find_components
from algorithms.graph_visualizer import draw_directed_graph
from validations.valid_kosarayu import validate_matrix_kosarayu, validate_matrix_text
from algorithms.euler import draw_graph, find_eulerian_path

# Эйлеров граф - маршруты для рисования и решения
@route('/euler/draw', method='POST')
def euler_draw_route():
    """Маршрут для отрисовки графа"""
    try:
        data = request.json
        if not data or "matrix" not in data:
            return {"error": "Матрица не передана"}
        
        matrix = data.get("matrix", [])
        if not matrix:
            return {"error": "Пустая матрица"}
        
        image_base64 = draw_graph(matrix)
        return {"image": image_base64}
    except Exception as e:
        return {"error": f"Ошибка при отрисовке графа: {str(e)}"}

@route('/euler/solve', method='POST')
def euler_solve_route():
    """Маршрут для поиска Эйлерова маршрута"""
    try:
        data = request.json
        if not data or "matrix" not in data:
            return {"exists": False, "message": "Матрица не передана"}
        
        matrix = data.get("matrix", [])
        if not matrix:
            return {"exists": False, "message": "Пустая матрица"}
        
        is_valid, error_res = validation_euler(matrix)
        if not is_valid:
            return error_res
            
        result = find_eulerian_path(matrix)
        return result
    except Exception as e:
        return {"exists": False, "message": f"Ошибка сервера: {str(e)}"}

@route('/euler/random', method='POST')
def euler_random_route():
    """Маршрут для генерации случайного графа"""
    try:
        data = request.json
        if not data or "n" not in data or "density" not in data:
            return {"error": "Не переданы параметры генерации"}

        is_valid, n, density, error_res = validation_random_params(data["n"], data["density"])
        if not is_valid:
            return error_res

        matrix = [[0] * n for _ in range(n)]
        density_p = density / 100
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < density_p:
                    matrix[i][j] = 1
                    matrix[j][i] = 1

        return {"matrix": matrix}
    except Exception as e:
        return {"error": f"Ошибка сервера при генерации: {str(e)}"}

@route('/euler/from_file', method='POST')
def euler_from_file_route():
    """Маршрут для загрузки матрицы из файла"""
    try:
        uploaded_file = request.files.get("file")
        if not uploaded_file:
            return {"error": "Файл не передан"}
        
        is_valid, matrix, error_res = validation_and_parse_file(uploaded_file)
        if not is_valid:
            return error_res

        return {"matrix": matrix}
    except Exception as e:
        return {"error": f"Ошибка сервера при загрузке файла: {str(e)}"}

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
def euler_graph():
    return dict(
        title='Euler graph',
        request=request
    )

@route('/hamillton_graph')
@view('hamillton_graph')
def hamillton_graph():
    return template(
        'hamillton_graph.tpl',
        title='Hamilltom graph',
        result=None,
        graph_image=None,
        success=False,
        errors={},
        form_data={},
        request=request
    )

@route('/decide_hamillton_graph', method='POST')
@view('hamillton_graph')
def decide_hamillton_graph():
    n = int(request.forms.get('n'))

    # Получение нажатой кнопки
    action = request.forms.get('action') 
    
    # Чтение матрицы из формы
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(
                request.forms.get(
                    f'{i}_{j}',
                    ''
                )
            )
        matrix.append(row)

    # Проверка валидности
    errors = valid_hamillton(matrix)

    if errors:

        return template(
            'hamillton_graph.tpl',
            title='Hamilltom graph',
            result=None,
            graph_image=None,
            success=False,
            errors=errors,
            form_data=request.forms,
            request=request
        )

    # Преобразование строк в чисоа
    matrix = [[int(cell) for cell in row]for row in matrix]

    graph_image = None
    result = None

    if action == "solve":
        result = find_hamillton_graph(matrix)
        graph_image = draw_graph(matrix)

    elif action == "save":

        zip_name, temp_dir = save_graph_archive(matrix)

        return static_file(
            zip_name,
            root=temp_dir,
            download=zip_name
        )

    return template(
        'hamillton_graph.tpl',
        title='Hamilltom graph',
        result=result,
        graph_image=graph_image,
        success=True,
        errors={},
        form_data=request.forms,
        request=request
    )

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


# Клики: POST (построить граф — ручной и случайный)
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


# ─── Клики: POST (загрузка TXT-файла)
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


# ─── Клики: POST (построить граф из файла)
@route('/clique_detection_file_solve', method='POST')
def clique_detection_file_solve():
    saved_file_name = request.forms.get('file_name', None) or None
    theory = _load_theory()

    n, n_err = validate_n(request.forms.get('n'))
    if n_err:
        return template('clique_detection.tpl', title='Clique detection',
                        request=request, theory=theory, tab='file',
                        n=None, matrix=None, result=None, errors={'n': n_err},
                       file_name=saved_file_name)

    matrix, matrix_errors = validate_matrix(request.forms, n)
    if matrix_errors:
        return template('clique_detection.tpl', title='Clique detection',
                        request=request, theory=theory, tab='file',
                        n=n, matrix=None, result=None, errors=matrix_errors,
                        file_name=saved_file_name)

    try:
        result = solve_cliques(matrix, n)
    except Exception as e:
        return template('clique_detection.tpl', title='Clique detection',
                        request=request, theory=theory, tab='file',
                        n=n, matrix=matrix, result=None,
                        errors={'file': f'Ошибка при построении графа: {e}'},
                        file_name=saved_file_name)
    return template('clique_detection.tpl', title='Clique detection',
                    request=request, theory=theory, tab='file',
                    n=n, matrix=matrix, result=result, errors={},
                    file_name=saved_file_name)


# ─── Клики: POST (сохранить ZIP)
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
    cliques = result['all_cliques']

    if cliques:
        lines.append(f'Найдено клик: {len(cliques)}')
        for idx, clique in enumerate(cliques):
            lines.append(f'{idx + 1}) {{{", ".join(map(str, clique))}}}')
    else:
        lines.append('Клик не найдено.')

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
@route('/kosarayu_algorithm')
@view('kosarayu_algorithm')
def kosarayu_algorithm():
    with open('./static/data/kosarayu_theory.json', encoding='utf-8') as f:
        theory = json.load(f)
    return dict(
        title='Kosarayu_algorithm',
        request=request,
        matrix=None,
        components=None,
        theory=theory,
        graph_image=None,
        errors = None
    )

@post('/kosarayu_algorithm/find_components')
@view('kosarayu_algorithm')
def find_components_route():

    with open('./static/data/kosarayu_theory.json', encoding='utf-8') as f:
        theory = json.load(f)

    matrix_json = request.forms.get('matrix_data')
    matrix = json.loads(matrix_json)

    errors = validate_matrix_kosarayu(matrix)

    # если есть ошибки — не считаем
    if errors:
        return dict(
            title='Kosarayu_algorithm',
            request=request,
            theory=theory,
            matrix=matrix,
            components=None,
            graph_image=None,
            errors=errors
        )

    components = find_components(matrix)
    draw_directed_graph(
        matrix,
        components,
        "static/images/result_graph.png"
    )
    return dict(
        title='Kosarayu_algorithm',
        request=request,
        theory=theory,
        matrix=matrix,
        components=components,
        graph_image="/static/images/result_graph.png",
        errors = None
    )

@post('/kosarayu_algorithm/load_matrix')
@view('kosarayu_algorithm')
def load_matrix_route():
    errors = []
    matrix = None
    file = request.files.get('matrix_file')
    allowed_extension = ".txt"
    extension = os.path.splitext(file.filename)[1].lower()

    if not file:
        errors.append("Файл не выбран")
    elif extension != allowed_extension:
        errors.append("Загружаемый файл должен быть расширения TXT")
    else:
        text = file.file.read().decode("utf-8").strip()
        valid, result = validate_matrix_text(text)
        if not valid:
            errors.append(result)
        else:
            matrix = result

    # Передаем matrix в шаблон, чтоб JS потом построил таблицу
    return dict(
        title='Kosarayu_algorithm',
        request=request,
        matrix=matrix,
        components=None,
        graph_image=None,
        theory=json.load(open('./static/data/kosarayu_theory.json', encoding='utf-8')),
        errors=errors
    )

@post('/kosarayu_algorithm/save_matrix')
def save_matrix():

    matrix = ast.literal_eval(
        request.forms.get("matrix")
    )

    components = ast.literal_eval(
        request.forms.get("components")
    )

    text = f'Дата: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n'

    text += "Матрица смежности:\n"

    for row in matrix:
        text += " ".join(map(str, row)) + "\n"

    text += "\nКомпоненты сильной связности:\n"

    for component in components:
        text += "{" + ", ".join(map(str, component)) + "}\n"

    response.content_type = "text/plain; charset=utf-8"
    response.headers[
        "Content-Disposition"
    ] = 'attachment; filename="result.txt"'

    return text