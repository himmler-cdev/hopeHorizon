import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ForumUsersDto, ForumUserPostDto } from '../dto/forum-user.dto';
import { Observable, of, tap } from 'rxjs';
import { MockData } from './mockdata';

@Injectable({
  providedIn: 'root',
})
export class ForumUserService {

  private mockData = new MockData();
  forumList = this.mockData.forumList;
  loggedInUser = this.mockData.loggedInUser;
  forumUserList = this.mockData.forumUserList;



  constructor(private _http: HttpClient) {}

  getAllUsers(): Observable<ForumUsersDto> {
    //return this._http.get<Readonly<ForumUsersDto>>('/api/user'); TODO when Users API is ready
    return of({ forum_users: this.forumUserList.forum_users });
  }

  getForumUsers(forumId: number): Observable<ForumUsersDto> {
    //return this._http.get<Readonly<ForumUsersDto>>(`/api/forum-user?forum_id=${forumId}`);
    const forumUsers = this.forumUserList.forum_users.filter(forumUser => forumUser.forum_id === forumId);
    return of({ forum_users: forumUsers });
  }

  createForumUsers(forumUsers: ForumUserPostDto): Observable<ForumUsersDto> {
    //return this._http.post<Readonly<ForumUsersDto>>('/api/forum-user/', forumUsers);
    const newId = this.forumUserList.forum_users.length + 1;
    forumUsers.users?.map(user => {
      this.forumUserList.forum_users.push({
        id: newId,
        is_owner: false,
        forum_id: forumUsers.forum_id,
        user_id: user.user_id,
        username: 'fish' + user.user_id,
      });
    });
    return of({ forum_users: this.forumUserList.forum_users });
  }

  deleteForumUser(id: number): Observable<ForumUsersDto> {
    //return this._http.delete(`/api/forum-user/${id}/`);
    const index = this.forumUserList.forum_users.findIndex(forumUser => forumUser.id === id);
    this.forumUserList.forum_users.splice(index, 1);
    return of({ forum_users: this.forumUserList.forum_users });
  }
}

