autosize(document.querySelectorAll('textarea'));

function saveTextarea(){
    var textarea = $('#id_texte').val();
    $.ajaxSetup({headers: {"X-CSRFToken": $("[name='csrfmiddlewaretoken']").val()}});
    $.ajax({
        url: '/journal/projets/' + $('#slug').val() + 'maj-main-courante',
        data: {
            'texte': textarea
        },
        dataType: 'json',
        method: 'POST',
        success: function(data){
          if(data.success){
            $('.error').remove();
            $('header').css('margin-top', '30px');
            $('#derniere_maj').text(data.date_update);
            $('#sauvegarde').fadeIn("slow", function(){$('#sauvegarde').fadeOut("slow");});
          }
        },
        error: function (jqXHR, exception) {
            var data = jQuery.parseJSON(jqXHR.responseText);
            $('.error').remove();
            $('nav').append("<span class='error'>" + 
                "<span style='color:red'>Erreur " + jqXHR.status + " : " + data.message + "</span>" + 
                "<br/>" +
                "<span style='color:red'>" + data.explanation + "</span>" + 
                "</span>"
            );
            $('header').css('margin-top', '75px');
        }
    });
}

$("#id_texte").typeWatch( {
    callback: saveTextarea,
    wait: 500,
    highlight: false,
    allowSubmit: false,
    captureLength: 1,
});