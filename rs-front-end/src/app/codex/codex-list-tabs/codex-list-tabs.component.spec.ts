import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {CodexListTabsComponent} from './codex-list-tabs.component';

describe('CodexListTabsComponent', () => {
  let component: CodexListTabsComponent;
  let fixture: ComponentFixture<CodexListTabsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CodexListTabsComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CodexListTabsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
