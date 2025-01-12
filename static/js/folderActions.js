export function createFolder() {
    document.getElementById('create-folder-btn').addEventListener('click', function() {
        const folderName = prompt("Enter folder name:");
        if (folderName) {
            fetch('/api/v1/folders', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: folderName })
            })
            .then(response => response.json())
            .then(() => {
                window.location.reload();
            })
            .catch(error => console.error('Error creating folder:', error));
        }
    });
}

export function editFolder(folderId) {
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
                document.querySelector(`#folder-${folderId} .folder-toggle`).innerText = data.name;
            }
        })
        .catch(error => console.error('Error editing folder:', error));
    }
}

export function deleteFolder(folderId) {
    if (confirm("Are you sure you want to delete this folder and all notes inside it?")) {
        fetch(`/api/v1/folders/${folderId}/notes`, { method: 'GET' })
            .then(response => response.json())
            .then(notes => {
                const deleteNotePromises = notes.map(note => {
                    return fetch(`/api/v1/notes/${note.id}`, { method: 'DELETE' });
                });

                Promise.all(deleteNotePromises)
                    .then(() => fetch(`/api/v1/folders/${folderId}`, { method: 'DELETE' }))
                    .then(response => response.json())
                    .then(data => {
                        if (data.message) {
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