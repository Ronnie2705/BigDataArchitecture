import { Component } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})
export class SignupComponent {
  validationForm: FormGroup;

  constructor() {
    this.validationForm = new FormGroup({
      firstName: new FormControl(null, { validators: Validators.required, updateOn: 'submit' }),
      lastName: new FormControl(null, { validators: Validators.required, updateOn: 'submit' }),
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
    this.validationForm.markAllAsTouched();
  }
}
