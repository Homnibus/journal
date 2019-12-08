import { Injectable } from '@angular/core';
import {ActivatedRouteSnapshot, Resolve, RouterStateSnapshot} from '@angular/router';
import {Task} from '../app.models';
import {Observable} from 'rxjs';
import {TaskService} from './task.service';

@Injectable({
  providedIn: 'root'
})
export class TaskResolver implements Resolve<Task[]> {

  constructor(private taskService: TaskService) { }

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<Task[]> {
    const codex = route.parent.data.codex;
    return this.taskService.getCodexToDoTask(codex.slug);
  }
}
