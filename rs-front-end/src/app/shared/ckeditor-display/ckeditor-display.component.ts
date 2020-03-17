import {Component, Input} from '@angular/core';
import {DomSanitizer} from '@angular/platform-browser';

@Component({
  selector: 'app-ckeditor-display',
  templateUrl: './ckeditor-display.component.html',
  styleUrls: ['./ckeditor-display.component.scss']
})
export class CkeditorDisplayComponent {

  @Input()
  content: string;

  constructor(public sanitizer: DomSanitizer) { }
}
