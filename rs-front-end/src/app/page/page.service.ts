import {formatDate} from '@angular/common';
import {Injectable} from '@angular/core';
import {ModelService} from '../core/services/model.service';
import {PageSerializer} from '../app.serializers';
import {Page} from '../app.models';
import {Observable} from 'rxjs';
import {ModificationRequestStatusService} from '../core/services/modification-request-status.service';
import {AuthService} from '../core/services/auth.service';

@Injectable({
  providedIn: 'root',
})
export class PageService extends ModelService<Page> {

  constructor(authService: AuthService, modificationRequestStatusService: ModificationRequestStatusService) {
    super(
      authService,
      Page,
      new PageSerializer(),
      modificationRequestStatusService,
    );
  }

  getCodexPage(codexSlug: string): Observable<Page[]> {
    const filter = `codex__slug=${codexSlug}`;
    return this.filteredList(filter);
  }

  getTodayCodexPage(codexSlug: string): Observable<Page[]> {
    const today = formatDate(new Date(), 'yyyy-MM-dd', 'en');
    const filter = `codex__slug=${codexSlug}&date=${today}`;
    return this.filteredList(filter);
  }

}
