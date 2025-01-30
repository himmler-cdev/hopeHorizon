import { Injectable } from '@angular/core';
import { ForumDto, ForumsDto } from '../dto/forum.dto';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ForumService {
  constructor(private _http: HttpClient) {}

  getForums(owner: boolean): Observable<ForumsDto> {
    return this._http.get<Readonly<ForumsDto>>('/api/forum?owned=' + owner);
  }

  getForum(id: number): Observable<ForumDto> {
    return this._http.get<Readonly<ForumDto>>(`/api/forum/${id}/`);
  }

  createForum(forum: ForumDto): Observable<ForumDto> {
    return this._http.post<Readonly<ForumDto>>('/api/forum/', forum);
  }

  updateForum(forum: ForumDto): Observable<ForumDto> {
    if (forum.id === undefined) {
      throw new Error('Cannot update a blog post without an id');
    }
    return this._http.put<Readonly<ForumDto>>(`/api/forum/${forum.id}/`, forum);
  }

  deleteForum(id: number): Observable<ForumDto> {
    return this._http.delete(`/api/forum/${id}/`);
  }
}
