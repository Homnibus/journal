autosize(document.querySelectorAll('textarea'));

function saveTextarea(){
    var textarea = $('#id_texte').val();
    $.ajaxSetup({headers: {"X-CSRFToken": $("[name='csrfmiddlewaretoken']").val()}});
    $.ajax({
        url: '/journal/projets/' + $('#slug').val() + 'maj-contact',
        data: {
            'texte': textarea
        },
        dataType: 'json',
        method: 'POST',
        success: function(data){  
          if(data.success){
            hide_error();
            $('.general-info h2').text(data.date_update);
            $('#sauvegarde').fadeIn("slow", function(){$('#sauvegarde').fadeOut("slow");});
          }
        },
        error: function (jqXHR, exception) {
            show_error(jqXHR, exception);
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