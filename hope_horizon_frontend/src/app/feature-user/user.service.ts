import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { UserEntity } from './entity/user.entity';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(private http: HttpClient) { }

  login(username: string, password: string): Observable<any> {
    const body = { username, password };
    return this.http.post<any>('/api/login/', body);
  }

  create(user: UserEntity): Observable<any> {
    return this.http.post<any>('/api/register/', user.toDto());
  }
}
