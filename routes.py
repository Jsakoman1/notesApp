from flask import Blueprint, request, jsonify, render_template
from db import db, Folder, Note
import openai
import os

client = openai.OpenAI()

main_routes = Blueprint('main_routes', __name__)

# Route to display all folders on the main page
@main_routes.route('/')
def index():
    folders = Folder.query.all()
    return render_template('index.html', folders=folders)

# Create a new note
@main_routes.route('/api/v1/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    folder_id = data.get('folder_id')

    if not title or not content:
        return jsonify({"message": "Title and content are required"}), 400

    # If no folder_id is provided, use the default folder 'All Notes'
    folder = Folder.query.get(folder_id) if folder_id else Folder.query.filter_by(name='All Notes').first()
    if not folder:
        folder = Folder(name='All Notes')
        db.session.add(folder)
        db.session.commit()

    new_note = Note(title=title, content=content, folder_id=folder.id)
    db.session.add(new_note)
    db.session.commit()

    return jsonify({
        "id": new_note.id,
        "title": new_note.title,
        "content": new_note.content,
        "folder_id": new_note.folder_id
    }), 201

# Fetch a single note by its ID
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

# Update an existing note
@main_routes.route('/api/v1/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"error": "Note not found"}), 404
    
    data = request.get_json()
    note.title = data.get('title')
    note.content = data.get('content')
    note.folder_id = data.get('folder_id')

    db.session.commit()
    return jsonify({
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'folder_id': note.folder_id
    }), 200

# Delete a note
@main_routes.route('/api/v1/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"error": "Note not found"}), 404

    try:
        db.session.delete(note)
        db.session.commit()
        return jsonify({"message": "Note deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete note"}), 500

# Create a new folder
@main_routes.route('/api/v1/folders', methods=['POST'])
def create_folder():
    folder_data = request.get_json()
    new_folder = Folder(name=folder_data['name'])
    db.session.add(new_folder)
    db.session.commit()
    return jsonify(id=new_folder.id, name=new_folder.name), 201

# Rename an existing folder
@main_routes.route('/api/v1/folders/<int:folder_id>', methods=['PUT'])
def edit_folder(folder_id):
    folder_data = request.get_json()
    folder = Folder.query.get(folder_id)
    if folder:
        folder.name = folder_data['name']
        db.session.commit()
        return jsonify({"id": folder.id, "name": folder.name}), 200
    else:
        return jsonify({"error": "Folder not found"}), 404

# Delete a folder
@main_routes.route('/api/v1/folders/<int:folder_id>', methods=['DELETE'])
def delete_folder(folder_id):
    folder = Folder.query.get(folder_id)
    if folder:
        db.session.delete(folder)
        db.session.commit()
        return jsonify({"message": "Folder deleted successfully"}), 200
    else:
        return jsonify({"error": "Folder not found"}), 404

# Move a note to another folder
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

# Get all notes in a specific folder
@main_routes.route('/api/v1/folders/<int:folder_id>/notes', methods=['GET'])
def get_notes_in_folder(folder_id):
    folder = Folder.query.get(folder_id)
    if folder:
        notes = Note.query.filter_by(folder_id=folder_id).all()
        return jsonify([{
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'folder_id': note.folder_id
        } for note in notes]), 200
    else:
        return jsonify({"error": "Folder not found"}), 404

# Generate a note based on user input via OpenAI
@main_routes.route('/api/v1/notes/generate', methods=['POST'])
def generate_note():
    data = request.get_json()
    user_input = data.get('input')
    folder_id = data.get('folder_id')
    user_title = data.get('title')

    if not user_input:
        return jsonify({"error": "Input is required"}), 400
    if not user_title:
        return jsonify({"error": "Title is required"}), 400

    try:
        # Use the 'client' object to call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4"
            messages=[
                {"role": "system", "content": "Ti si pomoćnik za bilješke."},
                {"role": "user", "content": user_input}
            ]
        )
        
        # Get the generated content from the response
        note_content = response.choices[0].message.content

        # Send only the generated content back as a response
        return jsonify({
            "content": note_content
        }), 200

    except Exception as e:
        # Handle any errors that occur
        return jsonify({"error": str(e)}), 500