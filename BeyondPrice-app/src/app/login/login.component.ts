import { Component } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import { RestService } from '../rest.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  loginForm: FormGroup;

  constructor(private api:RestService) { this.loginForm = new FormGroup({
    email: new FormControl(null, {  updateOn: 'submit' }),
    password: new FormControl(null, {  updateOn: 'submit' }),

  });}

  


  onSubmit() {
  
}
}