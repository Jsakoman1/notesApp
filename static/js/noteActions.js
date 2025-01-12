// Show note content in the edit form
export function showNoteContent(noteId) {
    fetch(`/api/v1/notes/${noteId}`)
        .then(response => response.json())
        .then(data => {
            if (data) {
                document.getElementById('note-id').value = data.id;
                document.getElementById('note-title').value = data.title;
                document.getElementById('note-content').value = data.content;
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
        const content = document.getElementById('new-note-content').value;
        const folderId = document.querySelector('.folder-toggle').getAttribute('data-folder-id');
        fetch('/api/v1/notes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, content, folder_id: folderId })
        })
        .then(response => response.json())
        .then(() => {
            document.getElementById('new-note-form').style.display = 'none';
            window.location.reload();
        })
        .catch(error => console.error('Error creating note:', error));
    });
}

export function generateNote() {
    document.querySelector('.container').addEventListener('click', function(event) {
        if (event.target.classList.contains('generate-note-btn')) {
            const form = event.target.closest('form');
            const titleInput = form.querySelector('input[type="text"]');
            const contentArea = form.querySelector('textarea');
            const userTitle = titleInput.value;
            const userInput = contentArea.value;
            const folderId = document.querySelector('.folder-toggle').getAttribute('data-folder-id');
            if (!userTitle.trim()) {
                alert('Title is required.');
                return;
            }
            fetch('/api/v1/notes/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title: userTitle, input: userInput, folder_id: folderId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert('Error generating note: ' + data.error);
                } else {
                    contentArea.value = data.content;
                }
            })
            .catch(error => console.error('Error sending to ChatGPT:', error));
        }
    });
}