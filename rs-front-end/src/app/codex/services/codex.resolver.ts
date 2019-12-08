import { Injectable } from '@angular/core';
import {ActivatedRouteSnapshot, Resolve, RouterStateSnapshot} from '@angular/router';
import {Codex} from '../../app.models';
import {Observable} from 'rxjs';
import {CodexDetailsService} from './codex-details.service';

@Injectable({
  providedIn: 'root'
})
export class CodexResolver implements Resolve<Codex> {

  constructor(private codexDetailsService: CodexDetailsService) { }

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<Codex> {
    return this.codexDetailsService.setActiveCodex(route.paramMap.get('slug'));
  }
}
