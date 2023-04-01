import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProdCompareComponent } from './prod-compare.component';

describe('ProdCompareComponent', () => {
  let component: ProdCompareComponent;
  let fixture: ComponentFixture<ProdCompareComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProdCompareComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProdCompareComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
