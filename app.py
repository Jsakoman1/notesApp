from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Update your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://super:Villigen5234@localhost:9999/dev_notes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Note model with schema
class Note(db.Model):
    __tablename__ = 'notes'
    __table_args__ = {'schema': 'public'}  # Specify the schema (public)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<Note {self.title}>'

# Route to display all notes
@app.route('/')
def index():
    notes = Note.query.all()
    return render_template('note_list.html', notes=notes)

# Route to create a new note (example)
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

if __name__ == '__main__':
    # Make sure to create the tables
    with app.app_context():
        db.create_all()  # Creates the tables in the database if they don't exist
    app.run(debug=True)