import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {CodexTaskTodoComponent} from './codex-task-todo.component';

describe('CodexTaskTodoComponent', () => {
  let component: CodexTaskTodoComponent;
  let fixture: ComponentFixture<CodexTaskTodoComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CodexTaskTodoComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CodexTaskTodoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
