function sendNoteRequest(url, method, noteData) {
    return fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(noteData)
    })
    .then(response => response.json())
    .catch(error => {
        console.error(`Error ${method} note:`, error);
        alert(`Error ${method} note.`);
    });
}

export function showNoteContent(noteId) {
    fetch(`/api/v1/notes/${noteId}`)
        .then(response => response.json())
        .then(data => {
            if (data) {
                document.getElementById('note-id').value = data.id;
                document.getElementById('note-title').value = data.title;
                // Set the content in the Quill editor
                const quill = document.querySelector('#note-content').__quill;
                quill.root.innerHTML = data.content; // Set the note content in Quill editor
                document.getElementById('note-folder').value = data.folder_id;
                document.getElementById('note-edit-form').style.display = 'block';
            } else {
                alert('Note not found');
            }
        })
        .catch(error => console.error('Error fetching note:', error));
}

export function createNewNote() {
    document.getElementById('create-note-btn').addEventListener('click', function() {
        document.getElementById('new-note-form').style.display = 'block';
    });

    document.getElementById('create-note-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const title = document.getElementById('new-note-title').value;
        // Get content from Quill editor
        const content = document.querySelector('#new-note-content').__quill.root.innerHTML;
        const folderId = document.querySelector('.folder-toggle').getAttribute('data-folder-id');

        const noteData = { title, content, folder_id: folderId };

        sendNoteRequest('/api/v1/notes', 'POST', noteData)
            .then(() => {
                document.getElementById('new-note-form').style.display = 'none';
                window.location.reload();
            });
    });
}

export function generateNote() {
    document.querySelector('.container').addEventListener('click', function(event) {
        if (event.target.classList.contains('generate-note-btn')) {
            const form = event.target.closest('form');
            const titleInput = form.querySelector('input[type="text"]');
            const contentArea = form.querySelector('.quill-editor'); // Quill editor container
            const userTitle = titleInput.value;
            const userInput = contentArea.__quill.root.innerHTML; // Get content from Quill editor
            const folderId = document.querySelector('.folder-toggle').getAttribute('data-folder-id');

            if (!userTitle.trim()) {
                alert('Title is required.');
                return;
            }

            const noteData = { title: userTitle, input: userInput, folder_id: folderId };

            sendNoteRequest('/api/v1/notes/generate', 'POST', noteData)
                .then(data => {
                    if (data && data.content) {
                        contentArea.__quill.root.innerHTML = data.content; // Update Quill editor content
                    } else {
                        alert('Error generating note.');
                    }
                });
        }
    });
}

export function handleSaveNote() {
    document.querySelector('.container').addEventListener('click', function(event) {
        if (event.target.classList.contains('save-note-btn')) {
            const form = event.target.closest('form');
            const titleInput = form.querySelector('input[type="text"]');
            const contentArea = form.querySelector('.quill-editor'); // Quill editor container
            const userTitle = titleInput.value;
            const userInput = contentArea.__quill.root.innerHTML; // Get content from Quill editor
            const folderId = document.querySelector('.folder-toggle').getAttribute('data-folder-id');

            if (!userTitle.trim()) {
                alert('Title is required.');
                return;
            }

            const noteData = { title: userTitle, input: userInput, folder_id: folderId };

            sendNoteRequest('/api/v1/notes/save', 'POST', noteData)
                .then(() => alert('Note saved successfully!'));
        }
    });
}

export function handleSaveEditedNote() {
    document.getElementById('edit-note-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const titleInput = document.getElementById('note-title');
        const contentArea = document.getElementById('note-content');
        const userTitle = titleInput.value;
        const userInput = contentArea.__quill.root.innerHTML; // Get content from Quill editor
        const noteId = document.getElementById('note-id').value;
        const folderId = document.getElementById('note-folder').value;

        if (!userTitle.trim()) {
            alert('Title is required.');
            return;
        }

        const noteData = { title: userTitle, content: userInput, folder_id: folderId };

        sendNoteRequest(`/api/v1/notes/${noteId}`, 'PUT', noteData)
            .then(() => window.location.reload());
    });
}

export function deleteNote(noteId) {
    if (!confirm('Are you sure you want to delete this note?')) {
        return; // User canceled the deletion
    }

    sendNoteRequest(`/api/v1/notes/${noteId}`, 'DELETE')
        .then(response => {
            if (response && response.message === 'Note deleted successfully') {
                window.location.reload(); // Reload to update the UI
            } else {
                alert('Failed to delete the note.');
            }
        })
        .catch(error => console.error('Error deleting note:', error));
}