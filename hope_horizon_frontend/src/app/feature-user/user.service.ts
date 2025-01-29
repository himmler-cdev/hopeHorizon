import {HttpClient} from '@angular/common/http';
import {Injectable, signal} from '@angular/core';
import {Router} from '@angular/router';
import {JwtHelperService} from '@auth0/angular-jwt';
import {Observable} from 'rxjs';
import {UserEntity} from './entity/user.entity';
import {UserDto} from './dto/user.dto';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  readonly accessTokenLocalStorageKey = 'access_token';
  isLoggedInSignal = signal(false);
  loggedInUser: UserEntity | null = null;

  constructor(
    private _http: HttpClient,
    private router: Router,
    private jwtHelperService: JwtHelperService,
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

  getUserDataImmediate(): UserEntity | null {
    return this.loggedInUser;
  }

  login(userData: { username: string; password: string }): boolean {
    let loggedInSuccessfully = false;
    this._http.post('/api/login/', userData).subscribe({
      next: (res: any) => {
        this.isLoggedInSignal.set(true);
        localStorage.setItem('access_token', res.access);
        this.router.navigate(['blog-list']); // TODO: home page
        loggedInSuccessfully = true;
        this._http.get<UserDto>(`/api/user/${userData.username}`).subscribe({
          next: (user) => {
            this.loggedInUser = UserEntity.fromDto(user);
          }
        });
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
    return this._http.post<UserDto>('/api/user/', user.toDto());
  }
}
