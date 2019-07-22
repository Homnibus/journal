import {Component, OnInit} from '@angular/core';
import {TaskService} from '../../task/task.service';
import {Observable} from 'rxjs';
import {Codex, Task} from 'src/app/app.models';
import {CodexDetailsService} from "../services/codex-details.service";
import {filter, switchMap} from "rxjs/operators";

@Component({
  selector: 'app-codex-task-todo',
  templateUrl: './codex-task-todo.component.html',
  styleUrls: ['./codex-task-todo.component.scss']
})
export class CodexTaskTodoComponent implements OnInit {

  taskList$: Observable<Task[]>;
  codex$: Observable<Codex>;
  editable = false;

  constructor(private taskService: TaskService, private codexDetailsService: CodexDetailsService) {
  }

  ngOnInit() {
    this.codex$ = this.codexDetailsService.activeCodex$;
    this.taskList$ = this.codex$.pipe(
      filter(codex => codex != undefined),
      switchMap(codex => this.taskService.getCodexToDoTask(codex.slug))
    );
  }

  switchEditMode() {
    this.editable = !this.editable;
  }

}
