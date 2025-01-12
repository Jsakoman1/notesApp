export function handleSaveNote() {
    document.querySelector('.container').addEventListener('click', function(event) {
        if (event.target.classList.contains('save-note-btn')) {
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
            fetch('/api/v1/notes/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title: userTitle, input: userInput, folder_id: folderId })
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
}