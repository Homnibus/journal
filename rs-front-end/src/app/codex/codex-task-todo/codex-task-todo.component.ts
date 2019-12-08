import {Component, OnInit} from '@angular/core';
import {TaskService} from '../../task/task.service';
import {Codex, Task} from 'src/app/app.models';
import {CodexDetailsService} from '../services/codex-details.service';
import {slideTopTransition} from '../../shared/slide-top.animations';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-codex-task-todo',
  templateUrl: './codex-task-todo.component.html',
  styleUrls: ['./codex-task-todo.component.scss'],
  animations: [slideTopTransition]
})
export class CodexTaskTodoComponent implements OnInit {

  codex: Codex;
  taskList: Task[] = [];
  editable = false;

  constructor(private taskService: TaskService,
              private codexDetailsService: CodexDetailsService,
              private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.route.data.subscribe(data => {
      this.taskList = data.taskList;
    });
    this.route.parent.data.subscribe(data => {
      this.codex = data.codex;
    });

  }

  switchEditMode() {
    this.editable = !this.editable;
  }

  trackByFn(index, item) {
    return item.id;
  }

  updateTaskText(taskToUpdate: Task, updatedTaskText: string): void {
    const taskCopy = Object.assign({}, taskToUpdate);
    taskCopy.text = updatedTaskText;
    this.updateTask(taskCopy);
  }

  updateTaskIsAchieved(taskToUpdate: Task, updateTaskIsAchieved: boolean) {
    const taskCopy = Object.assign({}, taskToUpdate);
    taskCopy.isAchieved = updateTaskIsAchieved;
    this.updateTask(taskCopy);
  }

  updateTask(taskToUpdate: Task): void {
    const taskCopy = Object.assign({}, taskToUpdate);
    this.taskService.update(taskCopy)
      .subscribe(task => this.taskList = this.taskService.updateList(this.taskList, task));
  }

  deleteTask(taskToDelete: Task) {
    this.taskService.delete(taskToDelete)
      .subscribe(() => this.taskList = this.taskService.deleteFromList(this.taskList, taskToDelete));
  }
}
