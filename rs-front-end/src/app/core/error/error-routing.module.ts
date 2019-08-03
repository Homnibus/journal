import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {NotFoundComponent} from './not-found/not-found.component';
import {ForbiddenComponent} from './forbidden/forbidden.component';
import {UnexpectedComponent} from './unexpected/unexpected.component';

const routes: Routes = [
  {
    path: 'error', children: [
      {path: 'not-found', component: NotFoundComponent},
      {path: 'forbidden', component: ForbiddenComponent},
      {path: 'unexpected', component: UnexpectedComponent},
    ]
  },
  {path: '**', redirectTo: 'error/not-found'},
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ErrorRoutingModule {
}
