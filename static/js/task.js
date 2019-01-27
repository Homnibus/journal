/** Add a new task at the start of the today-page task list  */
function add_new_task_dom(text, id, hash) {
    const task_list = $('.today-page .task-list');
    // Create the article element
    const article = document.createElement("article");
    article.setAttribute("class", "task");

    // Add the id hidden input
    const id_input = document.createElement("input");
    id_input.setAttribute("type", "hidden");
    id_input.setAttribute("class", "id");
    id_input.setAttribute("value", id);
    article.append(id_input);

    // Add the hash hidden input
    const hash_input = document.createElement("input");
    hash_input.setAttribute("type", "hidden");
    hash_input.setAttribute("class", "hash");
    hash_input.setAttribute("value", hash);
    article.append(hash_input);

    // Add the checkbox
    const is_achieved_div = document.createElement("div");
    is_achieved_div.setAttribute("class", "disp-task_is_achieved");
    const is_achieved_input = document.createElement("input");
    is_achieved_input.setAttribute("class", "task_is_achieved");
    is_achieved_input.setAttribute("type", "checkbox");
    is_achieved_div.append(is_achieved_input);
    article.append(is_achieved_div);

    // Add the textarea
    const text_div = document.createElement("div");
    text_div.setAttribute("class", "disp-task_text");
    const text_input = document.createElement("textarea");
    text_input.setAttribute("class", "task_text task_typewatch");
    text_input.setAttribute("style", "overflow: hidden; overflow-wrap: break-word; height: 52px;");
    text_input.value = text;
    autosize(text_input);
    text_div.append(text_input);
    article.append(text_div);

    // Add the article to the task list
    task_list.prepend(article)
}


/** Update the hash corresponding to the id */
function update_task_hash(text, id) {
    // Trim the text so it's the same as in the database
    $('.task .id[value=' + id + ']').parent().find('.hash').val(text.trim().hashCode());
}

/** Get the hash corresponding to the id */
function get_task_hash(id) {
    return $('.task .id[value=' + id + ']').parent().find('.hash').val();
}

/** Notice the user that the page was saved */
function show_task_save(parent_div) {
    const save_task = parent_div.closest('.page-tasks').find('.save-info');
    // Animate the save div
    save_task.fadeIn('slow', function () {
        save_task.fadeOut('slow');
    });
}

/** Notice the user that the page couldn't be saved */
function show_task_error(parent_div, local_error) {
    const error = $('<div class="local-error">').text(local_error);
    parent_div.closest('.page-task').find('header').append(error);
    parent_div.find('.task_text').addClass('textarea-error');
}

/** Create a new task */
function post_task() {
    const parent_div = $(this).closest('.task');
    const text = get_text(parent_div.find('.task_text'));

    if (text !== '') {
        //"codex/<slug:codex_slug>/tasks"
        // Set the csrf token
        $.ajaxSetup({headers: {'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val()}});
        // Do the ajax call
        $.ajax({

            url: '/codex/' + $('#slug').val() + '/tasks',
            data: {
                'text': text,
            },
            dataType: 'json',
            method: 'POST',
            success: function (result) {
                hide_error();
                if (result.success) {
                    console.log(text);

                    // Delete text from the initial from
                    $('.new-task .task_text').val('');

                    // Add the new task to the dom
                    add_new_task_dom(text, result.id, result.hash);

                    //Set typeWatch event
                    const jqry_textarea = $('.task .id[value = ' + result.id + ']').closest('article').find('.task_text');
                    jqry_textarea.typeWatch({
                        callback: put_or_delete_task,
                        wait: 500,
                        highlight: false,
                        allowSubmit: false,
                        captureLength: 1,
                    });
                    // Give a success feedback to the user
                    show_task_save(parent_div);
                }
                else {
                    // Give an error feedback to the user
                    show_task_error(parent_div, result.local_error);
                }
                // At the end of the function, remove the unclickable class to allow the add of a new task
                $('.add-item-button').removeClass('unclickable');

            },
            error: (jqXHR, exception) => {
                show_error(jqXHR, exception);
                // At the end of the function, remove the unclickable class to allow the add of a new task
                $('.add-item-button').removeClass('unclickable');

            }
        });
    }
    else {
        // At the end of the function, remove the unclickable class to allow the add of a new task
        $('.add-item-button').removeClass('unclickable');
    }
}

/** Update task */
function put_task(parent_div, is_achieved, text, id) {
    const hash = get_task_hash(id);
    // Update the hash of the text for the next update
    update_task_hash(text, id);

    // Set the crsf token
    $.ajaxSetup({headers: {'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val()}});
    // Do the ajax call
    $.ajax({
        url: '/tasks/' + id,
        data: {
            'text': text,
            'is_achieved': is_achieved,
            'hash': hash,
        },
        dataType: 'json',
        method: 'PUT',
        success: function (result) {
            hide_error();
            if (result.success) {
                // Give a feedback to the user
                show_task_save(parent_div);
            }
            else {
                // Give a feedback to the user
                show_task_error(parent_div, result.local_error);
            }
        },
        error: function (jqXHR, exception) {
            show_error(jqXHR, exception);
        }
    });
}

/** Delete a task */
function delete_task(parent_div, id) {
    // Delete task from the dom
    parent_div.remove();

    // Set the csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val()}});
    // Do the ajax call
    $.ajax({
        url: '/tasks/' + id,
        data: {},
        dataType: 'json',
        method: 'DELETE',
        success: function (result) {
            hide_error();
            if (result.success) {

                // Give a feedback to the user
                show_task_save(parent_div);
            }
            else {
                // Give a feedback to the user
                show_task_error(parent_div, result.local_error);
            }
        },
        error: function (jqXHR, exception) {
            show_error(jqXHR, exception);
        }
    });
}

/** Do the according rest action on a note */
function put_or_delete_task() {
    const parent_div = $(this).closest('.task');
    const is_achieved = parent_div.find('.task_is_achieved').prop('checked');
    const text = get_text(parent_div.find('.task_text'));
    const id = parent_div.find('.id').attr('value');
    if (text !== '') {
        put_task(parent_div, is_achieved, text, id);
    }
    else {
        delete_task(parent_div, id);
    }
}
