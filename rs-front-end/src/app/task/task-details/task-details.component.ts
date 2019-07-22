import {ChangeDetectionStrategy, Component, Input, OnDestroy, OnInit} from '@angular/core';
import {Task} from '../../app.models';
import {FormControl} from '@angular/forms';
import {Observable, Subscription} from 'rxjs';
import {TaskService} from '../task.service';
import {concatMap, debounceTime, distinct} from 'rxjs/operators';
import {MatCheckboxChange} from "@angular/material";

@Component({
  selector: 'app-task-details',
  templateUrl: './task-details.component.html',
  styleUrls: ['./task-details.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class TaskDetailsComponent implements OnInit, OnDestroy {

  @Input()
  task: Task;
  @Input()
  allowChangeEditable = true;

  @Input()
  editable = true;

  taskTextControl: FormControl;
  private taskTextControlOnChange: Subscription;

  constructor(private taskService: TaskService) {
  }

  ngOnInit() {
    this.taskTextControl = new FormControl(this.task.text);

    this.taskTextControlOnChange = this.taskTextControl.valueChanges.pipe(
      debounceTime(400),
      distinct(),
      concatMap(value => this.UpdateTaskText(value))
    ).subscribe(task => this.task = task);

  }

  ngOnDestroy() {
    this.taskTextControlOnChange.unsubscribe();
  }

  switchTaskEditableMode() {
    this.editable = !this.editable;
  }

  onCheckBoxChange(matCheckboxChange: MatCheckboxChange) {
    this.UpdateTaskIsAchieved(matCheckboxChange.checked).subscribe(task => this.task = task);
  }

  UpdateTaskText(taskText: string): Observable<Task> {
    // Create a copy of the Task to prevent the update of the markdown part until the server give a 200
    // response
    const taskCopy = Object.assign({}, this.task);
    taskCopy.text = taskText;
    return this.taskService.update(taskCopy);
  }

  UpdateTaskIsAchieved(taskIsAchieved: boolean): Observable<Task> {
    // Create a copy of the Task to prevent the update of the markdown part until the server give a 200
    // response
    const taskCopy = Object.assign({}, this.task);
    taskCopy.isAchieved = taskIsAchieved;
    return this.taskService.update(taskCopy);
  }

}
