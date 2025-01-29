import {Injectable} from '@angular/core';
import {ForumDto, ForumsDto} from '../dto/forum.dto';
import {HttpClient} from '@angular/common/http';
import {Observable, of} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ForumService {
  //private mockData = new MockData();
  //forumList = this.mockData.forumList;
  //loggedInUser = this.mockData.loggedInUser;
  //forumUserList = this.mockData.forumUserList;

  private apiUrl = 'http://127.0.0.1:8000/api/forum';

  constructor(private _http: HttpClient) {
  }

  getForums(): Observable<ForumsDto> {
    return this._http.get<Readonly<ForumsDto>>('/api/forum?owned=true');
    /*
    // Filter forums based on the logged-in user
    const userForums = this.forumUserList.forum_users
      .filter(forumUser => forumUser.user_id === this.loggedInUser.id)
      .map(forumUser => this.forumList.forums.find(forum => forum.id === forumUser.forum_id))
      .filter(forum => forum !== undefined) as ForumDto[];
    return of({ forums: userForums });
    */
  }

  getForum(id: number): Observable<ForumDto> {
    //return this._http.get<Readonly<ForumDto>>(`/api/forum/${id}/`);
    const forum = this.forumList.forums.find(forum => forum.id === id);
    if (!forum) {
      throw new Error(`Forum with id ${id} not found`);
    }
    return of(forum);
  }

  createForum(forum: ForumDto): Observable<ForumDto> {
    //return this._http.post<Readonly<ForumDto>>('/api/forum/', forum);
    const newId = this.forumList.forums.length + 1;
    forum.id = newId;

    this.forumList.forums.push(forum);
    this.forumUserList.forum_users.push({
      id: this.forumUserList.forum_users.length + 1,
      is_owner: true,
      forum_id: forum.id,
      user_id: this.loggedInUser.id,
      username: this.loggedInUser.username,
    });
    return of(forum);
  }

  updateForum(forum: ForumDto): Observable<ForumDto> {
    if (forum.id === undefined) {
      throw new Error('Cannot update a blog post without an id');
    }

    //return this._http.put<Readonly<ForumDto>>(`/api/forum/${forum.id}/`, forum);
    const index = this.forumList.forums.findIndex(forum => forum.id === forum.id);
    return of(this.forumList.forums[index] = forum);

  }

  deleteForum(id: number): Observable<void> {
    //return this._http.delete(`/api/forum/${id}/`);
    const index = this.forumList.forums.findIndex(forum => forum.id === id);
    this.forumList.forums.splice(index, 1);
    this.forumUserList.forum_users = this.forumUserList.forum_users.filter(forumUser => forumUser.forum_id !== id);
    return of(void 0);
  }
}
