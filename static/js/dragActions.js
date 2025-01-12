export function handleDragStart(event) {
    if (event.target.classList.contains('note')) {
        event.target.setAttribute('draggable', 'true');
        event.dataTransfer.setData('noteId', event.target.dataset.noteId);
        event.target.classList.add('dragging');
    }
}

export function handleDragEnd(event) {
    if (event.target.classList.contains('note')) {
        event.target.classList.remove('dragging');
    }
}

export function handleDragOver(event) {
    const folder = event.target.closest('.folder');
    if (folder) {
        event.preventDefault();
        folder.classList.add('dragover');
    }
}

export function handleDragLeave(event) {
    const folder = event.target.closest('.folder');
    if (folder) {
        folder.classList.remove('dragover');
    }
}

export function handleDrop(event) {
    event.preventDefault();
    const folder = event.target.closest('.folder');
    if (folder) {
        const noteId = event.dataTransfer.getData('noteId');
        const folderId = folder.dataset.folderId;
        fetch(`/api/v1/notes/${noteId}/move`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ folder_id: folderId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const noteElement = document.getElementById(`note-${noteId}`);
                const targetFolderNotes = document.getElementById(`folder-${folderId}-notes`);
                targetFolderNotes.appendChild(noteElement);
                folder.classList.remove('dragover');
            } else {
                alert('Error moving note');
            }
        })
        .catch(error => console.error('Error moving note:', error));
    }
}