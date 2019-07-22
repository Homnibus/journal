import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {CodexEditComponent} from './codex-edit.component';

describe('CodexEditComponent', () => {
  let component: CodexEditComponent;
  let fixture: ComponentFixture<CodexEditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CodexEditComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CodexEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
