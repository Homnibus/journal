import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {WebPageHeaderComponent} from './web-page-header.component';

describe('WebPageHeaderComponent', () => {
  let component: WebPageHeaderComponent;
  let fixture: ComponentFixture<WebPageHeaderComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [WebPageHeaderComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WebPageHeaderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
