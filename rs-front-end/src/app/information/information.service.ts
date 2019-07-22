import {Injectable} from '@angular/core';
import {ModelService} from '../core/services/model.service';
import {InformationSerializer} from '../app.serializers';
import {Information} from '../app.models';
import {ModificationRequestStatusService} from '../core/services/modification-request-status.service';
import {AuthService} from '../core/services/auth.service';
import {Observable} from "rxjs";
import {map} from "rxjs/operators";

@Injectable({
  providedIn: 'root',
})
export class InformationService extends ModelService<Information> {

  constructor(authService: AuthService, modificationRequestStatusService: ModificationRequestStatusService) {
    super(
      authService,
      Information,
      new InformationSerializer(),
      modificationRequestStatusService,
    );
  }

  getCodexInformation(codexSlug: string): Observable<Information[]> {
    const filter = `codex__slug=${codexSlug}`;
    return this.filteredList(filter).pipe(
      map(information => {
        if (information.length > 0) {
          return information.slice(0, 1);
        }
        return [];
      })
    );
  }
}
