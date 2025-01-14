import { handleDragStart, handleDragEnd, handleDragOver, handleDragLeave, handleDrop } from './dragDrop.js';
import { showNoteContent, createNewNote, generateNote, handleSaveNote, handleSaveEditedNote, deleteNote } from './noteActions.js';
import { createFolder, editFolder, deleteFolder } from './folderActions.js';

// Call the functions to initialize the app
showNoteContent();
createNewNote();
generateNote();
createFolder();
handleSaveNote();
handleSaveEditedNote();

document.querySelector('.container').addEventListener('click', function(event) {
    // Handle folder actions (edit, delete)
    if (event.target.classList.contains('edit-folder-btn')) {
        const folderId = event.target.getAttribute('data-folder-id');
        editFolder(folderId);
    } else if (event.target.classList.contains('delete-folder-btn')) {
        const folderId = event.target.getAttribute('data-folder-id');
        deleteFolder(folderId);
    }

    // Handle note click to show note content
    if (event.target.classList.contains('note')) {
        const noteId = event.target.getAttribute('data-note-id');
        showNoteContent(noteId); // Show note in the editor
    }
    // Handle note deletion
    if (event.target.classList.contains('delete-note-btn')) {
        const noteId = event.target.getAttribute('data-note-id');
        if (noteId) {
            deleteNote(noteId); // Call the delete function
        }
    }
});

document.addEventListener('DOMContentLoaded', function () {
    // Add drag and drop listeners to the notes
    const notes = document.querySelectorAll('.note');
    notes.forEach(note => {
        note.addEventListener('dragstart', handleDragStart);
        note.addEventListener('dragend', handleDragEnd);
    });

    // Add drag and drop listeners to folders
    const folders = document.querySelectorAll('.folder');
    folders.forEach(folder => {
        folder.addEventListener('dragover', handleDragOver);
        folder.addEventListener('dragleave', handleDragLeave);
        folder.addEventListener('drop', handleDrop);
    });
});