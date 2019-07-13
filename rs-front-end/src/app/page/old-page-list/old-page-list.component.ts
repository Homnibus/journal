import {Component, Input, OnInit} from '@angular/core';
import {Codex, Page} from '../../app.models';
import {PageService} from '../page.service';
import {formatDate} from '@angular/common';

@Component({
  selector: 'app-old-page-list',
  templateUrl: './old-page-list.component.html',
  styleUrls: ['./old-page-list.component.scss']
})
export class OldPageListComponent implements OnInit {

  @Input() codex: Codex;
  private dataSource: Page[];

  constructor(private pageService: PageService) {
  }

  ngOnInit() {
    this.getPage();
  }

  getPage(): void {
    this.pageService.getCodexPage(this.codex.slug).subscribe(
      data => {
        this.dataSource = this.filterTodayPage(data);
      }
    );
  }

  filterTodayPage(pages: Page[]): Page[] {
    let filteredPages: Page[];
    if (pages.length > 0) {
      const lastPage = pages[0];
      if (formatDate(lastPage.date, 'yyyy-MM-dd', 'en') === formatDate(new Date(), 'yyyy-MM-dd', 'en')) {
        filteredPages = pages.slice(1);
      } else {
        filteredPages = Array.from(pages);
      }
    } else {
      filteredPages = [];
    }
    return filteredPages;
  }
}
