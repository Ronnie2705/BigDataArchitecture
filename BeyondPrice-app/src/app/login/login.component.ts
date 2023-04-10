import { Component } from '@angular/core';
import { AbstractControl, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { RestService } from '../rest.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  loginForm: FormGroup;

  password: string;
  showPassword = false;

  constructor(private api:RestService) 
  { this.loginForm = new FormGroup({
    email: new FormControl(null, {  updateOn: 'submit' }),
    password: new FormControl(null, {  updateOn: 'submit' }),

  });}



  onSubmit() {
    // this.validationForm.markAllAsTouched();
    console.log(this.loginForm.value)
    console.log(this.loginForm.get('email').value)
    this.api.postlogin(this.loginForm.get('email').value
    ,this.loginForm.get('password').value)
  }
  
}
