import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {TaskDetailsComponent} from './task-details/task-details.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {TextareaAutosizeModule} from 'ngx-textarea-autosize';
import {TaskService} from './task.service';
import {SharedModule} from '../shared/shared.module';
import {TaskAddComponent} from './task-add/task-add.component';

@NgModule({
  declarations: [
    TaskDetailsComponent,
    TaskAddComponent,
  ],
  exports: [
    TaskDetailsComponent,
    TaskAddComponent,
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    TextareaAutosizeModule,
    SharedModule
  ],
  providers: [
    TaskService
  ],

})
export class TaskModule {
}
