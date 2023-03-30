import { Component, OnInit} from '@angular/core';
import { AbstractControl, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  showErrorMessage = false;

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
    });
  }

  get email(): AbstractControl {
    return this.loginForm.get('email')!;
  }

  get password(): AbstractControl {
    return this.loginForm.get('password')!;
  }

  onSubmit() {
    if (this.loginForm.invalid) {
      // form is invalid, show error message
      this.showErrorMessage = true;
      return;
    }

    // perform login check
    const email = this.email.value;
    const password = this.password.value;

    if (email === 'example@email.com' && password === 'password') {
      // login successful, redirect to home page
      console.log('Login successful!');
      // Redirect the user to the home page using Angular Router
    } else {
      // login failed, show error message
      console.log('Login failed!');
      // Display an error message in the UI using a Toast or Alert component
    }
  }
}



