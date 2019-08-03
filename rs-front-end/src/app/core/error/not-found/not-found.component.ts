import {Component} from '@angular/core';
import {environment} from '../../../../environments/environment';

@Component({
  selector: 'app-not-found',
  templateUrl: './not-found.component.html',
  styleUrls: ['./not-found.component.scss']
})
export class NotFoundComponent {

  notFoundImgUrl = `${environment.staticUrl}img/404_castle.png`;

  constructor() {
  }
}
