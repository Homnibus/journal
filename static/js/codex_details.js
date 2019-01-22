/** Change a un-editable note to a editable one */
function enable_edit_note() {
    const parent_div = $(this).closest('.page-note');
    const text = get_text(parent_div.find('.note_text'));
    const editable_text = $('<textarea class="note_text note_typewatch" />');
    const id = parent_div.find('.note_id').attr('value');

    // Setting the text hash before it can be modified
    update_note_hash(text, id);

    // Replace <div> with <textarea>
    editable_text.val(text);
    parent_div.find('.note_text').replaceWith(editable_text);

    // Set the focus on the new <textarea>
    editable_text.focus();
    editable_text.get(0).setSelectionRange(0, 0);

    // Setup typeWatch event
    editable_text.typeWatch({
        callback: put_or_delete_note,
        wait: 500,
        highlight: false,
        allowSubmit: false,
        captureLength: 1,
    });

    // Setup the blur event
    editable_text.blur(disable_edit_note);

    // Setup autosize event
    autosize(editable_text);

    // Hide the pencil
    parent_div.find('.edit-pen').hide();
}


/** Change a editable note to a un-editable one */
function disable_edit_note() {
    // Before disabling the <texarea>, we save it
    put_or_delete_note.call(this);
    const html_content = $(this).val();
    const viewable_text = $('<pre class="note_text disabled-textarea"/>');
    viewable_text.text(html_content);
    $(this).replaceWith(viewable_text);
    // Show the pencil again
    viewable_text.closest('.page').find('.edit-pen').show();
}


/** Change a un-editable task list to a editable one  */
function enable_edit_tasks() {
    // Get the list of the task that we need to set editable
    const task_list = $(this).closest('.page-tasks').find('.task-list .task_text');
    task_list.each(function () {
        const parent_div = $(this);
        const text = get_text(parent_div);
        const id = parent_div.closest('.task').find('.task_id').attr('value');

        // Update the task hash
        update_task_hash(text, id);

        // Replace the <div> by an editable <textarea>
        const editable_text = $('<textarea class="task_text task_typewatch" />');
        editable_text.val(text);
        parent_div.replaceWith(editable_text);

        // Setup typeWatch event
        editable_text.typeWatch({
            callback: put_or_delete_task,
            wait: 500,
            highlight: false,
            allowSubmit: false,
            captureLength: 1,
        });

        // Setup autosize event
        autosize(editable_text);
    });
    // Hide the pencil
    task_list.find('.edit-pen').hide();
}


$(document).ready(function () {
    // Maj of today_note hash after loading page
    const today_note_id = $('.today-page .note_id').attr('value');
    if (today_note_id !== undefined) {
        note_hash[today_note_id] = $('.note_id[value = ' + today_note_id + ']').closest('.page-note').find('.note_text').val().trim().hashCode();
    }
    // When done, set the <textarea> editable
    $('.today-page .note_text').removeAttr('readonly');
});

$(document).ready(function () {
    // Maj of today_task hash after loading note
    const today_task_list = $('.today-page .old-tasks');
    enable_edit_tasks.call(today_task_list);
});

$(document).on('click', '.page-note .edit-pen', enable_edit_note);

$(document).on('click', '.page-tasks .edit-pen', enable_edit_tasks);

$(document).on('click', '.add-item-button:not(.unclickable)', function () {
    // Add the class 'unclickable' to prevent multi submission
    $(this).addClass('unclickable');
    post_task.call(this);
});

$(document).on('change', '.task_is_achieved', put_or_delete_task);

$(document).on('keypress', '.new-task .task_text',
    function (e) {
        // Ctrl-Enter pressed
        if (e.ctrlKey && e.keyCode === 13) {
            e.preventDefault();
            const add_button = $(this).closest('.task').find('.add-item-button:not(.unclickable)');
            if (add_button !== null) {
                add_button.addClass('unclickable');
                post_task.call(add_button);
            }
        }
    });

$(document).on('keypress', '.note_text:not(disabled-textarea)',
    function (e) {
        // Tab pressed
        if (e.keyCode === 9) {
            e.preventDefault();
            const start = this.selectionStart;
            const end = this.selectionEnd;

            // Set <textarea> value to: text before caret + tab + text after caret
            $(this).val($(this).val().substring(0, start)
                + "\t"
                + $(this).val().substring(end)
            );

            // Put caret at right position again
            this.selectionStart = start + 1;
            this.selectionEnd = start + 1;
        }
    }
);

$('.note_typewatch').typeWatch({
    callback: post_put_or_delete_note,
    wait: 500,
    highlight: false,
    allowSubmit: false,
    captureLength: 1,
});

$('.task:not(.new-task) .task_text').typeWatch({
    callback: put_or_delete_task,
    wait: 500,
    highlight: false,
    allowSubmit: false,
    captureLength: 1,
});

autosize($('.today-page .note_text'));
