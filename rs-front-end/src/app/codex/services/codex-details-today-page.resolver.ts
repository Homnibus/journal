import { Injectable } from '@angular/core';
import {ActivatedRouteSnapshot, Resolve, RouterStateSnapshot} from '@angular/router';
import {Page} from '../../app.models';
import {Observable} from 'rxjs';
import {PageService} from '../../page/page.service';

@Injectable({providedIn: 'root'})
export class CodexDetailsTodayPageResolver implements Resolve<Page> {

  constructor(private pageService: PageService) { }

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<Page> {
    const codex = route.parent.data.codex;
    return this.pageService.getTodayCodexPage(codex.slug);
  }
}
