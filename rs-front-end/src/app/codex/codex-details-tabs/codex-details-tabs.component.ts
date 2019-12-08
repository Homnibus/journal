import {Component, OnDestroy, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {Codex} from '../../app.models';
import {CodexDetailsService} from '../services/codex-details.service';
import {TabLink} from '../../shared/web-page/web-page-tabs/web-page-tabs.component';

@Component({
  selector: 'app-codex-details-tabs',
  templateUrl: './codex-details-tabs.component.html',
  styleUrls: ['./codex-details-tabs.component.scss'],

})
export class CodexDetailsTabsComponent implements OnInit, OnDestroy {

  codex: Codex;
  tabLinkList: TabLink[];

  constructor(private codexDetailsService: CodexDetailsService, private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.route.data.subscribe(data => {
      this.codex = data.codex;
      this.initTabLinkList(data.codex);
    });
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
