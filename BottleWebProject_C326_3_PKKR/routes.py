"""
Routes and views for the bottle application.
"""

from bottle import route, view
from datetime import datetime
import json

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
    return dict(
        title='Hamillton graph'
    )

@route('/clique_detection')
@view('clique_detection')
def clique_detection():
    with open('./static/data/cliques_theory.json', encoding='utf-8') as f:
        theory = json.load(f)
    return dict(
        title='Clique detection',
        theory=theory
    )

@route('/kosarayu_algorithm')
@view('kosarayu_algorithm')
def kosarayu_algorithm():
    return dict(
        title='Kosarayu_algorithm'
    )