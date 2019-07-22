import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {CodexListComponent} from './codex-list/codex-list.component';
import {CodexDetailsComponent} from './codex-details/codex-details.component';
import {AuthGuard} from '../core/guard/auth.guard';
import {CodexTaskTodoComponent} from './codex-task-todo/codex-task-todo.component';
import {CodexAddComponent} from './codex-add/codex-add.component';
import {CodexDetailsTabsComponent} from "./codex-details-tabs/codex-details-tabs.component";
import {CodexInformationComponent} from "./codex-information/codex-information.component";
import {CodexEditComponent} from "./codex-edit/codex-edit.component";

const routes: Routes = [
  {
    path: 'codex',
    canActivateChild: [AuthGuard],
    children: [
      {
        path: '',
        component: CodexListComponent,
      },
      {
        path: 'add',
        component: CodexAddComponent
      },
      {
        path: 'edit/:slug',
        component: CodexEditComponent
      },
      {
        path: 'details/:slug',
        component: CodexDetailsTabsComponent,
        children: [
          {
            path: '',
            component: CodexDetailsComponent,
            data: {state: 1}
          },
          {
            path: 'todo',
            component: CodexTaskTodoComponent,
            data: {state: 2}
          },
          {
            path: 'information',
            component: CodexInformationComponent,
            data: {state: 3}
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
