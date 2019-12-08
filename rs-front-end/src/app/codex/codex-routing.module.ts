import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {CodexListComponent} from './codex-list/codex-list.component';
import {CodexDetailsComponent} from './codex-details/codex-details.component';
import {AuthGuard} from '../core/guard/auth.guard';
import {CodexTaskTodoComponent} from './codex-task-todo/codex-task-todo.component';
import {CodexAddComponent} from './codex-add/codex-add.component';
import {CodexDetailsTabsComponent} from './codex-details-tabs/codex-details-tabs.component';
import {CodexInformationComponent} from './codex-information/codex-information.component';
import {CodexEditComponent} from './codex-edit/codex-edit.component';
import {InformationResolver} from '../information/information.resolver';
import {CodexResolver} from './services/codex.resolver';
import {TaskResolver} from '../task/task.resolver';
import {CodexDetailsTodayPageResolver} from './services/codex-details-today-page.resolver';
import {CodexDetailsOldPageListResolver} from './services/codex-details-old-page-list.resolver';
import {CodexListResolver} from './services/codex-list.resolver';

const routes: Routes = [
  {
    path: 'codex',
    canActivateChild: [AuthGuard],
    children: [
      {
        path: '',
        component: CodexListComponent,
        resolve: {codexList : CodexListResolver},
      },
      {
        path: 'add',
        component: CodexAddComponent
      },
      {
        path: 'edit/:slug',
        component: CodexEditComponent,
        resolve: {codex : CodexResolver},
      },
      {
        path: 'details/:slug',
        component: CodexDetailsTabsComponent,
        resolve: {codex : CodexResolver},
        children: [
          {
            path: '',
            component: CodexDetailsComponent,
            data: {state: 1},
            resolve: {
              todayPage : CodexDetailsTodayPageResolver,
              oldPageListFirstPage : CodexDetailsOldPageListResolver
            },
          },
          {
            path: 'todo',
            component: CodexTaskTodoComponent,
            data: {state: 2},
            resolve: {taskList : TaskResolver},
          },
          {
            path: 'information',
            component: CodexInformationComponent,
            data: {state: 3},
            resolve: {information : InformationResolver}
          },
        ]
      },
    ]
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CodexRoutingModule {
}
