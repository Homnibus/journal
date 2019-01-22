task_hash = {};

/** Update the hash corresponding to the id */
function update_task_hash(text, id) {
    // Trim the text so it's the same as in the database
    task_hash[id] = text.trim().hashCode();
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

/** Add the new task to the dom */
function show_new_task(result) {
    // Get the old_tasks div
    const old_tasks_div = $('.today-page .old-tasks');

    // Add <div> to the returned form to navigate inside with Jquery
    const out_form_str = '<div>' + result.out_form + '</div>';
    // Add the returned form under the task add
    const new_checkbox = $('.task_is_achieved', out_form_str).clone().wrap('<div>').parent().html();
    const new_textarea = $('.task_text', out_form_str).clone().wrap('<div>').parent().html();
    const new_id = $('.task_id', out_form_str).clone().wrap('<div>').parent().html();
    old_tasks_div.prepend(
        '<article class="task">' +
        new_id +
        '<div class="disp-task_is_achieved">' +
        new_checkbox +
        '</div>' +
        '<div class="disp-task_text">' +
        new_textarea +
        '</div>' +
        '</article>'
    );
}

/** Create a new task */
function post_task() {
    const parent_div = $(this).closest('.task');
    const text = get_text(parent_div.find('.task_text'));
    const codex_slug = $('#slug').val();

    if (text !== '') {
        // Set the csrf token
        $.ajaxSetup({headers: {'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val()}});
        // Do the ajax call
        $.ajax({

            url: '/tasks',
            data: {
                'text': text,
                'codex_slug': codex_slug,
            },
            dataType: 'json',
            method: 'POST',
            success: function (result) {
                hide_error();
                if (result.success) {
                    // Update the hash of the text for the next update
                    update_task_hash(text, result.id);

                    // Delete text from the initial from
                    $('.new-task .task_text').val('');

                    // Add the new task to the dom
                    show_new_task(result);

                    //Set typeWatch event
                    const jqry_textarea = $('.task_id[value = ' + result.id + ']').closest('article').find('.task_text');
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
    // If it's the first time the task is updated, set the task hash
    if (typeof task_hash[id] === 'undefined') {
        update_task_hash(text, id);
    }
    const hash = task_hash[id];
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
    const id = parent_div.find('.task_id').attr('value');
    if (text !== '') {
        put_task(parent_div, is_achieved, text, id);
    }
    else {
        delete_task(parent_div, id);
    }
}
