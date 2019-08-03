import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {WebPageActionMenuComponent} from './web-page-action-menu.component';

describe('WebPageActionMenuComponent', () => {
  let component: WebPageActionMenuComponent;
  let fixture: ComponentFixture<WebPageActionMenuComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [WebPageActionMenuComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WebPageActionMenuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
