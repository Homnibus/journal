import {Component, Input, OnInit} from '@angular/core';
import {Page} from '../../app.models';

@Component({
  selector: 'app-page-details',
  templateUrl: './page-details.component.html',
  styleUrls: ['./page-details.component.scss']
})
export class PageDetailsComponent implements OnInit {

  @Input()
  page: Page;
  private noteEditable = false;
  private taskEditable = false;

  constructor() {
  }

  ngOnInit() {
  }

  switchNoteEditMode(): void {
    this.noteEditable = !this.noteEditable;
  }

  switchTaskEditMode(): void {
    this.taskEditable = !this.taskEditable;
  }

}
