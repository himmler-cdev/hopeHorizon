import {Component} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {Router, RouterModule} from '@angular/router';
import {UserService} from '../user.service';
import {FormControl, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';

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
      const userData = this.loginForm.value;
      this.userService.login(userData).subscribe({
        next: (res: any) => {
          this.userService.loginCallback(userData.username, res.access);
        },
        error: (err) => {
          console.error(err);
          this.errorMessage = 'Invalid username or password';
        },
      });
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
            default:
              return 'Invalid field';
          }
        }
      }
    }
    return '';
  }
}
