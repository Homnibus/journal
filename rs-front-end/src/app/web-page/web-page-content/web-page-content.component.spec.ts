import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {WebPageContentComponent} from './web-page-content.component';

describe('WebPageContentComponent', () => {
  let component: WebPageContentComponent;
  let fixture: ComponentFixture<WebPageContentComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [WebPageContentComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WebPageContentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
