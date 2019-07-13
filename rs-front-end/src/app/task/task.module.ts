import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {TaskDetailsComponent} from './task-details/task-details.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {TextareaAutosizeModule} from 'ngx-textarea-autosize';
import {SharedModule} from '../shared/shared.module';
import {TaskAddComponent} from './task-add/task-add.component';
import {TaskListComponent} from './task-list/task-list.component';

@NgModule({
  declarations: [
    TaskDetailsComponent,
    TaskAddComponent,
    TaskListComponent,
  ],
  imports: [
    CommonModule,
    SharedModule,
    ReactiveFormsModule,
    FormsModule,
    TextareaAutosizeModule,
  ],
  exports: [
    TaskDetailsComponent,
    TaskAddComponent,
    TaskListComponent,
  ],
})
export class TaskModule {
}
