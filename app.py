from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from db import db, Folder, Note, Contact
from routes.routes_notes import notes_routes
from routes.routes_pages import pages_routes
from routes.routes_contacts import contacts_routes
import openai
import datetime
from routes.routes_emails import emails_routes

# Define your Flask app
app = Flask(__name__)

# Configure database URI
if os.getenv('FLASK_ENV') == 'development':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev_notes.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

# Set the secret key from the environment variable
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Register blueprints
app.register_blueprint(pages_routes)
app.register_blueprint(notes_routes)
app.register_blueprint(emails_routes, url_prefix='/emails')
app.register_blueprint(contacts_routes, url_prefix='/contacts')

# Initialize and create default folder
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
        initialize_db(app)  # Pass 'app' as an argument

    # Start the Flask application
    app.run(debug=True)