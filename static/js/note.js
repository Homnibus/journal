/** Notice the user that the note couldn't be saved */
function show_note_error(note, jqXHR, exception) {
    const note_text = note.find('.note__text');
    const note_header = note.closest('.page__note-section').find('header');
    show_not_saved();
    show_element_error(note_text, note_header, jqXHR, exception);
}

/** Create a new note */
function post_note(note, text) {
    // Give a feedback to the user that there is a save being done.
    show_save();
    // Set the csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': CSRF_TOKEN}});
    // Do the ajax call
    return $.ajaxq('NoteQueueCreation', {
        url: '/codex/' + SLUG + '/notes',
        data: {
            'text': text,
        },
        dataType: 'json',
        method: 'POST',
    }).success(function (result) {
        // Update the hash and the id for the next update
        update_hash_and_id(note, result.hash, result.id);
    }).error(function (jqXHR, exception) {
        // Give a feedback to the user
        show_note_error(note, jqXHR, exception);
    }).success(function () {
        // Give a feedback to the user that the saving ended.
        hide_save();
    });
}

/** Update a note */
function put_note(note, text, id, hash) {
    // Update the hash of the text for the next update
    update_hash(note, text);

    // Give a feedback to the user that there is a save being done.
    show_save();
    // Set the csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': CSRF_TOKEN}});
    // Do the ajax call
    return $.ajaxq('NoteQueue' + id, {
        url: '/notes/' + id,
        data: {
            'text': text,
            'hash': hash,
        },
        dataType: 'json',
        method: 'PUT',
    }).error(function (jqXHR, exception) {
        // Give a feedback to the user
        show_note_error(note, jqXHR, exception);
    }).success(function () {
        // Give a feedback to the user that the saving ended.
        hide_save();
    });
}

/** Delete a note */
function delete_note(note, id, hash) {
    // Hide the note from so it can't be update after sending the delete request to the server
    if (!note.closest(".page").hasClass("page--today")) {
        note.hide()
    }
    else {
        reset_hash_and_id(note);
    }

    // Give a feedback to the user that there is a save being done.
    show_save();
    // Set the csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': CSRF_TOKEN}});
    // Do the ajax call
    return $.ajaxq('NoteQueue' + id, {
        url: '/notes/' + id,
        data: {
            'hash': hash,
        },
        dataType: 'json',
        method: 'DELETE',
    }).success(function () {
        // Delete note from the dom if it's not the note of the day
        if (!note.closest(".page").hasClass("page--today")) {
            note.remove();
        }
    }).error(function (jqXHR, exception) {
        // Give a feedback to the user
        show_note_error(note, jqXHR, exception);
        if (note.closest(".page").hasClass("page--today")) {
            note.show();
        }
    }).success(function () {
        // Give a feedback to the user that the saving ended.
        hide_save();
    });
}

/** Do the according rest action on a note */
function post_put_or_delete_note() {
    const note = $(this).closest('.note');
    // if the parent note is empty because it does not exist anymore, return
    if (note.length === 0) {
        return;
    }

    const text = get_text(note.find('.note__text'));
    const id = note.find('.id').attr('value');
    const hash = note.find('.hash').val();

    if (text !== '') {
        if (id) {
            return put_note(note, text, id, hash);
        }
        else {
            return post_note(note, text);
        }
    }
    else {
        return delete_note(note, id, hash);
    }
}

/** Do the according rest action on a note */
function put_or_delete_note() {
    const note = $(this).closest('.note');
    // if the parent note is empty because it does not exist anymore, return
    if (note.length === 0) {
        return
    }

    const text = get_text(note.find('.note__text'));
    const id = note.find('.id').attr('value');
    const hash = note.find('.hash').val();

    if (text !== '') {
        return put_note(note, text, id, hash);
    }
    else {
        return delete_note(note, id, hash);
    }
}
