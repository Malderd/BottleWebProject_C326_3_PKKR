"""
Routes and views for the bottle application.
"""

from bottle import route, view, request, template
from datetime import datetime
import json

from hamillton_graph import hamillton_graph, valid_hamillton


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
def euler_grap():
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