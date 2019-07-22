import {Component, OnDestroy, OnInit} from '@angular/core';
import {switchMap} from "rxjs/operators";
import {ActivatedRoute, ParamMap} from "@angular/router";
import {Observable} from "rxjs";
import {Codex} from "../../app.models";
import {CodexDetailsService} from "../services/codex-details.service";
import {TabLink} from "../../web-page/web-page-tabs/web-page-tabs.component";

@Component({
  selector: 'app-codex-details-tabs',
  templateUrl: './codex-details-tabs.component.html',
  styleUrls: ['./codex-details-tabs.component.scss'],

})
export class CodexDetailsTabsComponent implements OnInit, OnDestroy {

  codex$: Observable<Codex>;
  tabLinkList: TabLink[];

  constructor(private codexDetailsService: CodexDetailsService, private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.codex$ = this.route.paramMap.pipe(
      switchMap(
        (params: ParamMap) => this.codexDetailsService.setActiveCodex(params.get('slug'))
      )
    );
    this.codex$.subscribe(codex => this.initTabLinkList(codex));
  }

  ngOnDestroy(): void {
    this.codexDetailsService.removeActiveCodex();
  }

  initTabLinkList(codex: Codex) {
    this.tabLinkList = [
      new TabLink(0, 'Codex', '/codex/details/' + codex.slug),
      new TabLink(1, 'Task', '/codex/details/' + codex.slug + '/todo'),
      new TabLink(2, 'Information', '/codex/details/' + codex.slug + '/information'),
    ];
  }

}
