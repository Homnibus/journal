import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {HomeComponent} from './home/home.component';
import {CoreModule} from '../core/core.module';
import {RouterModule} from '@angular/router';
import {NavCodexDetailComponent} from './nav-codex-detail/nav-codex-detail.component';

@NgModule({
  declarations: [HomeComponent, NavCodexDetailComponent],
  imports: [
    CommonModule,
    CoreModule,
    RouterModule
  ],
  exports: [
    HomeComponent,
    NavCodexDetailComponent,
  ]
})
export class NavigationModule {
}
