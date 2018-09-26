function maj_todo(){
    var parent_div = $(this).closest(".task");
    var realisee = parent_div.find(".todo_entree_checkbox").prop('checked');
    var texte = parent_div.find(".task-texte").text();
    var id = parent_div.find(".todo_entree_id").attr("value");
    if(texte != ''){
        $.ajaxSetup({headers: {'X-CSRFToken': $("[name='csrfmiddlewaretoken']").val()}});
        $.ajax({
            url: '/projets/' + $('#slug').val() + 'maj-todo',
            data: {
                'todo_id': id,
                'texte': texte,
                'realisee': realisee,
            },
            dataType: 'json',
            method: 'POST',
            success: function(data){
                hide_error();
                if(data.success){
                    //On recherche le div de sauvegarde à faire clignoter
                    save_todo = $(".save-info");
                    save_todo.fadeIn('slow', function(){
                        save_todo = $(".save-info");
                        save_todo.fadeOut('slow');
                    });
                }
                else{
                    error_todo = $(".todo_entree_id[value = " + data.id + "]").closest("table").parent();
                    error_todo.prepend("<p id='maj_todo-error' class='error'>" + data.form_errors + "</p>");
                }
            },
            error: function (jqXHR, exception) {
                show_error(jqXHR, exception);
            }
        });
    }    
}

$(document).on('change','.todo_entree_checkbox',maj_todo); 

$(".todo_entree_texte").typeWatch( {
    callback: maj_todo,
    wait: 500,
    highlight: false,
    allowSubmit: false,
    captureLength: 1,
});

autosize($('textarea'));