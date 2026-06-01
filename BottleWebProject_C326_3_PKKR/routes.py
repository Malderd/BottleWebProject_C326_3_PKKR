"""
Routes and views for the bottle application.
"""

from bottle import route, view, request, template, post
from datetime import datetime
import json
import random

from hamillton_graph import hamillton_graph, valid_hamillton
from algorithms.euler_graph import solve_euler


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
        
        matrix = data["matrix"]
        result = solve_euler(matrix)
        return result
    except Exception as e:
        return {"exists": False, "message": f"Ошибка сервера: {str(e)}"}

@post("/euler/random")
def euler_random_route():
    try:
        data = request.json
        n = int(data["n"])
        density = int(data["density"]) / 100

        matrix = [[0] * n for _ in range(n)]

        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < density:
                    matrix[i][j] = 1
                    matrix[j][i] = 1

        return {"matrix": matrix}
    except Exception as e:
        return {"error": f"Ошибка генерации: {str(e)}"}

@post("/euler/from_file")
def euler_from_file_route():
    f = request.files.get("file")
    if not f:
        return {"error": "Файл не передан"}

    try:
        content = f.file.read().decode("utf-8")
        matrix = []

        for line in content.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            # Читаем числа, разделенные пробелами или табуляцией
            row = list(map(int, line.split()))
            matrix.append(row)

        return {"matrix": matrix}
    except Exception as e:
        return {"error": f"Неверный формат файла: {str(e)}"}

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


