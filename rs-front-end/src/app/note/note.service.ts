import {Injectable} from '@angular/core';
import {ModelService} from '../core/services/model.service';
import {NoteSerializer} from '../app.serializers';
import {Note} from '../app.models';
import {ModificationRequestStatusService} from '../core/services/modification-request-status.service';
import {AuthService} from '../core/services/auth.service';

@Injectable({
  providedIn: 'root',
})
export class NoteService extends ModelService<Note> {

  constructor(authService: AuthService, modificationRequestStatusService: ModificationRequestStatusService) {
    super(
      authService,
      Note,
      new NoteSerializer(),
      modificationRequestStatusService
    );
  }

  static noteShouldBeDeleted(noteText: string): boolean {
    return (noteText === '');
  }
}
