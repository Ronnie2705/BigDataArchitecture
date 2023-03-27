import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  constructor(private router: Router) { }
  bigDealURL:string = "../assets/images/bigdeal.png"

  gotoLogin() {
    this.router.navigate(['/login']);
  }
  gotoSignup() {
    this.router.navigate(['/signup']);
  }
  

}
