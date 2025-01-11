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

        