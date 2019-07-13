import {Component, Input} from '@angular/core';
import {Task} from 'src/app/app.models';
import {slideTopTransition} from "../../shared/slide-top.animations";

@Component({
  selector: 'app-task-list',
  templateUrl: './task-list.component.html',
  styleUrls: ['./task-list.component.scss'],
  animations: [slideTopTransition]
})
export class TaskListComponent {

  @Input()
  private taskList: Task[];
  @Input()
  private editable = false;
  @Input()
  private allowChangeEditable = true;

  constructor() {
  }

  trackByFn(index, item) {
    return item.id;
  }
}
