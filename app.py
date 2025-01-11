from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from db import db, Folder, Note
from routes import main_routes

app = Flask(__name__)

# Configure database URI
if os.getenv('FLASK_ENV') == 'development':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev_notes.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
    )


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(main_routes)

def initialize_db(app):
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        # Check if the "All Notes" folder exists
        all_notes_folder = Folder.query.filter_by(name='All Notes').first()
        if not all_notes_folder:
            all_notes_folder = Folder(name='All Notes')
            db.session.add(all_notes_folder)
            db.session.commit()

# Ensure tables and default folder exist
if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        initialize_db(app)  # Pass 'app' as an argument

    app.run(debug=True)