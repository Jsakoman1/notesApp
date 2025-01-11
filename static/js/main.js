        // Show note content in the edit form
        function showNoteContent(noteId) {
            // Fetch note data from the server
            fetch(`/api/v1/notes/${noteId}`)
                .then(response => response.json())
                .then(data => {
                    if (data) {
                        // Populate the form fields with note data
                        document.getElementById('note-id').value = data.id;
                        document.getElementById('note-title').value = data.title;
                        document.getElementById('note-content').value = data.content;
                        document.getElementById('note-folder').value = data.folder_id;
                        
                        // Display the edit form
                        document.getElementById('note-edit-form').style.display = 'block';
                    } else {
                        alert('Note not found');
                    }
                })
                .catch(error => console.error('Error fetching note:', error));
        }

        // Handle new note creation
        document.getElementById('create-note-btn').addEventListener('click', function() {
            document.getElementById('new-note-form').style.display = 'block';
        });

        // Create new note
        document.getElementById('create-note-form').addEventListener('submit', function(event) {
            event.preventDefault();

            const title = document.getElementById('new-note-title').value;
            const content = document.getElementById('new-note-content').value;
            const folderId = document.querySelector('.folder-toggle').getAttribute('data-folder-id');

            fetch('/api/v1/notes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    title: title,
                    content: content,
                    folder_id: folderId
                })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('new-note-form').style.display = 'none';
                window.location.reload();
            })
            .catch(error => console.error('Error creating note:', error));
        });

        // Create new folder
        document.getElementById('create-folder-btn').addEventListener('click', function() {
            const folderName = prompt("Enter folder name:");
            if (folderName) {
                fetch('/api/v1/folders', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ name: folderName })
                })
                .then(response => response.json())
                .then(data => {
                    window.location.reload();
                })
                .catch(error => console.error('Error creating folder:', error));
            }
        });

// Event listener for folder actions (Rename & Delete)
document.querySelector('.container').addEventListener('click', function(event) {
    if (event.target.classList.contains('edit-folder-btn')) {
        const folderId = event.target.getAttribute('data-folder-id');
        editFolder(folderId);
    } else if (event.target.classList.contains('delete-folder-btn')) {
        const folderId = event.target.getAttribute('data-folder-id');
        deleteFolder(folderId);
    }
});

// Edit folder name
function editFolder(folderId) {
    const newName = prompt("Enter new folder name:");
    if (newName) {
        fetch(`/api/v1/folders/${folderId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: newName })
        })
        .then(response => response.json())
        .then(data => {
            if (data.name) {
                // Update the folder name in the UI
                document.querySelector(`#folder-${folderId} .folder-toggle`).innerText = data.name;
            }
        })
        .catch(error => console.error('Error editing folder:', error));
    }
}


// Delete folder and all notes inside it
function deleteFolder(folderId) {
    if (confirm("Are you sure you want to delete this folder and all notes inside it?")) {
        // Fetch the notes associated with the folder to delete them
        fetch(`/api/v1/folders/${folderId}/notes`, {
            method: 'GET'
        })
        .then(response => response.json())
        .then(notes => {
            // Delete each note associated with the folder
            const deleteNotePromises = notes.map(note => {
                return fetch(`/api/v1/notes/${note.id}`, {
                    method: 'DELETE'
                });
            });

            // Wait for all notes to be deleted
            Promise.all(deleteNotePromises)
                .then(() => {
                    // After deleting all notes, delete the folder
                    return fetch(`/api/v1/folders/${folderId}`, {
                        method: 'DELETE'
                    });
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        // Remove the folder from the UI
                        document.getElementById(`folder-${folderId}`).remove();
                    } else {
                        alert('Error deleting folder');
                    }
                })
                .catch(error => console.error('Error deleting notes or folder:', error));
        })
        .catch(error => console.error('Error fetching notes to delete:', error));
    }
}

document.querySelector('.container').addEventListener('click', function(event) {
    if (event.target.classList.contains('generate-note-btn')) {
        const form = event.target.closest('form');
        const titleInput = form.querySelector('input[type="text"]'); // Get the title input
        const contentArea = form.querySelector('textarea');
        const userTitle = titleInput.value; // Get the title value
        const userInput = contentArea.value;
        const folderId = document.querySelector('.folder-toggle').getAttribute('data-folder-id');

        if (!userTitle.trim()) {
            alert('Title is required.');
            return;
        }

        // Call to generate text, but don't save it yet
        fetch('/api/v1/notes/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: userTitle, // Send the title along with input and folder_id
                input: userInput,
                folder_id: folderId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error generating note: ' + data.error);
            } else {
                contentArea.value = data.content;  // Update the content area with the generated text
            }
        })
        .catch(error => console.error('Error sending to ChatGPT:', error));
    }

    // Handle save note button click
    if (event.target.classList.contains('save-note-btn')) {
        const form = event.target.closest('form');
        const titleInput = form.querySelector('input[type="text"]'); // Get the title input
        const contentArea = form.querySelector('textarea');
        const userTitle = titleInput.value;
        const userInput = contentArea.value;
        const folderId = document.querySelector('.folder-toggle').getAttribute('data-folder-id');

        if (!userTitle.trim()) {
            alert('Title is required.');
            return;
        }

        // Save the note when the save button is clicked
        fetch('/api/v1/notes/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: userTitle,
                input: userInput,
                folder_id: folderId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error saving note: ' + data.error);
            } else {
                alert('Note saved successfully!');
            }
        })
        .catch(error => console.error('Error saving note:', error));
    }
});