import {Component, Input, OnInit} from '@angular/core';
import {Codex, Page, Task} from '../../app.models';
import {PageService} from '../page.service';

@Component({
  selector: 'app-today-page',
  templateUrl: './today-page.component.html',
  styleUrls: ['./today-page.component.scss']
})
export class TodayPageComponent implements OnInit {

  @Input() codex: Codex;
  dataSource: Page;
  private editableNote = false;

  constructor(private pageService: PageService) {
  }

  ngOnInit() {
    this.getTodayPage();
  }

  getTodayPage(): void {
    this.pageService.getTodayCodexPage(this.codex.slug).subscribe(
      data => {
        this.dataSource = this.initTodayPage(data);
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
    this.dataSource.tasks.unshift(task);
  }

  switchEditMode() {
    this.editableNote = !this.editableNote;
  }

}
