import {NgModule} from '@angular/core';

import {CodexRoutingModule} from './codex-routing.module';
import {CodexListComponent} from './codex-list/codex-list.component';
import {CodexDetailsComponent} from './codex-details/codex-details.component';
import {PageModule} from '../page/page.module';
import {CodexTaskTodoComponent} from './codex-task-todo/codex-task-todo.component';
import {TaskModule} from '../task/task.module';
import {CodexAddComponent} from './codex-add/codex-add.component';
import {CodexDetailsTabsComponent} from './codex-details-tabs/codex-details-tabs.component';
import {CodexInformationComponent} from './codex-information/codex-information.component';
import {InformationModule} from '../information/information.module';
import {CodexEditComponent, CodexEditDeleteDialogComponent} from './codex-edit/codex-edit.component';
import {SharedModule} from '../shared/shared.module';
import {NoteModule} from '../note/note.module';
import {InfiniteScrollModule} from 'ngx-infinite-scroll';

@NgModule({
  declarations: [
    CodexListComponent,
    CodexDetailsComponent,
    CodexTaskTodoComponent,
    CodexAddComponent,
    CodexDetailsTabsComponent,
    CodexInformationComponent,
    CodexEditComponent,
    CodexEditDeleteDialogComponent,
  ],
  imports: [
    SharedModule,
    CodexRoutingModule,
    PageModule,
    NoteModule,
    TaskModule,
    InformationModule,
    InfiniteScrollModule,
  ],
  entryComponents: [CodexEditDeleteDialogComponent],
})
export class CodexModule {
}
