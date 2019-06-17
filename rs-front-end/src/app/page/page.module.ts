import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {TodayPageComponent} from './today-page/today-page.component';
import {OldPageListComponent} from './old-page-list/old-page-list.component';
import {PageService} from './page.service';
import {NoteModule} from '../note/note.module';
import {PageDetailsComponent} from './page-details/page-details.component';
import {TaskModule} from '../task/task.module';

@NgModule({
  declarations: [TodayPageComponent, OldPageListComponent, PageDetailsComponent],
  exports: [
    TodayPageComponent,
    OldPageListComponent
  ],
  imports: [
    CommonModule,
    NoteModule,
    TaskModule
  ],
  providers: [PageService]
})
export class PageModule {
}
