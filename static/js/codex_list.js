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
    const codex_list = $('.codex-list .title');
    codex_list.filter(function () {
        return jq_contains_words(search_words, $(this).text());
    }).closest('.codex').show();
    codex_list.filter(function () {
        return !jq_contains_words(search_words, $(this).text());
    }).closest('.codex').hide();
}

$('.codex-search').typeWatch({
    callback: codex_search,
    wait: 350,
    highlight: false,
    allowSubmit: false,
    captureLength: 1,
});