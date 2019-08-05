import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {NoteDetailsComponent} from './note-details/note-details.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MarkdownModule} from 'ngx-markdown';
import {SharedModule} from '../shared/shared.module';

@NgModule({
  declarations: [
    NoteDetailsComponent,
  ],
  imports: [
    CommonModule,
    SharedModule,
    ReactiveFormsModule,
    FormsModule,
    MarkdownModule,
  ],
  exports: [
    NoteDetailsComponent,
  ],

})
export class NoteModule {
}
