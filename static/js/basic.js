const SLUG = $('#slug').val();
const CSRF_TOKEN = $('[name="csrfmiddlewaretoken"]').val();

function hide_error() {
    $('.error').remove();
    $('.local-error').remove();
    $('.nav-filler').removeAttr('style');
    $('.textarea-error').removeClass('textarea-error');
    $('.save-info__not-saved-image').fadeOut(0);
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
            const error = $('<div class="local-error">').text(error_list[i] + " ( field: " + field + ")");
            element_header.after(error);
            element.addClass('textarea-error');
        }
    });
    if (nb_global_error === 0 && jQuery.isEmptyObject(result.fields_error)) {
        show_error(jqXHR, exception);
    }
}

function show_save() {
    hide_error();
    $('.save-info__saving-image').stop(true).fadeIn('slow');
}

function hide_save() {
    if ($.ajaxq.queueLength() === 1) {
        $('.save-info__saving-image').fadeOut('slow');
    }
}

function show_not_saved() {
    $('.save-info__saving-image').fadeOut(0);
    $('.save-info__not-saved-image').fadeIn(0);
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
