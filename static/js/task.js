/** Add a new task at the start of the today-page task list  */
function add_new_task_dom(text, id, hash) {
    const task_list = $('.page--today .task-list');
    const task = $('' +
        '<article class="task simple-list__row">' +
        '<input type="hidden" name="id" class="id" id="id_id">' +
        '<input type="hidden" name="hash" class="hash" id="id_hash">' +
        '<textarea name="text" cols="40" rows="1" class="task__text typewatch simple-list__text inline-text-input" required="" id="id_text"></textarea>' +
        '<div class="simple-list__right-icon">' +
        '<input type="checkbox" name="is_achieved" class="task__is-achieved" id="id_is_achieved">' +
        '</div>' +
        '</article>' +
        '<div class="simple-list__separator"></div>'
    );
    task.find('.id').val(id);
    task.find('.hash').val(hash);
    task.find('.task__text').val(text);
    task_list.prepend(task);

    return task;
}

/** Notice the user that the page couldn't be saved */
function show_task_error(task, jqXHR, exception) {
    const task_text = task.find('.task__text');
    const task_header = task.closest('.page__task-section').find('header');
    show_not_saved();
    show_element_error(task_text, task_header, jqXHR, exception);
}

/** Create a new task */
function post_task(task, text) {
    // Check if the text is empty to not create an empty task
    if (text === '') {
        return;
    }

    // Give a feedback to the user that there is a save being done.
    show_save();
    // Set the csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': CSRF_TOKEN}});
    // Do the ajax call
    return $.ajaxq('TaskQueueCreation', {
        url: '/codex/' + SLUG + '/tasks',
        data: {
            'text': text,
        },
        dataType: 'json',
        method: 'POST',
    }).success(function (result) {
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
    }).error((jqXHR, exception) => {
        // Give a feedback to the user
        show_task_error(task, jqXHR, exception);
    }).success(function () {
        // Give a feedback to the user that the saving ended.
        hide_save();
    });
}

/** Update task */
function put_task(task, is_achieved, text, id, hash) {
    // Update the hash of the text for the next update
    update_hash(task, text);

    // Give a feedback to the user that there is a save being done.
    show_save();
    // Set the csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': CSRF_TOKEN}});
    // Do the ajax call
    return $.ajaxq('TaskQueue' + id, {
        url: '/tasks/' + id,
        data: {
            'text': text,
            'is_achieved': is_achieved,
            'hash': hash,
        },
        dataType: 'json',
        method: 'PUT',
    }).error(function (jqXHR, exception) {
        // Give a feedback to the user
        show_task_error(task, jqXHR, exception);
    }).success(function () {
        // Give a feedback to the user that the saving ended.
        hide_save();
    });
}

/** Delete a task */
function delete_task(task, id, hash) {
    //Hide the task so it can't be changed after sending the delete request to the server
    task.hide();

    // Give a feedback to the user that there is a save being done.
    show_save();
    // Set the csrf token
    $.ajaxSetup({headers: {'X-CSRFToken': CSRF_TOKEN}});
    // Do the ajax call
    return $.ajaxq('TaskQueue' + id, {
        url: '/tasks/' + id,
        data: {
            'hash': hash,
        },
        dataType: 'json',
        method: 'DELETE',
    }).success(function () {
        // Delete task from the dom
        task.remove();
    }).error(function (jqXHR, exception) {
        // Give a feedback to the user
        show_task_error(task, jqXHR, exception);
        task.show();
    }).success(function () {
        // Give a feedback to the user that the saving ended.
        hide_save();
    });
}

/** Do the according rest action on a note */
function put_or_delete_task() {
    const task = $(this).closest('.task');
    // If the parent task is empty because it does not exist anymore, return
    if (task.length === 0) {
        return
    }

    const is_achieved = task.find('.task__is-achieved').prop('checked');
    const text = get_text(task.find('.task__text'));
    const id = task.find('.id').attr('value');
    const hash = task.find('.hash').val();

    if (text !== '') {
        return put_task(task, is_achieved, text, id, hash);
    }
    else {
        return delete_task(task, id, hash);
    }
}
