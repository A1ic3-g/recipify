from flask import Blueprint, render_template, redirect, url_for, request
#from ../backend import 

pages = Blueprint('pages', __name__)


@pages.route('/')
def index_page():
    pass


