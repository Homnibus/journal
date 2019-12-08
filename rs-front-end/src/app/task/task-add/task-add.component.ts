import {Component, EventEmitter, Output} from '@angular/core';
import {FormBuilder} from '@angular/forms';
import {TaskService} from '../task.service';
import {Task} from 'src/app/app.models';


@Component({
  selector: 'app-task-add',
  templateUrl: './task-add.component.html',
  styleUrls: ['./task-add.component.scss']
})
export class TaskAddComponent {

  @Output() taskCreated = new EventEmitter<Task>();
  createTaskFrom = this.fb.group({
    taskText: ['']
  });

  constructor(private taskService: TaskService, private fb: FormBuilder) {
  }

  onSubmit(): void {
    if (this.createTaskFrom.get('taskText').value.trim() !== '') {
      const newTask = new Task();
      newTask.text = this.createTaskFrom.get('taskText').value;
      this.createTaskFrom.get('taskText').reset('');
      this.taskCreated.emit(newTask);
    } else {
      this.createTaskFrom.get('taskText').setErrors({value_empty: true});
    }
  }
}
