import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CkeditorDisplayComponent } from './ckeditor-display.component';

describe('CkeditorDisplayComponent', () => {
  let component: CkeditorDisplayComponent;
  let fixture: ComponentFixture<CkeditorDisplayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CkeditorDisplayComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CkeditorDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
