import {Injectable} from '@angular/core';
import {ModelService} from '../core/services/model.service';
import {ModificationRequestStatusService} from '../core/services/modification-request-status.service';
import {TaskSerializer} from '../app.serializers';
import {Task} from '../app.models';
import {AuthService} from '../core/services/auth.service';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class TaskService extends ModelService<Task> {

  constructor(authService: AuthService, modificationRequestStatusService: ModificationRequestStatusService) {
    super(
      authService,
      Task,
      new TaskSerializer(),
      modificationRequestStatusService
    );
  }

  static taskShouldBeDeleted(taskText: string): boolean {
    return (taskText === '');
  }

  getCodexToDoTask(codexSlug: string): Observable<Task[]> {
    const filter = `page__codex__slug=${codexSlug}&is_achieved=false`;
    return this.filteredList(filter);
  }
}
