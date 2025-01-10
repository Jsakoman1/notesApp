from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure database URI from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'postgresql://super:Villigen5234@localhost:9999/dev_notes'
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

# API endpoint: Delete a note
@app.route('/api/v1/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted successfully!'})

# Route to display all notes
@app.route('/')
def index():
    notes = Note.query.all()
    return render_template('note_list.html', notes=notes)



if __name__ == '__main__':
    # Ensure tables are created
    with app.app_context():
        db.create_all()
    app.run(debug=True)