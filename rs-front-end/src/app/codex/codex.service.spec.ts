import {TestBed} from '@angular/core/testing';

import {CodexService} from './codex.service';

describe('CodexService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: CodexService = TestBed.get(CodexService);
    expect(service).toBeTruthy();
  });
});
