import { Injectable } from '@angular/core';
import {ActivatedRouteSnapshot, Resolve, RouterStateSnapshot} from '@angular/router';
import {Page} from '../../app.models';
import {Observable} from 'rxjs';
import {PageService} from '../../page/page.service';
import {PaginationContainer} from '../../core/services/model-pagination.service';

@Injectable({providedIn: 'root'})
export class CodexDetailsOldPageListResolver implements Resolve<PaginationContainer<Page>> {

  constructor(private pageService: PageService) { }

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<PaginationContainer<Page>> {
    const codex = route.parent.data.codex;
    return this.pageService.getCodexPage(codex.slug, 1);
  }

}
