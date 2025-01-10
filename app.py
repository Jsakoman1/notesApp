from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Use PostgreSQL for production and SQLite for local development
if os.getenv('FLASK_ENV') == 'development':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev_notes.db'  # Local SQLite database
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',  # Production PostgreSQL (set in PythonAnywhere)
        'postgresql://super:Villigen5234@localhost:9999/dev_notes'  # Fallback for local testing if needed
    )

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Note model
class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<Note {self.title}>'

# API endpoint: Get all notes
@app.route('/api/v1/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    notes_list = [{'id': note.id, 'title': note.title, 'content': note.content, 'created_at': note.created_at} for note in notes]
    return jsonify(notes_list)

# Route to create a new note
@app.route('/create', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_note = Note(title=title, content=content)
        db.session.add(new_note)
        db.session.commit()
        return redirect('/')
    return render_template('create_note.html')

# API endpoint: Get a single note
@app.route('/api/v1/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    return jsonify({'id': note.id, 'title': note.title, 'content': note.content, 'created_at': note.created_at})

# Route to edit a note
@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        db.session.commit()
        return redirect('/')
    
    return render_template('edit_note.html', note=note)

# API endpoint: Delete a note
@app.route('/api/v1/notes/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    db.session.delete(note)
    db.session.commit()
    return redirect('/')

# Route to display all notes
@app.route('/')
def index():
    notes = Note.query.all()
    return render_template('note_list.html', notes=notes)

# Before request to handle method override for DELETE via form
@app.before_request
def before_request():
    if request.method == "POST" and "_method" in request.form:
        request.method = request.form["_method"]

if __name__ == '__main__':
    # Ensure tables are created
    with app.app_context():
        db.create_all()
    app.run(debug=True)