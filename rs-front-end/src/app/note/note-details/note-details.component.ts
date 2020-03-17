import {ChangeDetectionStrategy, Component, ElementRef, EventEmitter, Input, OnDestroy, OnInit, Output, ViewChild} from '@angular/core';
import {Note} from '../../app.models';
import {FormBuilder, FormGroup} from '@angular/forms';
import {Subscription} from 'rxjs';
import {debounceTime, distinctUntilChanged, filter, map, tap} from 'rxjs/operators';
import {NoteService} from '../note.service';
import {ModificationRequestStatusService} from '../../core/services/modification-request-status.service';
import * as CustomEditor from 'ckeditor5-build-rescodex';

@Component({
  selector: 'app-note-details',
  templateUrl: './note-details.component.html',
  styleUrls: ['./note-details.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class NoteDetailsComponent implements OnInit, OnDestroy {

  @Input() note?: Note;
  @Input() noteLabel = '';

  @Output() editableChange: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Output() noteCreated = new EventEmitter<Note>();
  @Output() noteTextChanged = new EventEmitter<string>();
  @Output() noteDeleted = new EventEmitter();

  @ViewChild('noteField') noteTextarea: ElementRef;

  private noteTextControl: FormGroup;
  private noteTextControlOnChange: Subscription;
  public Editor = CustomEditor;

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

  constructor(private noteService: NoteService,
              private modificationRequestStatus: ModificationRequestStatusService,
              private fb: FormBuilder) {
  }

  ngOnInit() {
    this.noteTextControl = this.fb.group({
      noteText: [this.note ? this.note.text : '']
    });

    this.noteTextControlOnChange = this.noteTextControl.get('noteText').valueChanges.pipe(
      map(value => value.trim()),
      filter( value => value !== '' || !!this.note),
      distinctUntilChanged(),
      tap(data => this.modificationRequestStatus.inputDataToSave(data)),
      debounceTime(400),
    ).subscribe(note => this.createOrUpdateOrDeleteNote(note));
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

  createOrUpdateOrDeleteNote(noteText: string): void {
    // let httpObservable: Observable<Note>;
    if (!this.note) { // Create
      // Create a copy of the Note to prevent the update of the markdown part until the server give a 200
      // response
      const newNote = new Note();
      newNote.text = noteText;
      this.noteCreated.emit(newNote);
    } else { // Update or Delete
      if (NoteService.noteShouldBeDeleted(noteText)) { // Delete
        // Create a copy of the Note to prevent the update of the markdown part until the server give a 200
        // response
        this.noteDeleted.emit();
      } else { // Update
        this.noteTextChanged.emit(noteText);
      }
    }
  }

}
