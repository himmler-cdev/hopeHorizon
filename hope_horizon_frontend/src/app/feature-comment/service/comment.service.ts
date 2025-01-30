import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CommentDto, CommentsDto } from '../dto/comment.dto';

@Injectable({
  providedIn: 'root',
})
export class CommentService {
  private readonly API_URL = '/api/comment/';

  constructor(private _http: HttpClient) {}

  getComments(queryParams?: Record<string, string | number>) {
    return this._http.get<Readonly<CommentsDto>>(this.API_URL, { params: queryParams });
  }

  getComment(comment: CommentDto) {
    return this._http.get<Readonly<CommentDto>>(`${this.API_URL}${comment.id}/`);
  }

  createComment(comment: CommentDto) {
    return this._http.post<Readonly<CommentDto>>(this.API_URL, comment);
  }

  updateComment(comment: CommentDto) {
    if (comment.id === undefined) {
        throw new Error('Cannot update a comment without an id');
      }
    return this._http.put<Readonly<CommentDto>>(`${this.API_URL}${comment.id}/`, comment);
  }

  deleteComment(comment: CommentDto) {
    console.log('Deleting comment:', comment);
    console.log('URL:', `${this.API_URL}${comment.id}/`);
    return this._http.delete(`${this.API_URL}${comment.id}/`);
  }
}
