function update_task_display() {
    var task = $(this).closest('.task');
    var is_achieved = task.find('.task__is-achieved').prop('checked');

    if (is_achieved) {
        task.addClass("task--achieved");
    } else {
        task.removeClass("task--achieved");
    }
}

$(document).on('change', '.task__is-achieved', put_or_delete_task);
$(document).on('change', '.task__is-achieved', update_task_display);
