import {HttpClient} from '@angular/common/http';
import {Injectable, signal} from '@angular/core';
import {Router} from '@angular/router';
import {JwtHelperService} from '@auth0/angular-jwt';
import {Observable} from 'rxjs';
import {UserEntity} from './entity/user.entity';
import {UserDto} from './dto/user.dto';
import {map, tap} from 'rxjs/operators';

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
        this.jwtHelperService.getTokenExpirationDate(token)
      );
      const tokenValid = !this.jwtHelperService.isTokenExpired(token);
      this.isLoggedInSignal.set(tokenValid);
    }
  }

  getUserDataImmediate(): UserEntity | null {
    if (localStorage.getItem('user')) {
      this.loggedInUser = UserEntity.fromDto(
        JSON.parse(localStorage.getItem('user') as string),
      );
    }
    return this.loggedInUser;
  }

  login(userData: { username: string; password: string }): Observable<UserDto> {
    return this._http.post('/api/login/', userData);
  }

  loginCallback(username: string, accessToken: string): void {
    this.isLoggedInSignal.set(true);
    localStorage.setItem('access_token', accessToken);
    this.router.navigate(['blog-list']);
    this._http.get<UserDto>(`/api/user/${username}`).subscribe({
      next: (user) => {
        this.loggedInUser = UserEntity.fromDto(user);
        localStorage.setItem('user', JSON.stringify(user));
      }
    });
  }

  logout(): void {
    localStorage.removeItem(this.accessTokenLocalStorageKey);
    localStorage.removeItem('user');
    this.isLoggedInSignal.set(false);
    this.router.navigate(['/login']);
  }

  create(user: UserEntity): Observable<UserDto> {
    return this._http.post<UserDto>('/api/user/', user.toDto());
  }

  update(user: UserEntity): Observable<UserDto> {
    return this._http.put<UserDto>(`/api/user/${user.id}/`, user.toDto());
  }

  delete(user: UserEntity): Observable<any> {
    return this._http.delete<any>(`/api/user/${user.id}/`);
  }

  getAllUsers(): Observable<UserDto[]> {
    return this._http
      .get<{ users: UserDto[] }>('/api/user/', { withCredentials: true })
      .pipe(
        tap((response) => console.log('API Response:', response)),
        map((response) => response.users)
      );
  }
}
