import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

import {CodexRoutingModule} from './codex-routing.module';
import {CodexListComponent} from './codex-list/codex-list.component';
import {CodexDetailsComponent} from './codex-details/codex-details.component';
import {PageModule} from '../page/page.module';
import {CodexTaskTodoComponent} from './codex-task-todo/codex-task-todo.component';
import {TaskModule} from '../task/task.module';
import {CodexAddComponent} from './codex-add/codex-add.component';
import {SharedModule} from "../shared/shared.module";
import {CodexDetailsTabsComponent} from './codex-details-tabs/codex-details-tabs.component';
import {CodexInformationComponent} from './codex-information/codex-information.component';
import {InformationModule} from "../information/information.module";
import {WebPageModule} from "../web-page/web-page.module";
import {CodexEditComponent, CodexEditDeleteDialog} from './codex-edit/codex-edit.component';

@NgModule({
  declarations: [
    CodexListComponent,
    CodexDetailsComponent,
    CodexTaskTodoComponent,
    CodexAddComponent,
    CodexDetailsTabsComponent,
    CodexInformationComponent,
    CodexEditComponent,
    CodexEditDeleteDialog,
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    SharedModule,
    CodexRoutingModule,
    PageModule,
    TaskModule,
    InformationModule,
    WebPageModule,
  ],
  entryComponents: [CodexEditDeleteDialog],
})
export class CodexModule {
}
