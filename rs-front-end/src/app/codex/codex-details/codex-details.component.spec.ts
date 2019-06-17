import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {CodexDetailsComponent} from './codex-details.component';

describe('CodexDetailsComponent', () => {
  let component: CodexDetailsComponent;
  let fixture: ComponentFixture<CodexDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CodexDetailsComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CodexDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
