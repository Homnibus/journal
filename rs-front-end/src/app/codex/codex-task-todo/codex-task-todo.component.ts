import {Component, OnInit} from '@angular/core';
import {TaskService} from '../../task/task.service';
import {Observable} from 'rxjs';
import {Task} from 'src/app/app.models';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-codex-task-todo',
  templateUrl: './codex-task-todo.component.html',
  styleUrls: ['./codex-task-todo.component.scss']
})
export class CodexTaskTodoComponent implements OnInit {

  taskList$: Observable<Task[]>;
  codexSlug: string;

  constructor(private taskService: TaskService, private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.codexSlug = this.route.snapshot.paramMap.get('slug');
    this.taskList$ = this.taskService.getCodexToDoTask(this.codexSlug);
  }

}
