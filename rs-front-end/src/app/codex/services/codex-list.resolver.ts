import { Injectable } from '@angular/core';
import {ActivatedRouteSnapshot, Resolve, RouterStateSnapshot} from '@angular/router';
import {Codex} from '../../app.models';
import {Observable} from 'rxjs';
import {CodexService} from './codex.service';

@Injectable({
  providedIn: 'root'
})
export class CodexListResolver implements Resolve<Codex[]> {

  constructor(private codexService: CodexService) { }

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<Codex[]> {
    return this.codexService.list();
  }
}
