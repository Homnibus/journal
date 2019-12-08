import {Component, OnInit} from '@angular/core';
import {Codex, Note, Page, Task} from '../../app.models';
import {CodexDetailsService} from '../services/codex-details.service';
import {ActivatedRoute} from '@angular/router';
import {TaskService} from '../../task/task.service';
import {PageService} from '../../page/page.service';
import {NoteService} from '../../note/note.service';
import {PaginationContainer} from '../../core/services/model-pagination.service';

@Component({
  selector: 'app-codex-details',
  templateUrl: './codex-details.component.html',
  styleUrls: ['./codex-details.component.scss']
})
export class CodexDetailsComponent implements OnInit {

  codex: Codex;
  todayPage: Page;
  oldPageList: Page[];
  infiniteScrollDisabled = false;
  isLoadingNewPages = false;
  currentOldPagePage: PaginationContainer<Page>;
  currentOldPagePageNumber = 1;

  constructor(private codexDetailsService: CodexDetailsService,
              private taskService: TaskService,
              private noteService: NoteService,
              private pageService: PageService,
              private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.route.data.subscribe(data => {
      this.todayPage = data.todayPage;
      this.currentOldPagePage = data.oldPageListFirstPage;
      this.oldPageList = PageService.filterTodayPage(this.currentOldPagePage.results);
    });
    this.route.parent.data.subscribe(data => {
      this.codex = data.codex;
    });
  }

  createTaskInTodayPage(newTask: Task) {
    const taskCopy = Object.assign({}, newTask);
    taskCopy.codex = this.codex.id;
    this.taskService.create(taskCopy)
      .subscribe(task => this.todayPage = PageService.addCreatedTask(this.todayPage, task));
  }

  updateTaskInTodayPage(updatedTask: Task) {
    this.taskService.update(updatedTask)
      .subscribe(task => this.todayPage = this.pageService.updateTask(this.todayPage, task));
  }

  deleteTaskInTodayPage(deletedTask: Task) {
    this.taskService.delete(deletedTask)
      .subscribe(() => this.todayPage = this.pageService.deleteTask(this.todayPage, deletedTask));
  }

  updateTask(toUpdatePage: Page, updatedTask: Task) {
    this.taskService.update(updatedTask)
      .subscribe(task => this.oldPageList = this.pageService.updateList(this.oldPageList, this.pageService.updateTask(toUpdatePage, task)));
  }

  deleteTask(toUpdatePage: Page, deletedTask: Task) {
    this.taskService.delete(deletedTask)
      .subscribe(() => this.oldPageList = this.pageService.updateList(
        this.oldPageList,
        this.pageService.deleteTask(toUpdatePage, deletedTask)
      ));
  }

  trackByFn(index, item) {
    return item.id;
  }

  createNoteInTodayPage(newNote: Note) {
    const noteCopy = Object.assign({}, newNote);
    noteCopy.codex = this.codex.id;
    this.noteService.create(noteCopy)
      .subscribe(note => this.todayPage = PageService.addCreatedNote(this.todayPage, note));
  }

  updateNoteInTodayPage(updatedNote: Note) {
    this.noteService.update(updatedNote)
      .subscribe(note => this.todayPage = PageService.updateNote(this.todayPage, note));
  }

  deleteNoteInTodayPage(deletedNote: Note) {
    this.noteService.delete(deletedNote)
      .subscribe(() => this.todayPage = PageService.deleteNote(this.todayPage, deletedNote));
  }

  updateNote(toUpdatePage: Page, updatedNote: Note) {
    this.noteService.update(updatedNote)
      .subscribe(note => this.oldPageList = this.pageService.updateList(this.oldPageList, PageService.updateNote(toUpdatePage, note)));
  }

  deleteNote(toUpdatePage: Page, deletedNote: Note) {
    this.noteService.delete(deletedNote)
      .subscribe(() => this.oldPageList = this.pageService.updateList(this.oldPageList, PageService.deleteNote(toUpdatePage, deletedNote)));

  }

  onScroll() {
    // disable scroll down event
    this.infiniteScrollDisabled = true;
    if (this.currentOldPagePage.next) {
      this.isLoadingNewPages = true;
      this.currentOldPagePageNumber++;
      this.pageService.getCodexPage(this.codex.slug, this.currentOldPagePageNumber)
        .subscribe(paginationContent => {
          // Add the new page to global list
          this.oldPageList = this.oldPageList.concat(paginationContent.results);
          this.isLoadingNewPages = false;
          // Reactivate scroll down event if the is a next page
          if (paginationContent.next) {
            this.infiniteScrollDisabled = false;
          }
        });
    }
  }

}
