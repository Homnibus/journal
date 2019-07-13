import {Component, Input, OnDestroy, OnInit} from '@angular/core';
import {Codex, Note} from '../../app.models';
import {FormControl} from '@angular/forms';
import {Observable, Subscription} from 'rxjs';
import {concatMap, debounceTime, distinct} from 'rxjs/operators';
import {NoteService} from '../note.service';

@Component({
  selector: 'app-note-details',
  templateUrl: './note-details.component.html',
  styleUrls: ['./note-details.component.scss']
})
export class NoteDetailsComponent implements OnInit, OnDestroy {

  @Input()
  noteLabel = '';
  @Input()
  editable = true;

  @Input()
  note?: Note;
  private noteTextControl: FormControl;
  @Input()
  codex?: Codex;
  private noteTextControlOnChange: Subscription;

  constructor(private noteService: NoteService) {
  }

  ngOnInit() {
    let formInitialValue = '';
    if (this.note) {
      formInitialValue = this.note.text;
    }
    this.noteTextControl = new FormControl(formInitialValue);

    this.noteTextControlOnChange = this.noteTextControl.valueChanges.pipe(
      debounceTime(400),
      distinct(),
      concatMap(value => this.createOrUpdateNote(value))
    ).subscribe(note => this.note = note);
  }

  ngOnDestroy() {
    this.noteTextControlOnChange.unsubscribe();
  }

  createOrUpdateNote(noteText: string): Observable<Note> {
    let httpObservable: Observable<Note>;
    if (this.note) {
      const noteCopy = Object.assign({}, this.note);
      noteCopy.text = noteText;
      httpObservable = this.noteService.update(noteCopy);
    } else {
      const newNote = new Note();
      newNote.text = noteText;
      newNote.codex = this.codex.id;
      httpObservable = this.noteService.create(newNote);
    }
    return httpObservable;
  }

}
