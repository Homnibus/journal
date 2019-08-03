import {Component, OnDestroy, OnInit} from '@angular/core';
import {ModificationRequestStatusService} from '../services/modification-request-status.service';
import {merge, Subscription} from 'rxjs';
import {saveIconTransition} from './save-icon.animations';

export enum iconStatusEnum {
  hide,
  toBeSaved,
  saving,
}

@Component({
  selector: 'app-save-icone',
  templateUrl: './save-icon.component.html',
  styleUrls: ['./save-icon.component.scss'],
  animations: [saveIconTransition],
})
export class SaveIconComponent implements OnInit, OnDestroy {

  iconStatusEnum = iconStatusEnum;
  iconStatus: iconStatusEnum = iconStatusEnum.hide;
  iconStatusObservable = merge(
    this.modificationRequestStatusService.dataToSaveIsInputted$,
    this.modificationRequestStatusService.saveRequestStarted$,
    this.modificationRequestStatusService.saveRequestEnded$
  );
  iconStatusSubscription: Subscription;

  constructor(private modificationRequestStatusService: ModificationRequestStatusService) {
  }

  ngOnInit() {

    this.iconStatusSubscription = this.iconStatusObservable.subscribe(data => {
        if (this.modificationRequestStatusService.activeSaveRequestCount === 0) {
          if (this.modificationRequestStatusService.dataNeedToBeSaved) {
            this.iconStatus = iconStatusEnum.toBeSaved;
            // console.log('toBeSaved');
          } else {
            this.iconStatus = iconStatusEnum.hide;
            // console.log('hide');
          }
        } else {
          this.iconStatus = iconStatusEnum.saving;
          // console.log('saving');
        }
      }
    );
  }

  ngOnDestroy() {
    this.iconStatusSubscription.unsubscribe();
  }
}


