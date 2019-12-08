import { Injectable } from '@angular/core';
import {ActivatedRouteSnapshot, Resolve, RouterStateSnapshot} from '@angular/router';
import {Information} from '../app.models';
import {InformationService} from './information.service';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class InformationResolver implements Resolve<Information[]> {

  constructor(private informationService: InformationService) { }

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<Information[]> {
    const codex = route.parent.data.codex;
    return this.informationService.getCodexInformation(codex.slug);
  }



}
