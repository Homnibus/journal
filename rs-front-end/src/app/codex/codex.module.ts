import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

import {CodexRoutingModule} from './codex-routing.module';
import {CodexListComponent} from './codex-list/codex-list.component';
import {CodexDetailsComponent} from './codex-details/codex-details.component';
import {CodexService} from './codex.service';
import {PageModule} from '../page/page.module';
import {AuthService} from '../core/services/auth.service';
import {CodexTaskTodoComponent} from './codex-task-todo/codex-task-todo.component';
import {TaskModule} from '../task/task.module';
import {CodexAddComponent} from './codex-add/codex-add.component';
import {NavigationModule} from '../navigation/navigation.module';

@NgModule({
  declarations: [
    CodexListComponent,
    CodexDetailsComponent,
    CodexTaskTodoComponent,
    CodexAddComponent,
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    CodexRoutingModule,
    PageModule,
    TaskModule,
    NavigationModule
  ],
  providers: [
    CodexService,
    AuthService,
  ]
})
export class CodexModule {
}
