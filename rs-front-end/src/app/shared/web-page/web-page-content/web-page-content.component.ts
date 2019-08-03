import {Component, Input} from '@angular/core';
import {webPageSize} from '../web-page/web-page.component';

@Component({
  selector: 'app-web-page-content',
  templateUrl: './web-page-content.component.html',
  styleUrls: ['./web-page-content.component.scss']
})
export class WebPageContentComponent {

  @Input()
  pageSize: webPageSize = webPageSize.Medium;

  constructor() {
  }

}
