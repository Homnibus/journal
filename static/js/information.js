/** Get the hash corresponding to the id */
function get_information_hash() {
    return $('.information .hash').val();
}

/** Notice the user that the information couldn't be saved */
function show_information_error(information, jqXHR, exception) {
    const information_text = information.find('.information__text');
    const information_header = information.find('header');
    show_not_saved();
    show_element_error(information_text, information_header, jqXHR, exception);

}

/** Create the information text */
function post_information(information, text) {
    // Give a feedback to the user that there is a save being done.
    show_save();
    // Set the csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': CSRF_TOKEN}});
    // Do the ajax call
    return $.ajaxq('InformationQueueCreation', {
        url: '/codex/' + SLUG + '/informations',
        data: {
            'text': text,
            'codex_slug': SLUG,
        },
        dataType: 'json',
        method: 'POST',
    }).success(function (result) {
        // Update the hash and the id for the next update
        update_hash_and_id(information, result.hash, result.id);
    }).error(function (jqXHR, exception) {
        // Give a feedback to the user
        show_information_error(information, jqXHR, exception)
    }).success(function () {
        // Give a feedback to the user that the saving ended.
        hide_save();
    });

}

/** Update the information text */
function put_information(information, text) {
    const hash = get_information_hash();
    // Update the hash of the text for the next update
    update_hash(information, text);

    // Give a feedback to the user that there is a save being done.
    show_save();
    // Set the csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': CSRF_TOKEN}});
    // Do the ajax call
    return $.ajaxq('InformationQueue', {
        url: '/codex/' + SLUG + '/information',
        data: {
            'text': text,
            'hash': hash,
        },
        dataType: 'json',
        method: 'PUT',
    }).error(function (jqXHR, exception) {
        // If the user is not authenticated, redirect to the connexion page
        if (jqXHR.status === 401) {
            window.location.replace(jqXHR.responseJSON.connexion_url + "?next=" + window.location.pathname);
        }
        // Give a feedback to the user
        show_information_error(information, jqXHR, exception)
    }).success(function () {
        // Give a feedback to the user that the saving ended.
        hide_save();
    });
}

/** Do the according rest action on a information */
function post_or_put_information() {
    const information = $(this).closest('.information');
    const text = get_text(information.find('.information__text'));
    const id = information.find('.id').attr('value');
    if (text !== '') {
        if (id) {
            return put_information(information, text);
        }
        else {
            return post_information(information, text);
        }
    }
}

autosize($('.information__text'));

$('.information__text').typeWatch({
    callback: post_or_put_information,
    wait: 500,
    highlight: false,
    allowSubmit: false,
    captureLength: 1,
});