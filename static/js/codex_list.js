/** Return True if at least one of the search word is present inside a given text*/
function jq_contains_words(search_words, text_to_search) {
    // Args initialisation
    if (search_words === undefined) {
        search_words = '';
    }
    if (text_to_search === undefined) {
        return false;
    }
    let return_value = true;
    const search_words_list = search_words.split(" ");

    // Look for the different string in the given text
    for (const word of search_words_list) {
        return_value = return_value && text_to_search.toLowerCase().indexOf(word.toLowerCase()) !== -1;
    }

    return return_value;
}

/** Filter codex given a list of words*/
function codex_search() {
    const search_words = $(this).val();

    // Find the corresponding codex
    const codex_list = $('.codex-list .codex__title');
    const matched_codex = codex_list.filter(function () {
        return jq_contains_words(search_words, $(this).text());
    }).closest('.codex__link');
    const unmatched_codex = codex_list.filter(function () {
        return !jq_contains_words(search_words, $(this).text());
    }).closest('.codex__link');

    // Add the class to save the current state
    const codex_was_hide = $('.codex--hide').length;
    matched_codex.removeClass('codex--hide');
    unmatched_codex.addClass('codex--hide');

    // Apply the visual effect
    let codex_to_hide = $('.codex__link');
    if (codex_was_hide === 0 && unmatched_codex.length === 0) {
        codex_to_hide = $();
    }

    Promise.all([
        $('.codex__not-found').fadeOut(100).promise(),
        codex_to_hide.fadeOut(100).promise()
    ]).then(function () {
        if (matched_codex.length === 0) {
            $('.codex__not-found').fadeIn(100);
        } else {
            matched_codex.fadeIn(100);
        }
    });
}

$('.codex-search_input').typeWatch({
    callback: codex_search,
    wait: 350,
    highlight: false,
    allowSubmit: false,
    captureLength: 1,
});