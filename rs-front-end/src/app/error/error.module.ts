import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {ErrorRoutingModule} from './error-routing.module';
import {NotFoundComponent} from './not-found/not-found.component';
import {SharedModule} from "../shared/shared.module";
import {WebPageModule} from "../web-page/web-page.module";
import {ForbiddenComponent} from './forbidden/forbidden.component';
import {UnexpectedComponent} from './unexpected/unexpected.component';

@NgModule({
  declarations: [NotFoundComponent, ForbiddenComponent, UnexpectedComponent],
  imports: [
    CommonModule,
    ErrorRoutingModule,
    SharedModule,
    WebPageModule,
  ]
})
export class ErrorModule {
}
