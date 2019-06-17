import {Component, OnDestroy, OnInit} from '@angular/core';
import {ModificationRequestStatusService} from '../services/modification-request-status.service';
import {Subscription} from 'rxjs';

@Component({
  selector: 'app-save-icone',
  templateUrl: './save-icon.component.html',
  styleUrls: ['./save-icon.component.scss'],
})
export class SaveIconComponent implements OnInit, OnDestroy {

  private showIcon: boolean;
  private requestStatusSubscription: Subscription;

  constructor(private modificationRequestStatusService: ModificationRequestStatusService) {
  }

  ngOnInit() {
    this.requestStatusSubscription = this.modificationRequestStatusService.requestPoolEvent$.subscribe(
      () => {
        this.showIcon = this.modificationRequestStatusService.hasActiveRequest();
      }
    );
  }

  ngOnDestroy() {
    this.requestStatusSubscription.unsubscribe();
  }
}


