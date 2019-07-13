import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {CodexInformationComponent} from './codex-information.component';

describe('CodexInformationComponent', () => {
  let component: CodexInformationComponent;
  let fixture: ComponentFixture<CodexInformationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CodexInformationComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CodexInformationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
