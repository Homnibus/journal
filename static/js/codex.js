function enable_edit_page()
{
    var parent_div = $(this).closest(".page-entry");
    var texte = get_text(parent_div.find(".journal_entree_texte"));
    var editableText = $('<textarea class="journal_entree_texte journal_typewatch" />');
    var id = parent_div.find(".journal_entree_id").attr("value");
    
    //Seting the text hash before it can be modifed
    update_page_hash(texte,id)

    //Replace <div> with <textarea>
    editableText.val(texte);
    parent_div.find(".journal_entree_texte").replaceWith(editableText);
    
    //Set focus
    editableText.focus();
    editableText.get(0).setSelectionRange(0, 0);
    
    //Set typeWatch
    editableText.typeWatch( {
        callback: put_or_delete_page,
        wait: 500,
        highlight: false,
        allowSubmit: false,
        captureLength: 1,
    });
    
    //setup the blur event for this new textarea
    editableText.blur(disable_edit_page);
    
    //setup autosize
    autosize(editableText);
    
    //hide the pencil
    parent_div.find('.edit-pen').hide();
}

function disable_edit_page() {
    //Before disabling the texarea, we save it
    put_or_delete_page.call(this);
    var html_content = $(this).val();
    var viewableText = $('<pre class="journal_entree_texte disabled-textarea"/>');
    viewableText.text(html_content);
    $(this).replaceWith(viewableText);
    //show the pencil again
    viewableText.closest('.page-entry').find('.edit-pen').show(); 
}

function enable_edit_task() {
    //get the list of the task that we need to update
    console.log('enable_edit_task :: ' + $(this).html());
    var task_list = $(this).closest('.page-tasks').find('.task-list .todo_entree_texte');
    task_list.each(function(index){
        console.log(index + ' :: ' + $(this).html());
        var parent_div = $(this)
        var texte = get_text(parent_div);
        var id = parent_div.closest('.task').find('.todo_entree_id').attr('value');
        
        console.log("id :" + id);

        //update the task hash
        update_task_hash(texte,id);
        console.log("hash :" + texte.hashCode());
        
        //replace the div by an editable textarea
        var editableText = $('<textarea class="todo_entree_texte todo_typewatch" />');
        editableText.val(texte);
        parent_div.replaceWith(editableText);
        
        //setup typeWatch
        editableText.typeWatch( {
            callback: put_or_delete_tache,
            wait: 500,
            highlight: false,
            allowSubmit: false,
            captureLength: 1,
        });
        
        //setup autosize
        autosize(editableText);
    });
    //hide the pencil
    task_list.find('.edit-pen').hide();
}

$(document).ready(function(){
    //Maj of today_page hash after loading page
    var today_page_id = $(".today-page .journal_entree_id").attr('value');
    if( today_page_id !== undefined ){
        page_hash[today_page_id] = $(".journal_entree_id[value = " + today_page_id + "]").closest(".page-entry").find(".journal_entree_texte").val().trim().hashCode();
    }
    //When done, we set the textarea editable
    $('.today-page .journal_entree_texte').removeAttr('readonly');
});

$(document).ready(function(){
    //Maj of today_task hash after loading page
    var today_task_list = $(".today-page .old-tasks");
    enable_edit_task.call(today_task_list);
});

$(document).on('click','.page-entry .edit-pen',enable_edit_page);

$(document).on('click','.page-tasks .edit-pen',enable_edit_task);

$(document).on('click','.add-item-button:not(.unclickable)',function(){
    // On pose la classe 'unclickable" pour empécher la multi soumission
    $(this).addClass('unclickable');
    post_tache.call(this);
});

$(document).on('change','.todo_entree_checkbox', put_or_delete_tache);  


$(document).on("keypress",'.journal_entree_texte:not(disabled-textarea)',
    function (e){
        //Si on appuis sur TAB
        if (e.keyCode == 9) {
            e.preventDefault();
            var start = this.selectionStart;
            var end = this.selectionEnd;

            // set textarea value to: text before caret + tab + text after caret
            $(this).val($(this).val().substring(0, start)
                        + "\t"
                        + $(this).val().substring(end)
                        );

            // put caret at right position again
            this.selectionStart = start +1;
            this.selectionEnd = start + 1;
        } 
        //Sinon on ne fait rien
    }
);

$(".journal_typewatch").typeWatch( {
    callback: post_put_or_delete_page,
    wait: 500,
    highlight: false,
    allowSubmit: false,
    captureLength: 1,
});

$(".task:not(.new-task) .todo_entree_texte").typeWatch( {
    callback: put_or_delete_tache,
    wait: 500,
    highlight: false,
    allowSubmit: false,
    captureLength: 1,
});

autosize($('.today-page .journal_entree_texte'));