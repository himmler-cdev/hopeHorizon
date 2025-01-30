import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {ForumUserPostDto, ForumUsersDto} from '../dto/forum-user.dto';
import {forkJoin, Observable} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ForumUserService {

  constructor(private _http: HttpClient) {
  }

  getForumUsers(forumId: number): Observable<ForumUsersDto> {
    return this._http.get<Readonly<ForumUsersDto>>(`/api/forum-user?forum_id=${forumId}`);
  }

  createForumUsers(forumUsers: ForumUserPostDto): Observable<ForumUserPostDto> {
    return this._http.post<Readonly<ForumUserPostDto>>('/api/forum-user/', forumUsers);
  }


  deleteForumUser(id: number) {
    return this._http.delete(`/api/forum-user/${id}/`);
  }

  deleteForumUsers(userIds: number[]) {
    const deleteRequests = userIds.map((id) => this.deleteForumUser(id));
    return forkJoin(deleteRequests);
  }
}
