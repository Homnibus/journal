autosize($('.information_text'));

/** Notice the user that the information was saved */
function show_information_save() {
    const save_information = $('.information .save-info');
    // Animate the save div
    save_information.fadeIn('slow', function () {
        save_information.fadeOut('slow');
    });
}

/** Save the information text */
function save_information() {
    const text = $('.information_text').val();
    // Set the csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val()}});
    // Do the ajax call
    $.ajax({
        url: '/codex/' + $('#slug').val() + 'information',
        data: {
            'text': text
        },
        dataType: 'json',
        method: 'POST',
        success: function (data) {
            if (data.success) {
                hide_error();

                // Give a success feedback to the user
                show_information_save()
            }
        },
        error: function (jqXHR, exception) {
            show_error(jqXHR, exception);
        }
    });
}

$('.information_text').typeWatch({
    callback: save_information,
    wait: 500,
    highlight: false,
    allowSubmit: false,
    captureLength: 1,
});