import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {FormControl} from '@angular/forms';
import {Subscription} from 'rxjs';
import {debounceTime} from 'rxjs/operators';

@Component({
  selector: 'app-button',
  templateUrl: './check-box.component.html',
  styleUrls: ['./check-box.component.scss']
})
export class CheckBoxComponent implements OnInit {

  @Input()
  id: number;
  @Input()
  checked: boolean;
  @Output()
  changed = new EventEmitter<boolean>();

  checkboxControl: FormControl;
  checkboxControlOnChange: Subscription;

  constructor() {
  }

  ngOnInit() {
    this.checkboxControl = new FormControl(this.checked);
    this.checkboxControlOnChange = this.checkboxControl.valueChanges.pipe(
      debounceTime(400),
    ).subscribe(value => this.changed.emit(value));
  }

}
