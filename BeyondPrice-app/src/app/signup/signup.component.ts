import { Component } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import { RestService } from '../rest.service';
@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})
export class SignupComponent {
  validationForm: FormGroup;
  showpassword: boolean = false;
  showPassword = false;
  showConfPassword = false;

  constructor(private api:RestService) {
    this.validationForm = new FormGroup({
      firstName: new FormControl(null, {  updateOn: 'submit' }),
      lastName: new FormControl(null, {  updateOn: 'submit' }),
      email: new FormControl(null, {  updateOn: 'submit' }),
      phone: new FormControl(null, { updateOn: 'submit' }),
      userPassword: new FormControl(null, {  updateOn: 'submit' }),
      confirmPassword: new FormControl(null, { updateOn: 'submit' }),

    });
  }

  get firstName(): AbstractControl {
    return this.validationForm.get('firstName')!;
  }

  get lastName(): AbstractControl {
    return this.validationForm.get('lastName')!;
  }

  get email(): AbstractControl {
    return this.validationForm.get('email')!;
  }

  get phone(): AbstractControl {
    return this.validationForm.get('phone')!;
  }

  get userPassword(): AbstractControl {
    return this.validationForm.get('userPassword')!;
  }
  get confirmPassword(): AbstractControl {
    return this.validationForm.get('confirmPassword')!;
  }

  onSubmit(): void {
    // this.validationForm.markAllAsTouched();
    console.log(this.validationForm.value)
    console.log(this.validationForm.get('email').value)
    this.api.postSignupData(this.validationForm.get('firstName').value
    ,this.validationForm.get('lastName').value
    ,this.validationForm.get('email').value
    ,this.validationForm.get('phone').value
    ,this.validationForm.get('userPassword').value)
  }

  toggleShowPassword() {
    this.showpassword = !this.showpassword;
  }
}
