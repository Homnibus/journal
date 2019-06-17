import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {FormControl} from '@angular/forms';
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

  taskTextControl: FormControl;

  constructor(private taskService: TaskService) {
  }

  ngOnInit() {
    this.initForm();
  }

  initForm(): void {
    this.taskTextControl = new FormControl();
  }

  onClick(): void {
    const newTask = new Task();
    newTask.text = this.taskTextControl.value;
    newTask.codex = this.codex.id;
    this.taskService.create(newTask)
      .subscribe(
        task => {
          this.taskAdded.emit(task);
          this.taskTextControl.reset();
        });
  }


}
