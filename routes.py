from flask import Blueprint, request, jsonify, render_template
from db import db, Folder, Note

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def index():
    folders = Folder.query.all()
    return render_template('index.html', folders=folders)

@main_routes.route('/api/v1/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    folder_id = data.get('folder_id')

    if not title or not content:
        return jsonify({"message": "Title and content are required"}), 400

    folder = Folder.query.get(folder_id) if folder_id else Folder.query.filter_by(name='All Notes').first()
    if not folder:
        folder = Folder(name='All Notes')
        db.session.add(folder)
        db.session.commit()

    new_note = Note(title=title, content=content, folder_id=folder.id)
    db.session.add(new_note)
    db.session.commit()

    return jsonify({"id": new_note.id, "title": new_note.title, "content": new_note.content, "folder_id": new_note.folder_id}), 201

@main_routes.route('/api/v1/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = Note.query.get(note_id)
    if note:
        return jsonify({
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'folder_id': note.folder_id
        })
    else:
        return jsonify({"error": "Note not found"}), 404

@main_routes.route('/api/v1/folders', methods=['POST'])
def create_folder():
    folder_data = request.get_json()
    new_folder = Folder(name=folder_data['name'])
    db.session.add(new_folder)
    db.session.commit()
    return jsonify(id=new_folder.id, name=new_folder.name), 201

@main_routes.route('/api/v1/notes/<int:note_id>/move', methods=['PUT'])
def move_note(note_id):
    data = request.get_json()
    folder_id = data.get('folder_id')

    note = Note.query.get(note_id)
    folder = Folder.query.get(folder_id)

    if note and folder:
        note.folder_id = folder.id
        db.session.commit()
        return jsonify({"success": True, "note": {"id": note.id, "title": note.title, "folder_id": note.folder_id}}), 200
    return jsonify({"error": "Note or Folder not found"}), 404