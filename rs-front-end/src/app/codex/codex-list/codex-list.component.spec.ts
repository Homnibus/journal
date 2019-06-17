import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {CodexListComponent} from './codex-list.component';

describe('CodexListComponent', () => {
  let component: CodexListComponent;
  let fixture: ComponentFixture<CodexListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CodexListComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CodexListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
