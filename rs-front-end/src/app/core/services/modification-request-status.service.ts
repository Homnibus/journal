import {Injectable} from '@angular/core';
import {Subject} from 'rxjs';


@Injectable({
  providedIn: 'root',
})
export class ModificationRequestStatusService {

  activeSaveRequestCount = 0;
  dataNeedToBeSaved = false;

  private saveRequestStartedSubject = new Subject<number>();
  saveRequestStarted$ = this.saveRequestStartedSubject.asObservable();
  private saveRequestEndedSubject = new Subject<number>();
  saveRequestEnded$ = this.saveRequestEndedSubject.asObservable();
  private dataToSaveIsInputtedSubject = new Subject<any>();
  dataToSaveIsInputted$ = this.dataToSaveIsInputtedSubject.asObservable();

  startSaveRequest(): void {
    // console.log('Save Request Start');
    this.activeSaveRequestCount += 1;
    this.dataNeedToBeSaved = false;
    this.saveRequestStartedSubject.next(this.activeSaveRequestCount);
  }

  endSaveRequest(): void {
    // console.log('Save Request End');
    this.activeSaveRequestCount -= 1;
    this.saveRequestEndedSubject.next(this.activeSaveRequestCount);
  }

  inputDataToSave(dataToSave: any): void {
    // console.log('Data to Save');
    this.dataNeedToBeSaved = true;
    this.dataToSaveIsInputtedSubject.next(dataToSave);
  }

  hasActiveSaveRequest(): boolean {
    return this.activeSaveRequestCount > 0;
  }

  // requestFail(): void {
  //   this.requestPool -= 1;
  //   this.anyRequestFailed = true;
  //   this.requestEventSubject.next(RequestEvent.Error);
  // }

}
