import {Component, Input, OnInit} from '@angular/core';
import {Page, Task} from '../../app.models';
import {TaskService} from '../../task/task.service';
import {slideTopTransition} from '../../shared/slide-top.animations';

@Component({
  selector: 'app-page-details',
  templateUrl: './page-details.component.html',
  styleUrls: ['./page-details.component.scss'],
  animations: [slideTopTransition]
})
export class PageDetailsComponent implements OnInit {

  @Input() page: Page;
  taskList: Task[] = [];
  private noteEditable = false;
  private taskEditable = false;

  constructor(private taskService: TaskService) {
  }

  ngOnInit() {
    this.taskList = this.page.tasks;
  }

  switchNoteEditMode(): void {
    this.noteEditable = !this.noteEditable;
  }

  switchTaskEditMode(): void {
    this.taskEditable = !this.taskEditable;
  }

  trackByFn(index, item) {
    return item.id;
  }

  taskDelete(taskDeleted: Task) {
    this.taskList = this.taskService.deleteFromTaskList(this.taskList, taskDeleted);
  }

}
