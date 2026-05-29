"""
Routes and views for the bottle application.
"""

from bottle import route, view, request, template
from datetime import datetime

from hamillton_graph import hamillton_graph, valid_hamillton

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        
    )

@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About'
    )


@route('/euler_graph')
@view('euler_graph')
def euler_grap():
    return dict(
        title='Euler grap'
    )

@route('/hamillton_graph')
@view('hamillton_graph')
def hamillton_graph():
    return template(
        'hamillton_graph.tpl',
        title='Hamilltom graph',
        result=None,
        success=False,
        errors={},
        form_data={}
    )

@route('/decide_hamillton_graph', method='POST')
@view('hamillton_graph')
def decide_hamillton_graph():
    n = int(request.forms.get('n'))

    matrix = []

    for i in range(n):

        row = []

        for j in range(n):

            row.append(
                int(
                    request.forms.get(
                        f'cell_{i}_{j}',
                        '0'
                    )
                )
            )

        matrix.append(row)

    errors = valid_hamillton(matrix)

    if errors:

        return template(
            'hamillton_graph.tpl',
            title='Hamilltom graph',
            result=None,
            success=False,
            errors=errors,
            form_data=request.forms
        )

    result = hamillton_graph(matrix)

    return template(
        'hamillton_graph.tpl',
        title='Hamilltom graph',
        result=result,
        success=True,
        errors={},
        form_data=request.forms
    )

@route('/clique_detection')
@view('clique_detection')
def clique_detection():
    return dict(
        title='Clique detection'
    )

@route('/kosarayu_algorithm')
@view('kosarayu_algorithm')
def kosarayu_algorithm():
    return dict(
        title='Kosarayu_algorithm'
    )