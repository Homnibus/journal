const SLUG = $('#slug').val();
const CSRF_TOKEN = $('[name="csrfmiddlewaretoken"]').val();

function hide_error() {
    $('.error').remove();
    $('.local-error').remove();
    $('.nav-filler').removeAttr('style');
    $('.textarea-error').removeClass('textarea-error');
}

function show_error(jqXHR) {
    hide_error();
    const data = jQuery.parseJSON(jqXHR.responseText);
    $('.menu__under').after("<div class='error'>" +
        "Erreur " + jqXHR.status + " : " + data.message +
        " -- " + data.explanation +
        "</div>"
    );
}

function show_element_error(element, element_header, jqXHR, exception) {
    hide_error();
    if (jqXHR.status !== 400) {
        show_error(jqXHR, exception);
    }
    const result = jqXHR.responseJSON;
    const nb_global_error = result.form_errors.length;
    for (let i = 0; i < nb_global_error; i++) {
        const error = $('<div class="error">').text(result.form_errors[i]);
        element_header.after(error);
        element.addClass('textarea-error');
    }
    jQuery.each(result.fields_error, function (field, error_list) {
        const nb_error = error_list.length;
        for (let i = 0; i < nb_error; i++) {
            const error = $('<div class="local-error">').text(error_list[i]);
            element_header.after(error);
            element.addClass('textarea-error');
        }
    });
    if (nb_global_error === 0 && jQuery.isEmptyObject(result.fields_error)) {
        show_error(jqXHR, exception);
    }
}

function show_element_save(element) {
    hide_error();
    const save_div = element.parent().find('.save-info');
    // Animate the save div
    save_div.fadeIn('slow', function () {
        save_div.fadeOut('slow');
    });
}

function get_text(element) {
    let text = '';
    if (element.is('textarea')) {
        text = element.val();
    } else {
        text = element.text();
    }
    return text
}

String.prototype.hashCode = function () {
    let hash = 0;
    if (this.length === 0) return hash;
    for (let i = 0; i < this.length; i++) {
        const char = this.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return hash;
};

function update_hash(element, text) {
    element.find('.hash').val(text.trim().hashCode());
}

function update_hash_and_id(element, hash, id) {
    element.find('.id').val(id);
    element.find('.hash').val(hash);
}

function reset_hash_and_id(element) {
    element.find('.id').val("");
    element.find('.hash').val("");
}