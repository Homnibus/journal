import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {RouterModule} from '@angular/router';
import {HttpClientModule} from '@angular/common/http';
import {TextareaAutosizeModule} from 'ngx-textarea-autosize';
import {SaveIconComponent} from './save-icon/save-icon.component';
import {LoginComponent} from './login/login.component';
import {LogoutComponent} from './logout/logout.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {SharedModule} from "../shared/shared.module";
import {NavigationComponent} from './navigation/navigation.component';
import {WebPageModule} from "../web-page/web-page.module";

@NgModule({
  declarations: [
    SaveIconComponent,
    LoginComponent,
    LogoutComponent,
    NavigationComponent,
  ],
  imports: [
    CommonModule,
    SharedModule,
    WebPageModule,
    RouterModule,
    HttpClientModule,
    TextareaAutosizeModule,
    ReactiveFormsModule,
    FormsModule,
  ],
  exports: [
    SaveIconComponent,
    NavigationComponent,
  ],
})
export class CoreModule {
}
