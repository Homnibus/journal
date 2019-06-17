const task_class = 'task';
let task_updates = {};

/** Update a task */
function put_task() {
  const text = get_text($(this));
  const task_id = $(this).find('.task_id').val();
  const is_achieved = false;
  const hash = task_hash[task_id];

  // Update the hash of the text for the next update
  update_task_hash(text, task_id);

  console.log('start put task');
  // Set the csrf token
  $.ajaxSetup({headers: {'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val()}});
  // Do the ajax call
  $.ajax({

    url: '/tasks/' + task_id,
    data: {
      'text': text,
      'is_achieved': is_achieved,
      'hash': hash,
    },
    dataType: 'json',
    method: 'PUT',
    success: (result) => {
      hide_error();
      if (result.success) {
        console.log('update ok');
      } else {
        console.log('update KO');
      }
    },
    error: (jqXHR, exception) => {
      console.log('update request error' + exception)
    }
  });
}

/** Create a new task */
function post_task() {
  const text = get_text($(this));
  const codex_slug = $('#slug').val();
  console.log('start post task');
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
      success: (result) => {
        hide_error();
        if (result.success) {
          console.log(result.id);
          this.append("<input type='hidden' class='task_id' value='" + result.id + "' />");
          task = $('.task_id[value = ' + result.id + ']').closest('.task');
          // Update the hash of the text for the next update
          update_task_hash(text, result.id);
          // pass in the target node, as well as the observer options
          console.log('observation set on ' + task[0].childNodes[0].nodeValue + ': ' + task.html());
          // Observer only work with Node element - Jquery does not implement Node element
          task_observer.observe(task[0].childNodes[0], {
            subtree: true,
            attributes: false,
            childList: false,
            characterData: true,
            characterDataOldValue: false
          });
        } else {
          console.log('save KO');
        }
      },
      error: (jqXHR, exception) => {
        console.log('request error' + exception)
      }
    });
  }
}

function get_caret_position(target) {
  let _range = document.getSelection().getRangeAt(0);
  let range = _range.cloneRange();
  range.selectNodeContents(target);
  range.setEnd(_range.endContainer, _range.endOffset);
  return range.toString().length - 1;

}

const task_observer = new MutationObserver(function (mutations) {
  mutations.forEach(function (mutation) {
    console.log("observer triggered");
    if (mutation.type === 'characterData') {
      console.log(mutation.target);
      console.log($(mutation.target).parent().html());
      const task = $(mutation.target).parent();
      const task_id = task.find(".task_id").val();
      task_updates[task_id] = task;
    }
  });
});

$(document).on('keyup', '.text-editor',
  function (e) {
    if (e.key === '*') {
      const caret_element = $(document.getSelection().anchorNode).parent();
      const caret_position = get_caret_position(document.getSelection().anchorNode);
      console.log('caret position: ' + caret_position);
      console.log('* first position: ' + caret_element.text().indexOf('*'));

      // first car can't be empty
      // TODO : add error management if first car does not exist
      if (caret_element.text().trim().charAt(0) === '*'
        /*&& caret_position === caret_element.text().indexOf('*')*/
        && !caret_element.hasClass(task_class)) {
        console.log('ok');
        caret_element.addClass(task_class);
        post_task.call(caret_element);
      } else {
        console.log('KO');
      }
    }
    if (e.keyCode === 13) {
      console.log('enter !');
      const caret_element = $(document.getSelection().anchorNode);
      console.log('caret element: ' + caret_element.html());
      // Set class task to none
      if (caret_element.prev().hasClass(task_class)) {
        console.log('no more a task');
        caret_element.removeClass(task_class);
      } else {
        console.log('prev sibling was not a task');
      }
    }
  }
);

function update_tasks() {
  console.log('update tasks');
  for (let task_id in task_updates) {
    if (task_updates.hasOwnProperty(task_id)) {
      const task = task_updates[task_id];
      delete task_updates[task_id];
      console.log(task_id + ': ' + task.html());
      put_task.call(task);
    }
  }
}

$('.text-editor').typeWatch({
  callback: update_tasks,
  wait: 500,
  highlight: false,
  allowSubmit: false,
  captureLength: 1,
});
