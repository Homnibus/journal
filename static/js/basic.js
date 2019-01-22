function hide_error() {
    $('.error').remove();
    $('.local-error').remove();
    $('.nav-filler').removeAttr('style');
    $('.textarea-error').removeClass('textarea-error');
}

function show_error(jqXHR, exception) {
    hide_error();
    var data = jQuery.parseJSON(jqXHR.responseText);
    $('nav').append("<div class='error'>" +
        "<div style='color:red'>Erreur " + jqXHR.status + " : " + data.message +
        " -- " + data.explanation + "</div>" +
        "</div>"
    );
    $('.nav-filler').css('margin-top', '+=1em');
}

function get_text(element) {
    var text = '';
    if (element.is('textarea')) {
        text = element.val();
    } else {
        text = element.text();
    }
    return text
}

String.prototype.hashCode = function () {
    var hash = 0;
    if (this.length == 0) return hash;
    for (i = 0; i < this.length; i++) {
        char = this.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return hash;
};