import {Component, Input, OnDestroy, OnInit} from '@angular/core';
import {Task} from '../../app.models';
import {FormControl} from '@angular/forms';
import {Observable, Subscription} from 'rxjs';
import {TaskService} from '../task.service';
import {concatMap, debounceTime, distinct} from 'rxjs/operators';

@Component({
  selector: 'app-task-details',
  templateUrl: './task-details.component.html',
  styleUrls: ['./task-details.component.scss']
})
export class TaskDetailsComponent implements OnInit, OnDestroy {

  @Input()
  task: Task;
  @Input()
  enableEdit = true;

  taskTextControl: FormControl;
  taskTextControlOnChange: Subscription;


  constructor(private taskService: TaskService) {
  }

  ngOnInit() {
    this.initForm();

    this.taskTextControlOnChange = this.taskTextControl.valueChanges.pipe(
      debounceTime(400),
      distinct(),
      concatMap(value => this.UpdateTaskText(value))
    ).subscribe(task => this.task = task);

  }

  ngOnDestroy() {
    this.taskTextControlOnChange.unsubscribe();
  }

  initForm(): void {
    this.taskTextControl = new FormControl(this.task.text);
  }

  onCheckBoxChange(value: boolean) {
    this.UpdateTaskIsAchieved(value).subscribe(task => this.task = task);
  }

  UpdateTaskText(taskText: string): Observable<Task> {
    const taskCopy = Object.assign({}, this.task);
    taskCopy.text = taskText;
    return this.taskService.update(taskCopy);
  }

  UpdateTaskIsAchieved(taskIsAchieved: boolean): Observable<Task> {
    const taskCopy = Object.assign({}, this.task);
    taskCopy.isAchieved = taskIsAchieved;
    return this.taskService.update(taskCopy);
  }

}
