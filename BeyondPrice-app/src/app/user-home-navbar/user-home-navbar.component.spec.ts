import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserHomeNavbarComponent } from './user-home-navbar.component';

describe('UserHomeNavbarComponent', () => {
  let component: UserHomeNavbarComponent;
  let fixture: ComponentFixture<UserHomeNavbarComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UserHomeNavbarComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UserHomeNavbarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
