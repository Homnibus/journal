import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {OldPageListComponent} from './old-page-list.component';

describe('OldPageListComponent', () => {
  let component: OldPageListComponent;
  let fixture: ComponentFixture<OldPageListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [OldPageListComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OldPageListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
