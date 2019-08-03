import {Component, Input, OnInit} from '@angular/core';
import {Codex, Page, Task} from '../../app.models';
import {PageService} from '../page.service';
import {TaskService} from '../../task/task.service';
import {slideTopTransition} from '../../shared/slide-top.animations';

@Component({
  selector: 'app-today-page',
  templateUrl: './today-page.component.html',
  styleUrls: ['./today-page.component.scss'],
  animations: [slideTopTransition]
})
export class TodayPageComponent implements OnInit {

  @Input() codex: Codex;
  page: Page;
  taskList: Task[] = [];
  private editableNote = false;

  constructor(private taskService: TaskService, private pageService: PageService) {
  }

  ngOnInit() {
    this.getTodayPage();
  }

  getTodayPage(): void {
    this.pageService.getTodayCodexPage(this.codex.slug).subscribe(
      data => {
        this.page = this.initTodayPage(data);
        this.taskList = this.page.tasks;
      }
    );
  }

  initTodayPage(pages: Page[]): Page {
    let todayPage: Page;
    if (pages.length > 0) {
      todayPage = pages[0];
    } else {
      todayPage = new Page();
      todayPage.date = new Date();
    }
    return todayPage;
  }

  addTask(task: Task): void {
    this.taskList.unshift(task);
  }

  switchEditMode() {
    this.editableNote = !this.editableNote;
  }

  trackByFn(index, item) {
    return item.id;
  }

  taskDelete(taskDeleted: Task) {
    this.taskList = this.taskService.deleteFromTaskList(this.taskList, taskDeleted);
  }
}
