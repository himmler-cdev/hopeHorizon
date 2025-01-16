import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ForumUsersDto, ForumUserPostDto } from '../dto/forum-user.dto';
import { of, tap } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ForumUserService {
  constructor(private _http: HttpClient) {}

  getForumUsers() {
    return this._http.get<Readonly<ForumUsersDto>>('/api/forum-user/');
  }

  createForumUsers(forumUsers: ForumUserPostDto) {
    return this._http.post<Readonly<ForumUsersDto>>('/api/forum-user/', forumUsers);
  }

  deleteForumUser(id: number) {
    return this._http.delete(`/api/forum-user/${id}/`);
  }
}

