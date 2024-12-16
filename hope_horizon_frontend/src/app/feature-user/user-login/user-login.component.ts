import { Component, OnInit } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { RouterModule } from '@angular/router';
import { UserService } from '../user.service';
import { Router } from "@angular/router"
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-user-login',
  standalone: true,
  imports: [
    MatInputModule,
    MatFormFieldModule,
    MatButtonModule,
    RouterModule,
    ReactiveFormsModule,
  ],
  templateUrl: './user-login.component.html',
  styleUrl: './user-login.component.scss'
})
export class UserLoginComponent {

  loginForm: FormGroup;
  errorMessage: string = '';

  constructor(private userService: UserService, private router: Router) {
    this.loginForm = new FormGroup({
      username: new FormControl('', [Validators.required]),
      password: new FormControl('', [Validators.required]),
    });
  }

  onLogin() {
    if (this.loginForm.valid) {
      const { username, password } = this.loginForm.value;
      this.userService.login(username, password).subscribe(
        response => {
          console.log('Login successful', response);
          this.errorMessage = ''; // Clear any previous error message
          localStorage.setItem('access_token', response.access);
          localStorage.setItem('refresh_token', response.refresh);
          this.router.navigate(['/home']);
        },
        error => {
          console.error('Login failed', error);
          this.errorMessage = error.error.detail;
        }
      );
    } else {
      this.errorMessage = '';
    }
  }

  getErrorMessage(controlName: string): string {
    const control = this.loginForm.get(controlName);
    if (control && control.errors) {
      for (const error in control.errors) {
        if (control.errors.hasOwnProperty(error)) {
          switch (error) {
            case 'required':
              return controlName.toLocaleUpperCase() + ' is required';
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
