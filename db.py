from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Folder(db.Model):
    __tablename__ = 'folders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    notes = db.relationship('Note', backref='folder', lazy=True)

    def __repr__(self):
        return f'<Folder {self.name}>'

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'), nullable=True)

    def __repr__(self):
        return f'<Note {self.title}>'
    
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return f'<Contact {self.first_name} {self.last_name}>'