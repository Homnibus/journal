import {NgModule} from '@angular/core';
import {RouterModule} from '@angular/router';
import {HttpClientModule} from '@angular/common/http';
import {SaveIconComponent} from './save-icon/save-icon.component';
import {LoginComponent} from './login/login.component';
import {LogoutComponent} from './logout/logout.component';
import {SharedModule} from '../shared/shared.module';
import {NavigationComponent} from './navigation/navigation.component';
import {ErrorModule} from './error/error.module';

@NgModule({
  declarations: [
    SaveIconComponent,
    LoginComponent,
    LogoutComponent,
    NavigationComponent,
  ],
  imports: [
    SharedModule,
    ErrorModule,
    RouterModule,
    HttpClientModule,
  ],
  exports: [
    SaveIconComponent,
    NavigationComponent,
  ],
})
export class CoreModule {
}
