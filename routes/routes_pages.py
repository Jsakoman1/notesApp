from flask import Blueprint, request, jsonify, render_template
from db import db, Folder, Note
import openai
import os

client = openai.OpenAI()


# Route to all pages
pages_routes = Blueprint('pages_routes', __name__)

@pages_routes.route('/')
def index():
    folders = Folder.query.all()
    return render_template('index.html', folders=folders)

@pages_routes.route('/notes')
def notes():
    folders = Folder.query.all()
    return render_template('notes.html', folders=folders)

@pages_routes.route('/emails')
def emails():
    folders = Folder.query.all()
    return render_template('emails.html', folders=folders)
