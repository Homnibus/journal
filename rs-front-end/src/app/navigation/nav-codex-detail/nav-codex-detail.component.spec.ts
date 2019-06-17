import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {NavCodexDetailComponent} from './nav-codex-detail.component';

describe('NavCodexDetailComponent', () => {
  let component: NavCodexDetailComponent;
  let fixture: ComponentFixture<NavCodexDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [NavCodexDetailComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NavCodexDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
