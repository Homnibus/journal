function put_tache(parent_div,realisee,texte,id){
    //Mise à jour d'une nouvelle Tache
    $.ajaxSetup({headers: {'X-CSRFToken': $("[name='csrfmiddlewaretoken']").val()}});
    $.ajax({
        url: '/projets/' + $('#slug').val() + 'rest-tache',
        data: {
            'todo_id': id,
            'texte': texte,
            'realisee': realisee,
        },
        dataType: 'json',
        method: 'PUT',
        success: function(data) {
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
                error_todo = $('.todo_entree_id[value = ' + data.id + ']').closest('table').parent();
                error_todo.prepend('<p id="maj_todo-error" class="error">' + data.form_errors + '</p>');
            }
        },
        error: function (jqXHR, exception) {
            show_error(jqXHR, exception);
        }
    });
}

function delete_tache(parent_div,id){
    //Supprime une Tache
    $.ajaxSetup({headers: {'X-CSRFToken': $("[name='csrfmiddlewaretoken']").val()}});
    $.ajax({
        url: '/projets/' + $('#slug').val() + 'rest-tache',
        data: {
            'todo_id': id,
        },
        dataType: 'json',
        method: 'DELETE',
        success: function(data) {
            hide_error();
            if(data.success){
                //On surprime la tache du DOM
                parent_div.remove()
            }
            else{
                error_todo = $('.todo_entree_id[value = ' + data.id + ']').closest('table').parent();
                error_todo.prepend('<p id="maj_todo-error" class="error">' + data.form_errors + '</p>');
            }
        },
        error: function (jqXHR, exception) {
            show_error(jqXHR, exception);
        }
    });
}

function put_or_delete_tache(){
    var parent_div = $(this).closest('.task_view');
    var realisee = parent_div.find('.todo_entree_checkbox').prop('checked');
    var texte = get_text(parent_div.find('.todo_entree_texte'));
    var id = parent_div.find('.todo_entree_id').attr('value');
    if(texte != ''){
        put_tache(parent_div,realisee,texte,id);
    }
    else{
        delete_tache(parent_div,id);
    }
}

$(document).on('change','.todo_entree_checkbox',put_or_delete_tache); 
