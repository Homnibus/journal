import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {NoteDetailsComponent} from './note-details/note-details.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {NoteService} from './note.service';
import {TextareaAutosizeModule} from 'ngx-textarea-autosize';
import {MarkdownModule} from 'ngx-markdown';

@NgModule({
  declarations: [
    NoteDetailsComponent,
  ],
  exports: [
    NoteDetailsComponent,
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    TextareaAutosizeModule,
    MarkdownModule
  ],
  providers: [
    NoteService
  ],
})
export class NoteModule {
}
