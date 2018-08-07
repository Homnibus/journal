function jq_contains_words(search_words,text_to_search)
{
    //Initalisation des args
    if (search_words === undefined)
    {
        search_words = '';
    }
    if (text_to_search === undefined)
    {
        return false;
    }
    return_value = true;
    search_words_list = search_words.split(" ");
    //Recherche de la liste des mots dans le texte
    for (word_id in search_words_list)
    {
        return_value = return_value && text_to_search.toLowerCase().indexOf(search_words_list[word_id].toLowerCase()) !== -1;
    }
    //On retourne la valeur
    return return_value;
}

function codex_search()
{
    search_words = $(this).val();
    $('.derniers-codex .titre').filter(function(){return jq_contains_words(search_words,$(this).text());}).closest('.codex').show();
    $('.derniers-codex .titre').filter(function(){return !jq_contains_words(search_words,$(this).text());}).closest('.codex').hide();
}

$('.codex-search').typeWatch( {
    callback: codex_search,
    wait: 350,
    highlight: false,
    allowSubmit: false,
    captureLength: 1,
});