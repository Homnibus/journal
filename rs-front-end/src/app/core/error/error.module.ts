import {NgModule} from '@angular/core';
import {NotFoundComponent} from './not-found/not-found.component';
import {ForbiddenComponent} from './forbidden/forbidden.component';
import {UnexpectedComponent} from './unexpected/unexpected.component';
import {SharedModule} from '../../shared/shared.module';

@NgModule({
  declarations: [NotFoundComponent, ForbiddenComponent, UnexpectedComponent],
  imports: [
    SharedModule,
  ]
})
export class ErrorModule {
}
