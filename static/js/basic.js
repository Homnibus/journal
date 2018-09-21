function hide_error() {
    $('.error').remove();
    $('.nav-filler').removeAttr('style');
}

function show_error(jqXHR, exception) {
    hide_error();
    var data = jQuery.parseJSON(jqXHR.responseText);
    $('nav').append("<div class='error'>" + 
        "<div style='color:red'>Erreur " + jqXHR.status + " : " + data.message + 
        " -- " + data.explanation + "</div>" + 
        "</div>"
    );
    $('.nav-filler').css('margin-top','+=1em');
}

function get_text(element) {
    var text =  '';
    if (element.is('textarea')) {
        text = element.val();
    } else {
        text = element.text();        
    }
    return text
}