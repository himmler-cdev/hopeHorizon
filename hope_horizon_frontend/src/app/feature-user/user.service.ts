import {HttpClient} from '@angular/common/http';
import {Injectable, signal} from '@angular/core';
import {Router} from '@angular/router';
import {JwtHelperService} from '@auth0/angular-jwt';
import {catchError, map, Observable, switchMap, throwError} from 'rxjs';
import {UserEntity} from './entity/user.entity';
import {UserDto, UsersDto} from './dto/user.dto';

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

  getUserId(): number {
    const token = localStorage.getItem(this.accessTokenLocalStorageKey);
    if (token) {
      const tokenPayload = this.jwtHelperService.decodeToken(token);
      return tokenPayload.user_id;
    }
    return -1;
  }

  getAllUsers(): Observable<UsersDto> {
    const cachedUsers = localStorage.getItem('cached_users');
    if (cachedUsers) {
      return new Observable(observer => {
        observer.next(JSON.parse(cachedUsers));
        observer.complete();
      });
    }

    return this.http.get<UsersDto>('/api/user/').pipe(
      map(users => {
        localStorage.setItem('cached_users', JSON.stringify(users));
        return users;
      })
    );
  }

  getUserData(id: number){
    return this.getAllUsers().pipe(
      map(response => {
        const user = response.users.find(user => user.id === id);
        if (!user) {
          throw new Error('User not found');
        }
        return user.username;
      }),
      switchMap(username => this.http.get<UserDto>(`/api/user/${username}`))
    );
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
