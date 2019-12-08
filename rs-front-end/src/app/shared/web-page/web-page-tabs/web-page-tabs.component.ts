import {Component, Input} from '@angular/core';
import {routerTransition} from './wep-page-tabs.animations';
import {environment} from '../../../../environments/environment';

export class TabLink {
  constructor(
    public index: number,
    public label: string,
    public routerLink: string,
  ) {
  }
}

@Component({
  selector: 'app-web-page-tabs',
  templateUrl: './web-page-tabs.component.html',
  styleUrls: ['./web-page-tabs.component.scss'],
  animations: [routerTransition]
})
export class WebPageTabsComponent {

  @Input()
  tabLinkList: TabLink[];
  tabMenuSideMaskUrl = `${environment.staticUrl}img/tab_menu_side_mask.svg`;
  tabMenuSideDecoUrl = `${environment.staticUrl}img/tab_menu_side_deco.svg`;

  constructor() {
  }

  getState(outlet) {
    return outlet.activatedRouteData.state;
  }
}
