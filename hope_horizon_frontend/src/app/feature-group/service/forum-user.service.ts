import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {ForumUserDto, ForumUserPostDto, ForumUsersDto} from '../dto/forum-user.dto';
import {forkJoin, Observable, of} from 'rxjs';
import {MockData} from './mockdata';

@Injectable({
  providedIn: 'root',
})
export class ForumUserService {

  constructor(private _http: HttpClient) {
  }

  getForumUsers(forumId: number): Observable<ForumUsersDto> {
    return this._http.get<Readonly<ForumUsersDto>>(`/api/forum-user?forum_id=${forumId}`);

    /*
    const forumUsers = this.forumUserList.forum_users.filter(forumUser => forumUser.forum_id === forumId);
    return of({forum_users: forumUsers});
    */
  }

  createForumUsers(forumUsers: ForumUserPostDto): Observable<ForumUserPostDto> {
    return this._http.post<Readonly<ForumUserPostDto>>('/api/forum-user/', forumUsers);

    /*
    let newId = this.forumUserList.forum_users.length + 1;
    forumUsers.forum_users?.forEach(user => {
      this.forumUserList.forum_users.push({
        id: newId++, // Increment ID for each user
        is_owner: false,
        forum_id: forumUsers.forum_users[0].forum_id,
        user_id: user.user_id,
        username: user.username,
      });
    });
    return of({forum_users: this.forumUserList.forum_users});
    */
  }
  

  deleteForumUser(id: number) {
    return this._http.delete(`/api/forum-user/${id}/`);
  }

  deleteForumUsers(userIds: number[]) {
    const deleteRequests = userIds.map((id) => this.deleteForumUser(id)); 
    return forkJoin(deleteRequests);
  }
}
