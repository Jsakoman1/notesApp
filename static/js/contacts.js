document.getElementById('contact-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const firstName = document.getElementById('contact_first_name').value;
    const lastName = document.getElementById('contact_last_name').value;
    const email = document.getElementById('contact_email').value;

    // Send POST request to add the new contact
    const response = await fetch('/contacts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ first_name: firstName, last_name: lastName, email: email })
    });

    const data = await response.json();
    if (data.success) {
        alert('Contact added successfully');
        loadContacts(); // Reload contacts
    } else {
        alert('Error adding contact: ' + data.message);
    }
});

// Function to load contacts
async function loadContacts() {
    const response = await fetch('/contacts');
    const data = await response.json();

    const contactsList = document.getElementById('contacts-list');
    contactsList.innerHTML = '';

    if (data.contacts.length === 0) {
        contactsList.innerHTML = '<li>No contacts found.</li>';
    } else {
        data.contacts.forEach(contact => {
            const li = document.createElement('li');
            li.textContent = `${contact.first_name} ${contact.last_name} - ${contact.email}`;
            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'Delete';
            deleteBtn.onclick = () => deleteContact(contact.id);
            li.appendChild(deleteBtn);
            contactsList.appendChild(li);
        });
    }
}

// Function to delete a contact
async function deleteContact(contactId) {
    const response = await fetch(`/contacts/${contactId}`, { method: 'DELETE' });
    const data = await response.json();
    if (data.success) {
        alert('Contact deleted');
        loadContacts(); // Reload contacts
    } else {
        alert('Error deleting contact');
    }
}

// Load contacts when page loads
window.onload = loadContacts;