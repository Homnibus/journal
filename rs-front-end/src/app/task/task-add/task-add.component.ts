import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {FormBuilder, Validators} from '@angular/forms';
import {TaskService} from '../task.service';
import {Codex, Task} from 'src/app/app.models';


@Component({
  selector: 'app-task-add',
  templateUrl: './task-add.component.html',
  styleUrls: ['./task-add.component.scss']
})
export class TaskAddComponent implements OnInit {

  @Input()
  codex: Codex;

  @Output()
  taskAdded = new EventEmitter<Task>();

  addTaskFrom = this.fb.group({
    taskText: ['', Validators.required]
  });

  constructor(private taskService: TaskService, private fb: FormBuilder) {
  }

  ngOnInit() {
  }

  onSubmit(): void {
    if (this.addTaskFrom.valid) {
      const newTask = new Task();
      newTask.text = this.addTaskFrom.get('taskText').value;
      newTask.codex = this.codex.id;
      this.taskService.create(newTask)
        .subscribe(
          task => {
            this.taskAdded.emit(task);
            this.addTaskFrom.reset();
          });
    }
  }


}
