import { Component,ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-user-home-navbar',
  templateUrl: './user-home-navbar.component.html',
  styleUrls: ['./user-home-navbar.component.scss']
})
export class UserHomeNavbarComponent {
  constructor(private route: ActivatedRoute, private router: Router, private cd: ChangeDetectorRef) { }
  logoURL:string = "../assets/images/logo-green-logo.png"

  user_name: string;

  gotoUserDash() {
    this.router.navigate(['/userDash']);
  }
  gotoHome() {
    this.router.navigate(['/home']);
  }


  ngOnInit(): void {
    this.route.queryParams.subscribe((params: any)=> {
      this.user_name = params.user_name
      console.log(this.user_name)
    });
  
  
}
}



