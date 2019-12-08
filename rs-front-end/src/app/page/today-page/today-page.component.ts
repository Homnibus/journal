import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Note, Page, Task} from '../../app.models';
import {slideTopTransition} from '../../shared/slide-top.animations';


@Component({
  selector: 'app-today-page',
  templateUrl: './today-page.component.html',
  styleUrls: ['./today-page.component.scss'],
  animations: [slideTopTransition]
})
export class TodayPageComponent implements OnInit {

  @Input() page: Page;

  @Output() taskCreated = new EventEmitter<Task>();
  @Output() taskUpdated = new EventEmitter<Task>();
  @Output() taskDeleted = new EventEmitter<Task>();
  @Output() noteCreated = new EventEmitter<Note>();
  @Output() noteUpdated = new EventEmitter<Note>();
  @Output() noteDeleted = new EventEmitter<Note>();

  private editableNote = false;

  constructor() {
  }

  ngOnInit() {}

  createTask(addedTask: Task): void {
    this.taskCreated.emit(addedTask);
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

  switchEditMode() {
    this.editableNote = !this.editableNote;
  }

  trackByFn(index, item) {
    return item.id;
  }

  createNote(addedNote: Note) {
    this.noteCreated.emit(addedNote);
  }

  updateNoteText(noteToUpdate: Note, updatedNoteText: string) {
    const noteCopy = Object.assign({}, noteToUpdate);
    noteCopy.text = updatedNoteText;
    this.noteUpdated.emit(noteCopy);
  }

  deleteNote(deletedNote: any) {
    this.noteDeleted.emit(deletedNote);
  }
}
