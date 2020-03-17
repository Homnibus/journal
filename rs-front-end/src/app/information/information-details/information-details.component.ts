import {ChangeDetectionStrategy, Component, ElementRef, EventEmitter, Input, OnDestroy, OnInit, Output, ViewChild} from '@angular/core';
import {Codex, Information} from '../../app.models';
import {FormBuilder, FormGroup} from '@angular/forms';
import {Observable, Subscription} from 'rxjs';
import {InformationService} from '../information.service';
import {concatMap, debounceTime, distinctUntilChanged, filter, map, tap} from 'rxjs/operators';
import {ModificationRequestStatusService} from '../../core/services/modification-request-status.service';
import * as CustomEditor from 'ckeditor5-build-rescodex';

@Component({
  selector: 'app-information-details',
  templateUrl: './information-details.component.html',
  styleUrls: ['./information-details.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class InformationDetailsComponent implements OnInit, OnDestroy {

  @ViewChild('informationEditorField') informationEditor: ElementRef;
  @Input() information?: Information;
  @Input() codex?: Codex;
  @Output() editableChange = new EventEmitter<boolean>();
  informationTextControl: FormGroup;
  private informationTextControlOnChange: Subscription;
  public Editor = CustomEditor;

  constructor(private informationService: InformationService,
              private modificationRequestStatus: ModificationRequestStatusService,
              private fb: FormBuilder) {
  }

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

  ngOnInit() {
    this.informationTextControl = this.fb.group({
      informationText: [this.information ? this.information.text : '']
    });
    this.informationTextControlOnChange =
      this.informationTextControl.get('informationText').valueChanges.pipe(
        map(value => value.trim()),
        filter( value => value !== '' || !!this.information),
        distinctUntilChanged(),
        tap(data => this.modificationRequestStatus.inputDataToSave(data)),
        debounceTime(400),
        concatMap(value => this.createOrUpdateOrDeleteInformation(value))
      ).subscribe(information => this.information = information);
  }

  ngOnDestroy() {
    this.informationTextControlOnChange.unsubscribe();
  }

  switchInformationEditableMode() {
    this.editable = !this.editable;
    setTimeout(() => { // this will make the execution after the above boolean has changed
      this.informationEditor.nativeElement.focus();
    }, 0);
  }

  createOrUpdateOrDeleteInformation(informationText: string): Observable<Information> {
    let httpObservable: Observable<Information>;
    if (!this.information) { // Create
    // Create a copy of the Information to prevent the update of the markdown part until the server give a 200
    // response
      const newInformation = new Information();
      newInformation.text = informationText;
      newInformation.codex = this.codex.id;
      httpObservable = this.informationService.create(newInformation);
    } else { // Update or delete
      if (informationText !== '') { // Update
        // Create a copy of the Information to prevent the update of the markdown part until the server give a 200
        // response
        const informationCopy = Object.assign({}, this.information);
        informationCopy.text = informationText;
        httpObservable = this.informationService.update(informationCopy);
      } else { // Delete
        httpObservable = this.informationService.delete(this.information).pipe(map(() => undefined));
      }
    }
    return httpObservable;
  }


}
