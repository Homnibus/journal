import {Component} from '@angular/core';
import {environment} from '../../../../environments/environment';

@Component({
  selector: 'app-unexpected',
  templateUrl: './unexpected.component.html',
  styleUrls: ['./unexpected.component.scss']
})
export class UnexpectedComponent {

  unexpectedImgUrl = `${environment.staticUrl}img/500_shadoks.gif`;

  constructor() {
  }

}
