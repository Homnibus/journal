import {Injectable} from '@angular/core';

@Injectable()
export class NavigationService {

  private links: NavigationLink[] = [];

  public setLinks(links: NavigationLink[]): void {
    this.links = links.map(a => Object.assign({}, a));
  }

  public getLinks(): NavigationLink[] {
    return this.links;
  }

}


export class NavigationLink {
  public routerLink: string;
  public label: string;

  constructor(routerLink: string, label: string) {
    this.routerLink = routerLink;
    this.label = label;
  }
}
