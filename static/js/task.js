/** Add a new task at the start of the today-page task list  */
function add_new_task_dom(text, id, hash) {
    const task_list = $('.page--today .task-list');
    const task = $('' +
        '<article class="task">' +
        '<input type="hidden" name="id" class="id" id="id_id">' +
        '<input type="hidden" name="hash" class="hash" id="id_hash">' +
        '<div class="left-border-box">' +
        '<input type="checkbox" name="is_achieved" class="task__is-achieved" id="id_is_achieved">' +
        '</div>' +
        '<div class="task__connexion-line"></div>' +
        '<textarea name="text" cols="40" rows="1" class="task__text typewatch left-border-box" required="" id="id_text"></textarea>' +
        '</article>'
    );
    task.find('.id').val(id);
    task.find('.hash').val(hash);
    task.find('.task__text').val(text);
    task_list.prepend(task);

    return task;
}

/** Notice the user that the page was saved */
function show_task_save(task) {
    const save_task = task.closest('.task-list').parent().find('.save-info');
    // Animate the save div
    save_task.fadeIn('slow', function () {
        save_task.fadeOut('slow');
    });
}

/** Notice the user that the page couldn't be saved */
function show_task_error(task, jqXHR, exception) {
    hide_error();
    if (jqXHR.status !== 400) {
        show_error(jqXHR, exception);
    }
    const result = jqXHR.responseJSON;
    const nb_global_error = result.form_errors.length;
    for (let i = 0; i < nb_global_error; i++) {
        const error = $('<div class="error">').text(result.form_errors[i]);
        task.closest('.page__task-section').find('header').after(error);
        task.find('.task__text').addClass('textarea-error');

    }
    jQuery.each(result.fields_error, function (field, error_list) {
        const nb_error = error_list.length;
        for (let i = 0; i < nb_error; i++) {
            const error = $('<div class="local-error">').text(error_list[i]);
            task.closest('.page__task-section').find('header').after(error);
            task.find('.task__text').addClass('textarea-error');
        }
    });
    if (nb_global_error === 0 && jQuery.isEmptyObject(result.fields_error)) {
        show_error(jqXHR, exception);
    }
}

/** Create a new task */
function post_task() {
    const task = $(this).closest('.task');
    const text = get_text(task.find('.task__text'));

    if (text !== '') {
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

                // Delete text from the initial from
                const task_creation_input = $('.task--new .task__text');
                task_creation_input.val('');

                // Add the new task to the dom
                const new_task = add_new_task_dom(text, result.id, result.hash);
                const new_task_text = new_task.find('.task__text');

                autosize(new_task_text);

                //Set typeWatch event
                new_task_text.typeWatch({
                    callback: put_or_delete_task,
                    wait: 500,
                    highlight: false,
                    allowSubmit: false,
                    captureLength: 1,
                });
                // Give a success feedback to the user
                show_task_save(task);
                // At the end of the function, remove the unclickable class to allow the add of a new task
                $('.task__add-item-button').removeClass('unclickable');

            },
            error: (jqXHR, exception) => {
                // Give a feedback to the user
                show_task_error(task, jqXHR, exception);
                // At the end of the function, remove the unclickable class to allow the add of a new task
                $('.task__add-item-button').removeClass('unclickable');

            }
        });
    }
    else {
        // At the end of the function, remove the unclickable class to allow the add of a new task
        $('.task__add-item-button').removeClass('unclickable');
    }
}

/** Update task */
function put_task(task, is_achieved, text, id, hash) {

    // Update the hash of the text for the next update
    task.find('.hash').val(text.trim().hashCode());

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
        success: function () {
            hide_error();
            // Give a feedback to the user
            show_task_save(task);
        },
        error: function (jqXHR, exception) {
            // Give a feedback to the user
            show_task_error(task, jqXHR, exception);
        }
    });
}

/** Delete a task */
function delete_task(task, id, hash) {
    // Delete task from the dom
    task.remove();

    // Set the csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val()}});
    // Do the ajax call
    $.ajax({
        url: '/tasks/' + id,
        data: {},
        dataType: 'json',
        method: 'DELETE',
        success: function () {
            hide_error();
            // Give a feedback to the user
            show_task_save(task);
        },
        error: function (jqXHR, exception) {
            // Give a feedback to the user
            show_task_error(task, jqXHR, exception);
        }
    });
}

/** Do the according rest action on a note */
function put_or_delete_task() {
    const task = $(this).closest('.task');
    const is_achieved = task.find('.task__is-achieved').prop('checked');
    const text = get_text(task.find('.task__text'));
    const id = task.find('.id').attr('value');
    const hash = task.find('.hash').val();
    if (text !== '') {
        put_task(task, is_achieved, text, id, hash);
    }
    else {
        delete_task(task, id, hash);
    }
}
