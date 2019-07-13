import {Component, Input, OnDestroy, OnInit} from '@angular/core';
import {Codex, Information} from "../../app.models";
import {FormControl} from "@angular/forms";
import {Observable, Subscription} from "rxjs";
import {InformationService} from "../information.service";
import {concatMap, debounceTime, distinct} from "rxjs/operators";

@Component({
  selector: 'app-information-details',
  templateUrl: './information-details.component.html',
  styleUrls: ['./information-details.component.scss'],
})
export class InformationDetailsComponent implements OnInit, OnDestroy {


  @Input()
  information?: Information;
  @Input()
  editable = true;
  @Input()
  codex?: Codex;

  informationTextControl: FormControl;
  informationTextControlOnChange: Subscription;

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


  createOrUpdateInformation(informationText: string): Observable<Information> {
    let httpObservable: Observable<Information>;
    if (this.information) {
      const informationCopy = Object.assign({}, this.information);
      informationCopy.text = informationText;
      httpObservable = this.informationService.update(informationCopy);
    } else {
      const newInformation = new Information();
      newInformation.text = informationText;
      newInformation.codex = this.codex.id;
      httpObservable = this.informationService.create(newInformation);
    }
    return httpObservable;
  }


}
