from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from db import db, Folder, Note
from routes import main_routes

app = Flask(__name__)

if os.getenv('FLASK_ENV') == 'development':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev_notes.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'postgresql://super:Villigen5234@localhost:9999/dev_notes'
    )


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(main_routes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Check if the "All Notes" folder exists, if not create it
        all_notes_folder = Folder.query.filter_by(name='All Notes').first()
        if not all_notes_folder:
            all_notes_folder = Folder(name='All Notes')
            db.session.add(all_notes_folder)
            db.session.commit()
    app.run(debug=True)