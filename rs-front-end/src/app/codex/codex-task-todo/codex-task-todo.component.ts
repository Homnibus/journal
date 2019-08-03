import {Component, OnInit} from '@angular/core';
import {TaskService} from '../../task/task.service';
import {Observable} from 'rxjs';
import {Codex, Task} from 'src/app/app.models';
import {CodexDetailsService} from '../services/codex-details.service';
import {filter, switchMap} from 'rxjs/operators';
import {slideTopTransition} from '../../shared/slide-top.animations';

@Component({
  selector: 'app-codex-task-todo',
  templateUrl: './codex-task-todo.component.html',
  styleUrls: ['./codex-task-todo.component.scss'],
  animations: [slideTopTransition]
})
export class CodexTaskTodoComponent implements OnInit {

  codex$: Observable<Codex>;
  taskList: Task[] = [];
  editable = false;

  constructor(private taskService: TaskService, private codexDetailsService: CodexDetailsService) {
  }

  ngOnInit() {
    this.codex$ = this.codexDetailsService.activeCodex$;
    this.codex$.pipe(
      filter(codex => codex !== undefined),
      switchMap(codex => this.taskService.getCodexToDoTask(codex.slug))
    ).subscribe(taskList => this.taskList = taskList);
  }

  switchEditMode() {
    this.editable = !this.editable;
  }

  trackByFn(index, item) {
    return item.id;
  }

  taskDelete(taskDeleted: Task) {
    this.taskList = this.taskService.deleteFromTaskList(this.taskList, taskDeleted);
  }
}
