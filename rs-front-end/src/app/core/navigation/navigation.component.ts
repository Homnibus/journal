import {Component, OnDestroy, OnInit} from '@angular/core';
import {NavigationService} from './navigation.service';
import {AuthService} from '../services/auth.service';
import {NavigationEnd, Router} from '@angular/router';
import {Subscription} from 'rxjs';
import {filter, map} from 'rxjs/operators';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent implements OnInit, OnDestroy {

  urlSubcriber: Subscription;
  navTemplate: string;

  constructor(
    private authService: AuthService,
    private navigationService: NavigationService,
    private router: Router
  ) {
  }

  ngOnInit() {
    this.urlSubcriber = this.router.events.pipe(
      filter(event => event instanceof NavigationEnd),
      map(event => event as NavigationEnd),
      map(event => event.url)
    ).subscribe(url => this.changeTemplate(url));
  }

  ngOnDestroy() {
    this.urlSubcriber.unsubscribe();
  }

  changeTemplate(url: string): void {
    const segments = url.split('/');
    if (segments.length > 2 && segments[1] === 'codex') {
      this.navTemplate = 'codexDetails';
    } else {
      this.navTemplate = '';
    }


  }

}
