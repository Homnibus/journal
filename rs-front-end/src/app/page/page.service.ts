import {formatDate} from '@angular/common';
import {Injectable} from '@angular/core';
import {PageSerializer} from '../app.serializers';
import {Note, Page, Task} from '../app.models';
import {Observable} from 'rxjs';
import {ModificationRequestStatusService} from '../core/services/modification-request-status.service';
import {AuthService} from '../core/services/auth.service';
import {map} from 'rxjs/operators';
import {TaskService} from '../task/task.service';
import {ModelPaginationService, PaginationContainer} from '../core/services/model-pagination.service';

@Injectable({
  providedIn: 'root',
})
export class PageService extends ModelPaginationService<Page> {

  constructor(authService: AuthService,
              modificationRequestStatusService: ModificationRequestStatusService,
              private taskService: TaskService,
  ) {
    super(
      authService,
      Page,
      new PageSerializer(),
      modificationRequestStatusService,
    );
  }

  static addCreatedTask(page: Page, addedTask: Task): Page {
    const pageCopy = Object.assign({}, page);
    pageCopy.tasks = [addedTask].concat(page.tasks);
    return pageCopy;
  }

  static filterTodayPage(pages: Page[]): Page[] {
    let filteredPages: Page[];
    if (pages.length > 0) {
      const lastPage = pages[0];
      if (formatDate(lastPage.date, 'yyyy-MM-dd', 'en') === formatDate(new Date(), 'yyyy-MM-dd', 'en')) {
        filteredPages = pages.slice(1);
      } else {
        filteredPages = Object.assign([], pages);
      }
    } else {
      filteredPages = [];
    }
    return filteredPages;
  }

  static addCreatedNote(page: Page, addedNote: Note): Page {
    const pageCopy = Object.assign({}, page);
    pageCopy.note = addedNote;
    return pageCopy;
  }

  static updateNote(page: Page, updatedNote: Note) {
    const pageCopy = Object.assign({}, page);
    pageCopy.note = Object.assign({}, updatedNote);
    return pageCopy;
  }

  static deleteNote(page: Page, deletedNote: Note) {
    const pageCopy = Object.assign({}, page);
    pageCopy.note = undefined;
    return pageCopy;
  }

  getCodexPage(codexSlug: string, pageNumber: number): Observable<PaginationContainer<Page>> {
    const filter = `codex__slug=${codexSlug}`;
    return this.filteredList(filter, pageNumber);
  }

  getTodayCodexPage(codexSlug: string): Observable<Page> {
    const today = formatDate(new Date(), 'yyyy-MM-dd', 'en');
    const filter = `codex__slug=${codexSlug}&date=${today}`;
    return this.filteredList(filter, 1).pipe(
      map(paginationContent => {
        let todayPage: Page;
        const pageList  = paginationContent.results;
        if (pageList.length > 0) {
          todayPage = pageList[0];
        } else {
          todayPage = new Page();
          todayPage.date = new Date();
        }
        return todayPage;
      })
    );
  }

  updateTask(page: Page, updatedTask: Task) {
    const pageCopy = Object.assign({}, page);
    const taskCopy = Object.assign({}, updatedTask);
    pageCopy.tasks = this.taskService.updateList(pageCopy.tasks, taskCopy);
    return pageCopy;
  }

  deleteTask(page: Page, deletedTask: Task) {
    const pageCopy = Object.assign({}, page);
    pageCopy.tasks = this.taskService.deleteFromList(pageCopy.tasks, deletedTask);
    return pageCopy;
  }
}
