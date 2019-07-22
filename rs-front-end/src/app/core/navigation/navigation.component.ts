import {Component} from '@angular/core';
import {AuthService} from "../services/auth.service";
import {environment} from "../../../environments/environment";

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent {

  iconUrl = `${environment.staticUrl}img/favicon.png`;

  constructor(public authService: AuthService) {
  }
}
