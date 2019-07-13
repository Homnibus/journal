import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {CodexDetailsTabsComponent} from './codex-details-tabs.component';

describe('CodexDetailsTabsComponent', () => {
  let component: CodexDetailsTabsComponent;
  let fixture: ComponentFixture<CodexDetailsTabsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CodexDetailsTabsComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CodexDetailsTabsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
