import {ChangeDetectionStrategy, Component, ElementRef, EventEmitter, Input, OnDestroy, OnInit, Output, ViewChild} from '@angular/core';
import {Codex, Note} from '../../app.models';
import {FormControl} from '@angular/forms';
import {Observable, Subscription} from 'rxjs';
import {concatMap, debounceTime, distinctUntilChanged, map, tap} from 'rxjs/operators';
import {NoteService} from '../note.service';
import {ModificationRequestStatusService} from '../../core/services/modification-request-status.service';

@Component({
  selector: 'app-note-details',
  templateUrl: './note-details.component.html',
  styleUrls: ['./note-details.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class NoteDetailsComponent implements OnInit, OnDestroy {

  @ViewChild('noteField', {static: false}) noteTextarea: ElementRef;
  @Input() noteLabel = '';
  @Output() editableChange: EventEmitter<boolean> = new EventEmitter<boolean>();
  private _editable: boolean;

  get editable() {
    return this._editable;
  }

  @Input()
  set editable(val: boolean) {
    if (this._editable !== undefined) {
      this.editableChange.emit(val);
    }
    this._editable = val;
  }

  @Input() note?: Note;
  private noteTextControl: FormControl;
  @Input() codex?: Codex;
  private noteTextControlOnChange: Subscription;

  constructor(private noteService: NoteService, private modificationRequestStatus: ModificationRequestStatusService) {
  }

  ngOnInit() {
    let formInitialValue = '';
    if (this.note) {
      formInitialValue = this.note.text;
    }
    this.noteTextControl = new FormControl(formInitialValue);

    this.noteTextControlOnChange = this.noteTextControl.valueChanges.pipe(
      map(value => value.trim()),
      distinctUntilChanged(),
      tap(data => this.modificationRequestStatus.inputDataToSave(data)),
      debounceTime(400),
      concatMap(value => this.createOrUpdateOrDeleteNote(value))
    ).subscribe(note => this.note = note);
  }

  ngOnDestroy() {
    this.noteTextControlOnChange.unsubscribe();
  }

  switchNoteEditableMode(): void {
    this.editable = !this.editable;
    setTimeout(() => { // this will make the execution after the above boolean has changed
      this.noteTextarea.nativeElement.focus();
    }, 0);
  }

  createOrUpdateOrDeleteNote(noteText: string): Observable<Note> {
    let httpObservable: Observable<Note>;
    if (!this.note) { // Create
      // Create a copy of the Note to prevent the update of the markdown part until the server give a 200
      // response
      const newNote = new Note();
      newNote.text = noteText;
      newNote.codex = this.codex.id;
      httpObservable = this.noteService.create(newNote);
    } else { // Update or Delete
      if (noteText !== '') { // Update
        // Create a copy of the Note to prevent the update of the markdown part until the server give a 200
        // response
        const noteCopy = Object.assign({}, this.note);
        noteCopy.text = noteText;
        httpObservable = this.noteService.update(noteCopy);
      } else { // Delete
        httpObservable = this.noteService.delete(this.note).pipe(map(() => undefined));
      }
    }
    return httpObservable;
  }

}
