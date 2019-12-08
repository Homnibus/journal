import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Note, Page, Task} from '../../app.models';
import {slideTopTransition} from '../../shared/slide-top.animations';

@Component({
  selector: 'app-page-details',
  templateUrl: './page-details.component.html',
  styleUrls: ['./page-details.component.scss'],
  animations: [slideTopTransition]
})
export class PageDetailsComponent implements OnInit {

  @Input() page: Page;

  @Output() taskUpdated = new EventEmitter<Task>();
  @Output() taskDeleted = new EventEmitter<Task>();
  @Output() noteUpdated = new EventEmitter<Note>();
  @Output() noteDeleted = new EventEmitter<Note>();

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

  trackByFn(index, item) {
    return item.id;
  }

  updateTaskText(taskToUpdate: Task, updatedTaskText: string) {
    const taskCopy = Object.assign({}, taskToUpdate);
    taskCopy.text = updatedTaskText;
    this.taskUpdated.emit(taskCopy);
  }

  updateTaskIsAchieved(taskToUpdate: Task, updatedTaskIsAchieved: boolean) {
    const taskCopy = Object.assign({}, taskToUpdate);
    taskCopy.isAchieved = updatedTaskIsAchieved;
    this.taskUpdated.emit(taskCopy);
  }

  deleteTask(deletedTask: Task): void {
    this.taskDeleted.emit(deletedTask);
  }


  updateNoteText(noteToUpdate: Note, updatedNoteText: string) {
    const noteCopy = Object.assign({}, noteToUpdate);
    noteCopy.text = updatedNoteText;
    this.noteUpdated.emit(noteCopy);
  }

  deleteNote(deletedNote: Note) {
    this.noteDeleted.emit(deletedNote);
  }
}
