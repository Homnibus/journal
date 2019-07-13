import {Component, OnDestroy, OnInit} from '@angular/core';
import {switchMap} from "rxjs/operators";
import {ActivatedRoute, ParamMap} from "@angular/router";
import {Observable} from "rxjs";
import {Codex} from "../../app.models";
import {CodexDetailsService} from "../codex-details.service";
import {routerTransition} from "../codex-routing.animations";

@Component({
  selector: 'app-codex-details-tabs',
  templateUrl: './codex-details-tabs.component.html',
  styleUrls: ['./codex-details-tabs.component.scss'],
  animations: [routerTransition]
})
export class CodexDetailsTabsComponent implements OnInit, OnDestroy {

  codex$: Observable<Codex>;

  constructor(private codexDetailsService: CodexDetailsService, private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.codex$ = this.route.paramMap.pipe(
      switchMap(
        (params: ParamMap) => this.codexDetailsService.setActiveCodex(params.get('slug'))
      )
    );
  }

  ngOnDestroy(): void {
    this.codexDetailsService.removeActiveCodex();
  }

  getState(outlet) {
    return outlet.activatedRouteData.state;
  }

}
