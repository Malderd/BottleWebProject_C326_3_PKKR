"""
Routes and views for the bottle application.
"""

from bottle import route, view, request, template, post
from datetime import datetime
import json
import random

from hamillton_graph import hamillton_graph, valid_hamillton
from algorithms.euler_graph import solve_euler
from validations.valid_euler import validation_euler,validation_random_params, validation_and_parse_file


@route('/')
@route('/home')
@view('index')
def home():
    return dict(
        request=request
    )


@route('/about')
@view('about')
def about():
    return dict(
        title='About',
        request=request
    )


@route('/euler_graph')
@view('euler_graph')
def euler_graph():
    return dict(
        title='Euler graph',
        request=request
    )
@post("/euler/solve")
def euler_solve_route():
    try:
        data = request.json
        if not data or "matrix" not in data:
            return {"exists": False, "message": "Матрица не передана"}
        
        # 1. Валидация матрицы перед решением
        is_valid, error_res = validation_euler(data["matrix"])
        if not is_valid:
            return error_res
            
        return solve_euler(data["matrix"])
    except Exception as e:
        return {"exists": False, "message": f"Ошибка сервера: {str(e)}"}

@post("/euler/random")
def euler_random_route():
    try:
        data = request.json
        if not data or "n" not in data or "density" not in data:
            return {"error": "Не переданы параметры генерации"}

        # 2. Валидация входных параметров для генерации
        is_valid, n, density, error_res = validation_random_params(data["n"], data["density"])
        if not is_valid:
            return error_res

        # Чистая генерация, так как параметры уже проверены и безопасны
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

@post("/euler/from_file")
def euler_from_file_route():
    # 3. Валидация и парсинг файла в одном месте
    is_valid, matrix, error_res = validation_and_parse_file(request.files.get("file"))
    if not is_valid:
        return error_res

    return {"matrix": matrix}


@route('/hamillton_graph')
@view('hamillton_graph')
def hamillton_graph():
    return template(
        'hamillton_graph.tpl',
        title='Hamilltom graph',
        result=None,
        success=False,
        errors={},
        form_data={},
        request=request
    )

@route('/decide_hamillton_graph', method='POST')
@view('hamillton_graph')
def decide_hamillton_graph():
  
    return template(
        'hamillton_graph.tpl',
        title='Hamilltom graph',
        result=None,
        success=True,
        errors={},
        form_data=request.forms,
        request=request
    )

@route('/clique_detection')
@view('clique_detection')
def clique_detection():
    with open('./static/data/cliques_theory.json', encoding='utf-8') as f:
        theory = json.load(f)
    return dict(
        title='Clique detection',
        request=request,
        theory=theory
    )


@route('/kosarayu_algorithm')
@view('kosarayu_algorithm')
def kosarayu_algorithm():
    return dict(
        title='Kosarayu_algorithm',
        request=request
    )


