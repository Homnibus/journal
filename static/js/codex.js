$(".old-pages .page-entry:not(:has(.journal_entree_id))").closest(".codex-page").css("flex-direction", "column");

function saveTextarea(){
    var parent_div = $(this).closest(".page-entry")
    var texte = parent_div.find(".journal_entree_texte").val();
    var id = parent_div.find(".journal_entree_id").attr("value");

    $.ajaxSetup({headers: {'X-CSRFToken': $("[name='csrfmiddlewaretoken']").val()}});
    $.ajax({
        url: '/journal/projets/' + $('#slug').val() + 'maj-journal',
        data: {
            'id': id,
            'texte': texte,
        },
        dataType: 'json',
        method: 'POST',
        success: function(data){
            hide_error();
            if(data.success){
                if(data.nouveau_journal){
                    $(".today-page").find(".journal_entree_id").attr('value',data.id);
                }
                //$('.today-entry .journal-entry .save-info').fadeIn('slow', function(){$('.today-entry .journal-entry .save-info').fadeOut('slow');});
                save_journal = $(".journal_entree_id[value = " + data.id + "]").closest(".page-entry").find(".save-info");
                save_journal.fadeIn('slow', function(){
                    save_journal = $(".journal_entree_id[value = " + data.id + "]").closest(".page-entry").find(".save-info");
                    save_journal.fadeOut('slow');
                });
            }
            else{
                $('#id_form-' + form_id + '-id').parent().prepend("<p id='id_form-" + form_id +
                    "-error' class='error'>" + data.form_errors + "</p>");
            }
        },
        error: function (jqXHR, exception) {
            show_error(jqXHR, exception);
        }
    });
}

$(".journal_typewatch").typeWatch( {
    callback: saveTextarea,
    wait: 500,
    highlight: false,
    allowSubmit: false,
    captureLength: 1,
});

function maj_todo(){
    var parent_div = $(this).parent(".task");
    var realisee = parent_div.find(".todo_entree_checkbox").prop('checked');
    var texte = parent_div.find(".todo_entree_texte").val();
    var id = parent_div.find(".todo_entree_id").attr("value");
    if(texte != ''){
        $.ajaxSetup({headers: {'X-CSRFToken': $("[name='csrfmiddlewaretoken']").val()}});
        $.ajax({
            url: '/journal/projets/' + $('#slug').val() + 'maj-todo',
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
                    if(data.nouvelle_tache){
                        //On retire le texte du formulaire initial
                        $('.new-task .todo_entree_texte').val('');
                        //On cherche la celule d'ajout d'une tache
                        var parent_div = $('.today-page .old-tasks');
                        //On ajoute des <div> au formulaire retourné pour pouvoir naviguer dedans avec jquery
                        out_form_str = '<div>' + data.out_form + '</div>'
                        //On ajoute correctement le formulaire de retour en dessous de l'ajout de tache
                        var new_checkbox = $('.todo_entree_checkbox',out_form_str).clone().wrap('<div>').parent().html()
                        var new_textearea = $('.todo_entree_texte',out_form_str).clone().wrap('<div>').parent().html()
                        var new_id = $('.todo_entree_id',out_form_str).clone().wrap('<div>').parent().html()
                        parent_div.prepend(
                            '<article class="task">' +
                            new_checkbox + 
                            new_textearea +
                            new_id +
                            '</article>'
                        );
                        var jqry_textearea = $('.todo_entree_id[value = ' + data.id +']').closest('article').find('.todo_entree_texte');
                        autosize(jqry_textearea);
                        $(jqry_textearea).typeWatch( {
                            callback: maj_todo,
                            wait: 500,
                            highlight: false,
                            allowSubmit: false,
                            captureLength: 1,
                        });
                    }
                    else{
                        //On recherche le div de sauvegarde à faire clignoter
                        save_todo = $(".todo_entree_id[value = " + data.id + "]").closest(".page-tasks").find(".save-info");
                        save_todo.fadeIn('slow', function(){
                            save_todo = $(".todo_entree_id[value = " + data.id + "]").closest(".page-tasks").find(".save-info");
                            save_todo.fadeOut('slow');
                        });
                    }
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

$('.add-item-button').click( maj_todo );

$(document).on('change','.todo_entree_checkbox', maj_todo); 

$(".task:not(.new-task) .todo_entree_texte").typeWatch( {
    callback: maj_todo,
    wait: 500,
    highlight: false,
    allowSubmit: false,
    captureLength: 1,
});

autosize($('.today-page .journal_entree_texte'));