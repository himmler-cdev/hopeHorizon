import { Component } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { Router, RouterModule } from '@angular/router';
import { UserService } from '../user.service';
import { UserEntity } from '../entity/user.entity';

@Component({
  selector: 'app-user-register',
  standalone: true,
  imports: [
    MatInputModule,
    MatFormFieldModule,
    MatButtonModule,
    RouterModule,
    ReactiveFormsModule,
  ],
  templateUrl: './user-register.component.html',
  styleUrl: './user-register.component.scss'
})
export class UserRegisterComponent {

  user = new UserEntity();
  registerForm: FormGroup;
  errorMessage: string = '';

  constructor(private userService: UserService, private router: Router) {
    this.registerForm = new FormGroup({
      username: new FormControl('', [Validators.required]),
      email : new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', [Validators.required]),
      password2: new FormControl('', [Validators.required]),
    });
  }

  onRegister() {
    if (this.registerForm.valid) {
      this.user.username = this.registerForm.value.username;
      this.user.email = this.registerForm.value.email;
      this.user.password = this.registerForm.value.password;
      this.userService.create(this.user).subscribe(
        response => {
          console.log('Registration successful', response);
          this.errorMessage = ''; // Clear any previous error message
          this.router.navigate(['/login']);
        },
        error => {
          console.error('Registration failed', error);
          this.errorMessage = 'An error occurred. Please try again later.';
        }
      );
    } else {
      this.errorMessage = 'Please enter your username, email, and password.';
    }
  }

  getErrorMessage(controlName: string): string {
    const control = this.registerForm.get(controlName);
    if (control && control.errors) {
      for (const error in control.errors) {
        if (control.errors.hasOwnProperty(error)) {
          switch (error) {
            case 'required':
              return 'This field is required';
            case 'email':
              return 'Please enter a valid email address';
            // Add more cases as needed for other validators
            default:
              return 'Invalid field';
          }
        }
      }
    }
    return '';
  }
}
