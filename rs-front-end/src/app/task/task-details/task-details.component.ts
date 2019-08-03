import {ChangeDetectionStrategy, Component, EventEmitter, Input, OnDestroy, OnInit, Output} from '@angular/core';
import {Task} from '../../app.models';
import {FormControl} from '@angular/forms';
import {Observable, Subscription} from 'rxjs';
import {TaskService} from '../task.service';
import {concatMap, debounceTime, distinctUntilChanged, map, tap} from 'rxjs/operators';
import {MatCheckboxChange} from '@angular/material';
import {ModificationRequestStatusService} from '../../core/services/modification-request-status.service';

@Component({
  selector: 'app-task-details',
  templateUrl: './task-details.component.html',
  styleUrls: ['./task-details.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class TaskDetailsComponent implements OnInit, OnDestroy {

  @Input() task: Task;
  @Input() allowChangeEditable = true;
  @Input() editable = true;
  @Output() delete = new EventEmitter();

  taskTextControl: FormControl;
  private taskTextControlOnChange: Subscription;

  constructor(private taskService: TaskService, private modificationRequestStatus: ModificationRequestStatusService) {
  }

  ngOnInit() {
    this.taskTextControl = new FormControl(this.task.text);

    this.taskTextControlOnChange = this.taskTextControl.valueChanges.pipe(
      map(value => value.trim()),
      distinctUntilChanged(),
      tap(data => this.modificationRequestStatus.inputDataToSave(data)),
      debounceTime(400),
      concatMap(value => this.updateOrDeleteTaskText(value))
    ).subscribe(task => this.task = task);

  }

  ngOnDestroy() {
    this.taskTextControlOnChange.unsubscribe();
  }

  switchTaskEditableMode() {
    this.editable = !this.editable;
  }

  onCheckBoxChange(matCheckboxChange: MatCheckboxChange) {
    this.updateTaskIsAchieved(matCheckboxChange.checked).subscribe(task => this.task = task);
  }

  updateOrDeleteTaskText(taskText: string): Observable<Task> {
    let httpObservable: Observable<Task>;
    if (taskText !== '') { // Update
      // Create a copy of the Task to prevent the update of the markdown part until the server give a 200
      // response
      const taskCopy = Object.assign({}, this.task);
      taskCopy.text = taskText;
      httpObservable = this.taskService.update(taskCopy);
    } else { // Delete
      httpObservable = this.taskService.delete(this.task).pipe(tap(() => this.delete.emit()));
    }
    return httpObservable;
  }

  updateTaskIsAchieved(taskIsAchieved: boolean): Observable<Task> {
    // Create a copy of the Task to prevent the update of the markdown part until the server give a 200
    // response
    const taskCopy = Object.assign({}, this.task);
    taskCopy.isAchieved = taskIsAchieved;
    return this.taskService.update(taskCopy);
  }

}
