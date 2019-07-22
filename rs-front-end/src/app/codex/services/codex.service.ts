import {Injectable} from '@angular/core';
import {Codex} from '../../app.models';
import {CodexSerializer} from '../../app.serializers';
import {ModelService} from '../../core/services/model.service';
import {ModificationRequestStatusService} from '../../core/services/modification-request-status.service';
import {AuthService} from '../../core/services/auth.service';

@Injectable({
  providedIn: 'root',
})
export class CodexService extends ModelService<Codex> {

  constructor(authService: AuthService, modificationRequestStatusService: ModificationRequestStatusService) {
    super(
      authService,
      Codex,
      new CodexSerializer(),
      modificationRequestStatusService
    );
  }

}
