import {Injectable} from '@angular/core';
import {Subject} from 'rxjs';
import {filter} from 'rxjs/operators';

export enum RequestEvent {
  Start,
  End,
  Error
}

@Injectable({
  providedIn: 'root',
})
export class ModificationRequestStatusService {

  private requestEventSubject = new Subject<RequestEvent>();

  public requestEvent$ = this.requestEventSubject.asObservable();
  private requestPool = 0;
  public requestPoolEvent$ = this.requestEvent$.pipe(
    filter(value => (value === RequestEvent.Start && this.requestPool === 1)
      || (value === RequestEvent.End && this.requestPool === 0)
      || (value === RequestEvent.Error)
    )
  );
  private anyRequestFailed = false;

  requestStart(): void {
    console.log('Request Start');
    this.requestPool += 1;
    this.requestEventSubject.next(RequestEvent.Start);
  }

  requestEnd(): void {
    console.log('Request End');
    this.requestPool -= 1;
    this.requestEventSubject.next(RequestEvent.End);
  }

  requestFail(): void {
    this.requestPool -= 1;
    this.anyRequestFailed = true;
    this.requestEventSubject.next(RequestEvent.Error);
  }

  hasActiveRequest(): boolean {
    return this.requestPool > 0;
  }

  countActiveRequest(): number {
    return this.requestPool;
  }

}
