page_hash={};

function update_page_hash(texte,id){
//Update the hash corresponding to the id//  
    //trim the text so it's the same as in the database
    page_hash[id] = texte.trim().hashCode();
}

function show_page_save(parent_div){
//Notice the user that the page was saved//
    var save_journal = parent_div.find('.save-info');
    //animate the save div
    save_journal.fadeIn('slow', function(){
        save_journal.fadeOut('slow');
    });    
}

function show_page_error(parent_div,local_error){
//Notice the user that the page couldn't be saved
    var error = $('<div class="local-error">').text(local_error); 
    parent_div.find('header').append(error);
    parent_div.find('.journal_entree_texte').addClass('textarea-error');
}                  

function post_page(parent_div,texte){
//Create a new page//
    //setup csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': $("[name='csrfmiddlewaretoken']").val()}});
    //setup ajax call
    $.ajax({
        url: '/projets/' + $('#slug').val() + 'rest-page',
        data: {
            'texte': texte,
        },
        dataType: 'json',
        method: 'POST',
        success: function(result) {
            
            hide_error();
            if(result.success){
                //update the id of the page
                parent_div.find(".journal_entree_id").attr('value',result.id);
                
                //update the hash of the text for the next update
                update_page_hash(texte,result.id);
                
                //give a feedback to the user
                show_page_save(parent_div);
            }
            else{
                //give a feedback to the user
                show_page_error(parent_div,result.local_error);
            }
        },
        error: function (jqXHR, exception) {
            show_error(jqXHR, exception);
        }
    });
}

function put_page(parent_div,texte,id){
//Update a page//

    var hash = page_hash[id];
    //update the hash of the text for the next update
    update_page_hash(texte,id);

    //setup csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': $("[name='csrfmiddlewaretoken']").val()}});
    //setup ajax call
    $.ajax({
        url: '/projets/' + $('#slug').val() + 'rest-page',
        data: {
            'id': id,
            'texte': texte,
            'hash':hash,
        },
        dataType: 'json',
        method: 'PUT',
        success: function(result) {
            hide_error();
            if(result.success){
                //give a feedback to the user
                show_page_save(parent_div);
            }
            else{
                //give a feedback to the user
                show_page_error(parent_div,result.local_error);
            }
        },
        error: function (jqXHR, exception) {
            show_error(jqXHR, exception);
        }
    });
}

function delete_page(parent_div,id){
//Delete a page//

    //delete page from the dom
    parent_div.find('.journal_entree_texte').remove()
    
    //setup csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': $("[name='csrfmiddlewaretoken']").val()}});
    //setup ajax call
    $.ajax({
        url: '/projets/' + $('#slug').val() + 'rest-page',
        data: {
            'id': id,
        },
        dataType: 'json',
        method: 'DELETE',
        success: function(result){
            hide_error();
            if(result.success){                
                //give a feedback to the user
                show_page_save(parent_div);
            }
            else{
                //give a feedback to the user
                show_page_error(parent_div,result.local_error);
            }
        },
        error: function (jqXHR, exception) {
            show_error(jqXHR, exception);
        }
    });
}

function post_put_or_delete_page(){
    var parent_div = $(this).closest(".page-entry");
    var texte = get_text(parent_div.find(".journal_entree_texte"));
    var id = parent_div.find(".journal_entree_id").attr("value");
    if(texte != ''){
        if(id){
            put_page(parent_div,texte,id);
        }
        else{
            post_page(parent_div,texte);
        }
    }
    else{
        delete_page(parent_div,id);
    }
}

function put_or_delete_page(){
    var parent_div = $(this).closest(".page-entry");
    var texte = get_text(parent_div.find(".journal_entree_texte"));
    var id = parent_div.find(".journal_entree_id").attr("value");
    if(texte != ''){
        put_page(parent_div,texte,id);
    }
    else{
        delete_page(parent_div,id);
    }
}