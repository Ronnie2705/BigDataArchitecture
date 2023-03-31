import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserDashFilterComponent } from './user-dash-filter.component';

describe('UserDashFilterComponent', () => {
  let component: UserDashFilterComponent;
  let fixture: ComponentFixture<UserDashFilterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UserDashFilterComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UserDashFilterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
