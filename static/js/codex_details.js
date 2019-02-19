/** Change a un-editable note to a editable one */
function enable_edit_note() {
    const parent_div = $(this).closest('.page__note-section');
    const text = get_text(parent_div.find('.note__text'));
    const editable_text = $('<textarea name="text" cols="40" rows="1" class="note__text typewatch" required="" id="id_text"></textarea>');

    // Replace <pre> with <textarea>
    editable_text.val(text);
    parent_div.find('.note__text').replaceWith(editable_text);

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
    const textarea = $(this);
    const html_content = $(this).val();
    const viewable_text = $('<pre class="note__text disabled-textarea"/>');
    viewable_text.text(html_content);
    textarea.replaceWith(viewable_text);
    // Show the pencil again
    viewable_text.closest('.page__note-section').find('.edit-pen').show();
    put_or_delete_note.call(viewable_text);
}


/** Change a un-editable task list to a editable one  */
function enable_edit_tasks() {
    // Get the list of the task that we need to set editable
    const task_list = $(this).closest('.page__task-section').find('.task-list .task__text');
    task_list.each(function () {
        const parent_div = $(this);
        const text = get_text(parent_div);

        // Replace the <div> by an editable <textarea>
        const editable_text = $('<textarea name="text" cols="40" rows="1" class="task__text typewatch left-border-box" required="" id="id_text"></textarea>');
        editable_text.val(text);
        parent_div.replaceWith(editable_text);

        // Setup autosize event
        autosize(editable_text);

        // Setup typeWatch event
        editable_text.typeWatch({
            callback: put_or_delete_task,
            wait: 500,
            highlight: false,
            allowSubmit: false,
            captureLength: 1,
        });

    });
    // Hide the pencil
    task_list.find('.edit-pen').hide();
}


$(document).on('click', '.page__note-section .edit-pen', enable_edit_note);

$(document).on('click', '.page__task-section .edit-pen', enable_edit_tasks);

$(document).on('click', '.task__add-item-button:not(.unclickable)', function () {
    // Add the class 'unclickable' to prevent multi submission
    $(this).addClass('unclickable');
    post_task.call(this);
});

$(document).on('change', '.task__is-achieved', put_or_delete_task);

$(document).on('keypress', '.task--new .task__text',
    function (e) {
        // Ctrl-Enter pressed
        if (e.ctrlKey && e.keyCode === 13) {
            e.preventDefault();
            const add_button = $(this).closest('.task').find('.task__add-item-button:not(.unclickable)');
            if (add_button !== null) {
                add_button.addClass('unclickable');
                post_task.call(add_button);
            }
        }
    });

$(document).on('keypress', '.note__text:not(disabled-textarea)',
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

$('.note .typewatch').typeWatch({
    callback: post_put_or_delete_note,
    wait: 500,
    highlight: false,
    allowSubmit: false,
    captureLength: 1,
});

$('.task:not(.task--new) .typewatch').typeWatch({
    callback: put_or_delete_task,
    wait: 500,
    highlight: false,
    allowSubmit: false,
    captureLength: 1,
});

autosize($('.page--today .typewatch'));