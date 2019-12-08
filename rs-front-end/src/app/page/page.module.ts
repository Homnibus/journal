import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {TodayPageComponent} from './today-page/today-page.component';
import {NoteModule} from '../note/note.module';
import {PageDetailsComponent} from './page-details/page-details.component';
import {TaskModule} from '../task/task.module';
import {SharedModule} from '../shared/shared.module';

@NgModule({
  declarations: [
    TodayPageComponent,
    PageDetailsComponent,
  ],
  imports: [
    CommonModule,
    SharedModule,
    NoteModule,
    TaskModule,
  ],
  exports: [
    TodayPageComponent,
    PageDetailsComponent,
  ],
})
export class PageModule {
}
