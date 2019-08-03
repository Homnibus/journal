import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {WebPageSubtitleComponent} from './web-page-subtitle.component';

describe('WebPageSubtitleComponent', () => {
  let component: WebPageSubtitleComponent;
  let fixture: ComponentFixture<WebPageSubtitleComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [WebPageSubtitleComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WebPageSubtitleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
