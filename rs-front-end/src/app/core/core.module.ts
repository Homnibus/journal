import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {RouterModule} from '@angular/router';
import {HttpClientModule} from '@angular/common/http';
import {TextareaAutosizeModule} from 'ngx-textarea-autosize';

import {NavigationComponent} from './navigation/navigation.component';
import {NavigationService} from './navigation/navigation.service';
import {SaveIconComponent} from './save-icon/save-icon.component';
import {ModificationRequestStatusService} from './services/modification-request-status.service';
import {LoginComponent} from './login/login.component';
import {LogoutComponent} from './logout/logout.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {AuthService} from './services/auth.service';

@NgModule({
  declarations: [
    NavigationComponent,
    SaveIconComponent,
    LoginComponent,
    LogoutComponent,
  ],
  imports: [
    CommonModule,
    RouterModule,
    HttpClientModule,
    TextareaAutosizeModule,
    ReactiveFormsModule,
    FormsModule,
  ],
  exports: [
    NavigationComponent,
    LoginComponent,
    LogoutComponent,
    SaveIconComponent,
  ],
  providers: [
    AuthService,
    NavigationService,
    ModificationRequestStatusService,
  ]
})
export class CoreModule {
}
