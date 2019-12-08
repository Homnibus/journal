import {ChangeDetectionStrategy, Component, EventEmitter, Input, OnDestroy, OnInit, Output} from '@angular/core';
import {Task} from '../../app.models';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Subscription} from 'rxjs';
import {TaskService} from '../task.service';
import {debounceTime, distinctUntilChanged, map, tap} from 'rxjs/operators';
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

  @Output() taskTextChanged = new EventEmitter<string>();
  @Output() taskIsAchievedChanged = new EventEmitter<boolean>();
  @Output() taskDeleted = new EventEmitter();

  taskTextControl: FormGroup;
  private taskTextControlOnChange: Subscription;

  constructor(private modificationRequestStatus: ModificationRequestStatusService, private fb: FormBuilder) {
  }

  ngOnInit() {
    this.taskTextControl = this.fb.group({
      taskText: [this.task.text, Validators.required]
    });

    this.taskTextControlOnChange = this.taskTextControl.get('taskText').valueChanges.pipe(
      map(value => value.trim()),
      distinctUntilChanged(),
      tap(data => this.modificationRequestStatus.inputDataToSave(data)),
      debounceTime(400),
    ).subscribe(value => this.updateOrDeleteTaskText(value));
  }

  ngOnDestroy() {
    this.taskTextControlOnChange.unsubscribe();
  }

  switchTaskEditableMode() {
    this.editable = !this.editable;
  }

  updateOrDeleteTaskText(taskText: string): void {
    if (TaskService.taskShouldBeDeleted(taskText)) {
      this.taskDeleted.emit();
    } else {
      this.taskTextChanged.emit(taskText);
    }
  }

  updateTaskIsAchieved(matCheckboxChange: MatCheckboxChange) {
    this.taskIsAchievedChanged.emit(matCheckboxChange.checked);
  }
}
