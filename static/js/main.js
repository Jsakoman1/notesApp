import { showNoteContent, createNewNote, generateNote } from './noteActions.js';
import { createFolder, editFolder, deleteFolder } from './folderActions.js';
import { handleSaveNote } from './formHandler.js';
import { handleDragStart, handleDragEnd, handleDragOver, handleDragLeave, handleDrop } from './dragActions.js'; // Or from './dragDrop.js'

// Call the functions to initialize the app
showNoteContent();
createNewNote();
generateNote();
createFolder();
handleSaveNote();

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
});

document.addEventListener('DOMContentLoaded', function () {
    // Add drag and drop listeners to the notes
    const notes = document.querySelectorAll('.note');
    notes.forEach(note => {
        note.addEventListener('dragstart', handleDragStart);
        note.addEventListener('dragend', handleDragEnd);
    });

    // Add drag and drop listeners to the folders
    const folders = document.querySelectorAll('.folder');
    folders.forEach(folder => {
        folder.addEventListener('dragover', handleDragOver);
        folder.addEventListener('dragleave', handleDragLeave);
        folder.addEventListener('drop', handleDrop);
    });
});