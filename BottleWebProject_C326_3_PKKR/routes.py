"""
Routes and views for the bottle application.
"""

from bottle import route, view, request
from datetime import datetime


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
    return dict(
        title='Hamillton graph',
        request=request
    )


@route('/clique_detection')
@view('clique_detection')
def clique_detection():
    return dict(
        title='Clique detection',
        request=request
    )


@route('/kosarayu_algorithm')
@view('kosarayu_algorithm')
def kosarayu_algorithm():
    return dict(
        title='Kosarayu_algorithm',
        request=request
    )