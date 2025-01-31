import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {CommentDto, CommentsDto} from '../dto/comment.dto';

@Injectable({
  providedIn: 'root',
})
export class CommentService {
  private readonly API_URL = '/api/comment/';

  constructor(private _http: HttpClient) {
  }

  getComments(queryParams?: Record<string, string | number>) {
    return this._http.get<Readonly<CommentsDto>>(this.API_URL, {params: queryParams});
  }

  getComment(commentId: number) {
    return this._http.get<Readonly<CommentDto>>(`${this.API_URL}${commentId}/`);
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
    return this._http.delete(`${this.API_URL}${comment.id}/`);
  }
}
