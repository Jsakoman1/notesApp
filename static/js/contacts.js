const sendRequest = async (url, method, body = null) => {
    const options = { method, headers: { 'Content-Type': 'application/json' } };
    if (body) options.body = JSON.stringify(body);
    const response = await fetch(url, options);
    return response.json();
};

const loadContacts = async () => {
    const data = await sendRequest('/contacts', 'GET');
    const contactsList = document.getElementById('contacts-list');
    contactsList.innerHTML = data.contacts.length ? data.contacts.map(contact => `
        <li>
            ${contact.first_name} ${contact.last_name} - ${contact.email}
            <button onclick="deleteContact(${contact.id})">Delete</button>
        </li>
    `).join('') : '<li>No contacts found.</li>';
};

const deleteContact = async (contactId) => {
    const data = await sendRequest(`/contacts/${contactId}`, 'DELETE');
    if (data.success) {
        alert('Contact deleted');
        loadContacts();
    } else {
        alert('Error deleting contact');
    }
};

document.getElementById('contact-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = {
        first_name: document.getElementById('contact_first_name').value,
        last_name: document.getElementById('contact_last_name').value,
        email: document.getElementById('contact_email').value
    };
    const data = await sendRequest('/contacts', 'POST', formData);
    alert(data.success ? 'Contact added successfully' : `Error adding contact: ${data.message}`);
    if (data.success) loadContacts();
});

window.onload = loadContacts;