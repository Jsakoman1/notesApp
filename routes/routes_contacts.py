from flask import Blueprint, request, jsonify, render_template
from db import db, Contact

# Define the blueprint for contacts
contacts_routes = Blueprint('contacts_routes', __name__)

# Route to render the contacts page
@contacts_routes.route('/page', methods=['GET'])
def contacts_page():
    return render_template('contacts.html')


# Route to get all contacts
@contacts_routes.route('/', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify({'contacts': [{'id': contact.id, 'first_name': contact.first_name, 'last_name': contact.last_name, 'email': contact.email} for contact in contacts]})

# Route to add a new contact
@contacts_routes.route('/', methods=['POST'])
def add_contact():
    data = request.get_json()

    # Check if the email already exists
    existing_contact = Contact.query.filter_by(email=data['email']).first()
    if existing_contact:
        return jsonify({'success': False, 'message': 'Email already exists'}), 400

    new_contact = Contact(first_name=data['first_name'], last_name=data['last_name'], email=data['email'])
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Contact added successfully'}), 201

# Route to delete a contact
@contacts_routes.route('/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Contact deleted successfully'})