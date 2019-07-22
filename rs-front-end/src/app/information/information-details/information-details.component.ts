import {ChangeDetectionStrategy, Component, EventEmitter, Input, OnDestroy, OnInit, Output} from '@angular/core';
import {Codex, Information} from "../../app.models";
import {FormControl} from "@angular/forms";
import {Observable, Subscription} from "rxjs";
import {InformationService} from "../information.service";
import {concatMap, debounceTime, distinct} from "rxjs/operators";

@Component({
  selector: 'app-information-details',
  templateUrl: './information-details.component.html',
  styleUrls: ['./information-details.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class InformationDetailsComponent implements OnInit, OnDestroy {

  @Input()
  information?: Information;
  @Input()
  codex?: Codex;

  @Output()
  editableChange: EventEmitter<boolean> = new EventEmitter<boolean>();
  private informationTextControlOnChange: Subscription;

  private _editable: boolean;

  get editable() {
    return this._editable;
  }

  informationTextControl: FormControl;

  @Input()
  set editable(val: boolean) {
    if (this._editable != undefined) {
      this.editableChange.emit(val);
    }
    this._editable = val;
  }

  constructor(private informationService: InformationService) {
  }

  ngOnInit() {
    this.informationTextControl = this.initForm();

    this.informationTextControlOnChange = this.informationTextControl.valueChanges.pipe(
      debounceTime(400),
      distinct(),
      concatMap(value => this.createOrUpdateInformation(value))
    ).subscribe(information => this.information = information);

  }

  ngOnDestroy() {
    this.informationTextControlOnChange.unsubscribe();
  }

  initForm(): FormControl {
    let formInitialValue = '';
    if (this.information) {
      formInitialValue = this.information.text;
    }
    return new FormControl(formInitialValue);
  }

  switchInformationEditableMode() {
    this.editable = !this.editable;
  }

  createOrUpdateInformation(informationText: string): Observable<Information> {
    let httpObservable: Observable<Information>;
    if (this.information) {
      // Create a copy of the Information to prevent the update of the markdown part until the server give a 200
      // response
      const informationCopy = Object.assign({}, this.information);
      informationCopy.text = informationText;
      httpObservable = this.informationService.update(informationCopy);
    } else {
      // Create a copy of the Information to prevent the update of the markdown part until the server give a 200
      // response
      const newInformation = new Information();
      newInformation.text = informationText;
      newInformation.codex = this.codex.id;
      httpObservable = this.informationService.create(newInformation);
    }
    return httpObservable;
  }


}
