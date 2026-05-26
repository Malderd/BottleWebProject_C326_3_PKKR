"""
Routes and views for the bottle application.
"""

from bottle import route, view, request, template
from datetime import datetime

from algorithms.hamilton_graph import find_hamiltonian
from validators.valid_hamilton import validate_matrix

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