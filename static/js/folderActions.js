const fetchData = async (url, method, body = null) => {
    const options = { method, headers: { 'Content-Type': 'application/json' } };
    if (body) options.body = JSON.stringify(body);
    const response = await fetch(url, options);
    return response.json();
};

export function createFolder() {
    document.getElementById('create-folder-btn').addEventListener('click', async () => {
        const folderName = prompt("Enter folder name:");
        if (folderName) {
            const data = await fetchData('/api/v1/folders', 'POST', { name: folderName });
            if (data) window.location.reload();
        }
    });
}

export function editFolder(folderId) {
    const newName = prompt("Enter new folder name:");
    if (newName) {
        fetchData(`/api/v1/folders/${folderId}`, 'PUT', { name: newName })
            .then(data => {
                if (data.name) document.querySelector(`#folder-${folderId} .folder-toggle`).innerText = data.name;
            })
            .catch(error => console.error('Error editing folder:', error));
    }
}

export function deleteFolder(folderId) {
    if (confirm("Are you sure you want to delete this folder and all notes inside it?")) {
        fetchData(`/api/v1/folders/${folderId}/notes`, 'GET')
            .then(notes => {
                const deleteNotes = notes.map(note => fetchData(`/api/v1/notes/${note.id}`, 'DELETE'));
                Promise.all(deleteNotes)
                    .then(() => fetchData(`/api/v1/folders/${folderId}`, 'DELETE'))
                    .then(data => {
                        if (data.message) document.getElementById(`folder-${folderId}`).remove();
                        else alert('Error deleting folder');
                    })
                    .catch(error => console.error('Error deleting notes or folder:', error));
            })
            .catch(error => console.error('Error fetching notes to delete:', error));
    }
}