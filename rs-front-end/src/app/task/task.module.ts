import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {TaskDetailsComponent} from './task-details/task-details.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {SharedModule} from '../shared/shared.module';
import {TaskAddComponent} from './task-add/task-add.component';

@NgModule({
  declarations: [
    TaskDetailsComponent,
    TaskAddComponent,
  ],
  imports: [
    CommonModule,
    SharedModule,
    ReactiveFormsModule,
    FormsModule,
  ],
  exports: [
    TaskDetailsComponent,
    TaskAddComponent,
  ],
})
export class TaskModule {
}
