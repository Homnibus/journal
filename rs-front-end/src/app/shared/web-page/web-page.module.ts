import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {WebPageComponent} from './web-page/web-page.component';
import {WebPageHeaderComponent} from './web-page-header/web-page-header.component';
import {WebPageContentComponent} from './web-page-content/web-page-content.component';
import {WebPageTabsComponent} from './web-page-tabs/web-page-tabs.component';
import {RouterModule} from '@angular/router';
import {WebPageTitleComponent} from './web-page-title/web-page-title.component';
import {WebPageSubtitleComponent} from './web-page-subtitle/web-page-subtitle.component';
import {WebPageActionMenuComponent} from './web-page-action-menu/web-page-action-menu.component';
import {MatDividerModule, MatTabsModule} from '@angular/material';

@NgModule({
  declarations: [
    WebPageComponent,
    WebPageHeaderComponent,
    WebPageContentComponent,
    WebPageTabsComponent,
    WebPageTitleComponent,
    WebPageSubtitleComponent,
    WebPageActionMenuComponent
  ],
  exports: [
    WebPageComponent,
    WebPageHeaderComponent,
    WebPageContentComponent,
    WebPageTabsComponent,
    WebPageSubtitleComponent,
    WebPageTitleComponent,
    WebPageActionMenuComponent,
  ],
  imports: [
    CommonModule,
    RouterModule,
    MatDividerModule,
    MatTabsModule,
  ]
})
export class WebPageModule {
}
