import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-prod-compare',
  templateUrl: './prod-compare.component.html',
  styleUrls: ['./prod-compare.component.scss']
})
export class ProdCompareComponent {
  constructor(private router: Router) { }
  shoeURL:string = "../assets/images/shoe.jpg"

}
