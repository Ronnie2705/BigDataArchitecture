import { Component } from '@angular/core';

import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent {
  constructor(private router: Router) { }
  logoURL:string = "../assets/images/logo-green-logo.png"

  gotoLogin() {
    this.router.navigate(['/login']);
  }
  gotoAbout() {
    this.router.navigate(['/about']);
  }
  gotoHome() {
    this.router.navigate(['/home']);
  }
}


