/** Notice the user that the note was saved */
function show_note_save(note) {
    const save_note = note.parent().find('.save-info');
    // Animate the save div
    save_note.fadeIn('slow', function () {
        save_note.fadeOut('slow');
    });
}

/** Notice the user that the note couldn't be saved */
function show_note_error(note, jqXHR, exception) {
    hide_error();
    if (jqXHR.status !== 400) {
        show_error(jqXHR, exception);
    }
    const result = jqXHR.responseJSON;
    const nb_global_error = result.form_errors.length;
    for (let i = 0; i < nb_global_error; i++) {
        const error = $('<div class="error">').text(result.form_errors[i]);
        note.closest('.page__note-section').find('header').after(error);
        note.find('.note__text').addClass('textarea-error');
    }
    jQuery.each(result.fields_error, function (field, error_list) {
        const nb_error = error_list.length;
        for (let i = 0; i < nb_error; i++) {
            const error = $('<div class="local-error">').text(error_list[i]);
            note.closest('.page__note-section').find('header').after(error);
            note.find('.note__text').addClass('textarea-error');
        }
    });
    if (nb_global_error === 0 && jQuery.isEmptyObject(result.fields_error)) {
        show_error(jqXHR, exception);
    }
}

/** Create a new note */
function post_note(note, text) {
    // Set the csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val()}});
    // Do the ajax call
    $.ajax({
        url: '/codex/' + $('#slug').val() + '/notes',
        data: {
            'text': text,
        },
        dataType: 'json',
        method: 'POST',
        success: function (result) {
            hide_error();
            // Update the id of the note
            note.find('.id').val(result.id);

            // Update the hash of the text for the next update
            note.find('.hash').val(result.hash);

            // Give a feedback to the user
            show_note_save(note);
        },
        error: function (jqXHR, exception) {
            // Give a feedback to the user
            show_note_error(note, jqXHR, exception);
        }
    });
}

/** Update a note */
function put_note(note, text, id, hash) {

    // Update the hash of the text for the next update
    note.find('.hash').val(text.trim().hashCode());

    // Set the csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val()}});
    // Do the ajax call
    $.ajax({
        url: '/notes/' + id,
        data: {
            'text': text,
            'hash': hash,
        },
        dataType: 'json',
        method: 'PUT',
        success: function () {
            hide_error();
            // Give a feedback to the user
            show_note_save(note);
        },
        error: function (jqXHR, exception) {
            // Give a feedback to the user
            show_note_error(note, jqXHR, exception);
        }
    });
}

/** Delete a note */
function delete_note(note, id, hash) {
    // Hide the note from so it can't be update after sending the delete request to the server
    if (!note.closest(".page").hasClass("page--today")) {
        note.hide()
    }
    else {
        // Update the id of the note
        note.find('.id').val("");

        // Update the hash of the text for the next update
        note.find('.hash').val("");
    }

    // Set the csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val()}});
    // Do the ajax call
    $.ajax({
        url: '/notes/' + id,
        data: {
            'hash': hash,
        },
        dataType: 'json',
        method: 'DELETE',
        success: function () {
            hide_error();
            // Give a feedback to the user
            show_note_save(note);
            // Delete note from the dom if it's not the note of the day
            if (!note.closest(".page").hasClass("page--today")) {
                note.remove();
            }

        },
        error: function (jqXHR, exception) {
            // Give a feedback to the user
            show_note_error(note, jqXHR, exception);
            if (note.closest(".page").hasClass("page--today")) {
                note.show();
            }

        }
    });
}

/** Do the according rest action on a note */
function post_put_or_delete_note() {
    const note = $(this).closest('.note');
    const text = get_text(note.find('.note__text'));
    const id = note.find('.id').attr('value');
    const hash = note.find('.hash').val();
    if (text !== '') {
        if (id) {
            put_note(note, text, id, hash);
        }
        else {
            post_note(note, text);
        }
    }
    else {
        delete_note(note, id, hash);
    }
}

/** Do the according rest action on a note */
function put_or_delete_note() {
    const note = $(this).closest('.note');
    const text = get_text(note.find('.note__text'));
    const id = note.find('.id').attr('value');
    const hash = note.find('.hash').val();
    if (text !== '') {
        put_note(note, text, id);
    }
    else {
        delete_note(note, id, hash);
    }
}
