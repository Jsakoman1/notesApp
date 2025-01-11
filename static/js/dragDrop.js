document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.container');

    // Event delegation for dragging notes
    container.addEventListener('dragstart', (event) => {
        if (event.target.classList.contains('note')) {
            event.target.setAttribute('draggable', 'true');
            event.dataTransfer.setData('noteId', event.target.dataset.noteId);
            event.target.classList.add('dragging');  // Apply dragging style to the note
        }
    });

    container.addEventListener('dragend', (event) => {
        if (event.target.classList.contains('note')) {
            event.target.classList.remove('dragging');  // Remove dragging style when drag ends
        }
    });

    // Event delegation for folders (dragover)
    container.addEventListener('dragover', (event) => {
        // Ensure we're dealing with a folder
        const folder = event.target.closest('.folder');
        
        if (folder) {
            event.preventDefault();

            // Only highlight the target folder
            folder.classList.add('dragover');  // Highlight the folder as the drop target

            const notes = folder.querySelectorAll('.note');
            const draggingNote = document.querySelector('.note.dragging');

            if (notes.length > 0 && draggingNote) {
                const targetNote = Array.from(notes).find(note => note !== draggingNote);
                if (targetNote) {
                    // Add "dragover" effect when a note is hovered over another inside the folder
                    targetNote.classList.add('dragover');
                } else {
                    // Reset any dragover effect if there's no valid position
                    folder.classList.add('dragover');
                }
            } else {
                // Add "dragover" effect when the folder is empty
                folder.classList.add('dragover');
            }
        }
    });

    // Event delegation for when leaving a folder (dragleave)
    container.addEventListener('dragleave', (event) => {
        const folder = event.target.closest('.folder');
        if (folder) {
            // Remove the "dragover" effect from the target folder
            folder.classList.remove('dragover');
            const notes = folder.querySelectorAll('.note');
            notes.forEach(note => note.classList.remove('dragover'));
        }
    });

    // Event delegation for drop action
    container.addEventListener('drop', (event) => {
        event.preventDefault();

        const folder = event.target.closest('.folder');  // Get the closest folder element

        if (folder) {
            const noteId = event.dataTransfer.getData('noteId');
            const folderId = folder.dataset.folderId;

            // Move the note via API
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
                    
                    // Move the note to the new folder
                    targetFolderNotes.appendChild(noteElement);

                    // Clear "dragover" effects after successful drop
                    folder.classList.remove('dragover');
                    folder.querySelectorAll('.note').forEach(note => note.classList.remove('dragover'));
                } else {
                    alert('Error moving note');
                }
            })
            .catch(error => console.error('Error moving note:', error));
        }
    });
});