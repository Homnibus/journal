import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {CodexListComponent} from './codex-list/codex-list.component';
import {CodexDetailsComponent} from './codex-details/codex-details.component';
import {AuthGuard} from '../core/auth.guard';
import {CodexTaskTodoComponent} from './codex-task-todo/codex-task-todo.component';
import {CodexAddComponent} from './codex-add/codex-add.component';

const routes: Routes = [
  {
    path: 'codex',
    canActivateChild: [AuthGuard],
    children: [
      {path: '', component: CodexListComponent, pathMatch: 'full'},
      {path: 'add', component: CodexAddComponent},
      {path: ':slug', component: CodexDetailsComponent},
      {path: ':slug/todo', component: CodexTaskTodoComponent},
    ]
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CodexRoutingModule {
}
