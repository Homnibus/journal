/** Update the hash corresponding to the id */
function update_note_hash(text, id) {
    // Trim the text so it's the same as in the database
    $('.page-note .id[value=' + id + ']').parent().find('.hash').val(text.trim().hashCode());
}

/** Get the hash corresponding to the id */
function get_note_hash(id) {
    return $('.page-note .id[value=' + id + ']').parent().find('.hash').val();
}

/** Notice the user that the note was saved */
function show_note_save(parent_div) {
    const save_note = parent_div.find('.save-info');
    // Animate the save div
    save_note.fadeIn('slow', function () {
        save_note.fadeOut('slow');
    });
}

/** Notice the user that the note couldn't be saved */
function show_note_error(parent_div, local_error) {
    const error = $('<div class="local-error">').text(local_error);
    parent_div.find('header').append(error);
    parent_div.find('.note_text').addClass('textarea-error');
}

/** Create a new note */
function post_note(parent_div, text) {
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
            if (result.success) {
                // Update the id of the note
                parent_div.find('.id').val(result.id);

                // Update the hash of the text for the next update
                parent_div.find('.hash').val(result.hash);

                // Give a feedback to the user
                show_note_save(parent_div);
            }
            else {
                // Give a feedback to the user
                show_note_error(parent_div, result.local_error);
            }
        },
        error: function (jqXHR, exception) {
            show_error(jqXHR, exception);
        }
    });
}

/** Update a note */
function put_note(parent_div, text, id) {
    const hash = get_note_hash(id);
    // Update the hash of the text for the next update
    update_note_hash(text, id);

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
        success: function (result) {
            hide_error();
            if (result.success) {
                // Give a feedback to the user
                show_note_save(parent_div);
            }
            else {
                // Give a feedback to the user
                show_note_error(parent_div, result.local_error);
            }
        },
        error: function (jqXHR, exception) {
            show_error(jqXHR, exception);
        }
    });
}

/** Delete a note */
function delete_note(parent_div, id) {
    // Delete note from the dom
    parent_div.find('.note_text').remove();

    // Set the csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val()}});
    // Do the ajax call
    $.ajax({
        url: '/notes/' + id,
        data: {},
        dataType: 'json',
        method: 'DELETE',
        success: function (result) {
            hide_error();
            if (result.success) {
                // Give a feedback to the user
                show_note_save(parent_div);
            }
            else {
                // Give a feedback to the user
                show_note_error(parent_div, result.local_error);
            }
        },
        error: function (jqXHR, exception) {
            show_error(jqXHR, exception);
        }
    });
}

/** Do the according rest action on a note */
function post_put_or_delete_note() {
    const parent_div = $(this).closest('.page-note');
    const text = get_text(parent_div.find('.note_text'));
    const id = parent_div.find('.id').attr('value');
    if (text !== '') {
        if (id) {
            put_note(parent_div, text, id);
        }
        else {
            post_note(parent_div, text);
        }
    }
    else {
        delete_note(parent_div, id);
    }
}

/** Do the according rest action on a note */
function put_or_delete_note() {
    const parent_div = $(this).closest('.page-note');
    const text = get_text(parent_div.find('.note_text'));
    const id = parent_div.find('.id').attr('value');
    if (text !== '') {
        put_note(parent_div, text, id);
    }
    else {
        delete_note(parent_div, id);
    }
}
