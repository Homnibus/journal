import {Component, OnInit} from '@angular/core';
import {AuthService} from '../services/auth.service';
import {environment} from '../../../environments/environment';
import {NavigationEnd, NavigationStart, Router} from '@angular/router';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent implements OnInit {

  iconUrl = `${environment.staticUrl}img/favicon.png`;
  isLoading = false;

  constructor(public authService: AuthService, private router: Router) {
  }

  ngOnInit(): void {
    this.router.events.subscribe(
      event => {
        if (event instanceof NavigationStart) {
          this.isLoading = true;
        } else if (event instanceof NavigationEnd) {
          this.isLoading = false;
        }
      }
    );
  }

}
