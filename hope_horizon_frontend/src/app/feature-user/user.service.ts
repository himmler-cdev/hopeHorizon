import { HttpClient } from '@angular/common/http';
import { Injectable, signal } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { JwtHelperService } from '@auth0/angular-jwt';
import { BehaviorSubject, Observable } from 'rxjs';
import { UserEntity } from './entity/user.entity';
import { UserDto } from './dto/user.dto';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  readonly accessTokenLocalStorageKey = 'access_token';
  isLoggedInSignal = signal(false);

  constructor(
    private http: HttpClient,
    private router: Router,
    private jwtHelperService: JwtHelperService,
    private snackbar: MatSnackBar,
  ) {
    const token = localStorage.getItem(this.accessTokenLocalStorageKey);
    if (token) {
      console.log(
        'Token expiration date: ' +
          this.jwtHelperService.getTokenExpirationDate(token),
      );
      const tokenValid = !this.jwtHelperService.isTokenExpired(token);
      this.isLoggedInSignal.set(tokenValid);
    }
  }

  login(userData: { username: string; password: string }): boolean {
    let loggedInSuccessfully = false;
    this.http.post('/api/login/', userData).subscribe({
      next: (res: any) => {
        this.isLoggedInSignal.set(true);
        localStorage.setItem('access_token', res.access);
        this.router.navigate(['blog-list']); // TODO: home page
        loggedInSuccessfully = true;
      },
    });

    return loggedInSuccessfully;
  }

  logout(): void {
    localStorage.removeItem(this.accessTokenLocalStorageKey);
    this.isLoggedInSignal.set(false);
    this.router.navigate(['/login']);
  }

  create(user: UserEntity): Observable<UserDto> {
    return this.http.post<UserDto>('/api/user/', user.toDto());
  }
}
