/** Update the hash corresponding to the id */
function update_information_hash(text) {
    // Trim the text so it's the same as in the database
    $('.information .hash').val(text.trim().hashCode());
}

/** Get the hash corresponding to the id */
function get_information_hash() {
    return $('.information .hash').val();
}

/** Notice the user that the information couldn't be saved */
function show_information_error(parent_div, jqXHR, exception) {
    hide_error();
    if (jqXHR.status !== 400) {
        show_error(jqXHR, exception);
    }
    const result = jqXHR.responseJSON;
    const nb_global_error = result.form_errors.length;
    for (let i = 0; i < nb_global_error; i++) {
        const error = $('<div class="error">').text(result.form_errors[i]);
        parent_div.find('header').after(error);
        parent_div.find('.information_text').addClass('textarea-error');
    }
    jQuery.each(result.fields_error, function (field, error_list) {
        const nb_error = error_list.length;
        for (let i = 0; i < nb_error; i++) {
            const error = $('<div class="local-error">').text(error_list[i]);
            parent_div.find('header').after(error);
            parent_div.find('.note_text').addClass('textarea-error');
        }
    });
    if (nb_global_error === 0 && jQuery.isEmptyObject(result.fields_error)) {
        show_error(jqXHR, exception);
    }
}

/** Notice the user that the information was saved */
function show_information_save() {
    const save_information = $('.information .save-info');
    // Animate the save div
    save_information.fadeIn('slow', function () {
        save_information.fadeOut('slow');
    });
}

/** Save the information text */
function post_information(parent_div, text) {
    const codex_slug = $('#slug').val();
    // Set the csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val()}});
    // Do the ajax call
    $.ajax({
        url: '/codex/' + codex_slug + 'informations',
        data: {
            'text': text,
            'codex_slug': codex_slug,
        },
        dataType: 'json',
        method: 'POST',
        success: function (result) {
            hide_error();
            // Update the id of the information
            $('.information .id').val(result.id);

            // Update the hash of the text for the next update
            $('.information .hash').val(result.hash);

            // Give a success feedback to the user
            show_information_save()
        },
        error: function (jqXHR, exception) {
            // Give a feedback to the user
            show_information_error(parent_div, jqXHR, exception)
        }
    });
}


/** Save the information text */
function put_information(parent_div, text) {
    const hash = get_information_hash();
    // Update the hash of the text for the next update
    update_information_hash(text);

    // Set the csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val()}});
    // Do the ajax call
    $.ajax({
        url: '/codex/' + $('#slug').val() + 'information',
        data: {
            'text': text,
            'hash': hash,
        },
        dataType: 'json',
        method: 'PUT',
        success: function () {
            hide_error();
            // Give a success feedback to the user
            show_information_save()
        },
        error: function (jqXHR, exception) {
            // Give a feedback to the user
            show_information_error(parent_div, jqXHR, exception)
        }
    });
}

/** Do the according rest action on a information */
function post_or_put_information() {
    const parent_div = $(this).closest('.information');
    const text = get_text(parent_div.find('.information_text'));
    const id = parent_div.find('.id').attr('value');
    if (text !== '') {
        if (id) {
            put_information(parent_div, text);
        }
        else {
            post_information(parent_div, text);
        }
    }
}

autosize($('.information_text'));

$('.information_text').typeWatch({
    callback: post_or_put_information,
    wait: 500,
    highlight: false,
    allowSubmit: false,
    captureLength: 1,
});