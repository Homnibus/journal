import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {CodexAddComponent} from './codex-add.component';

describe('CodexAddComponent', () => {
  let component: CodexAddComponent;
  let fixture: ComponentFixture<CodexAddComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CodexAddComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CodexAddComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
