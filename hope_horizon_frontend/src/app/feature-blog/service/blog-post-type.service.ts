import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {BlogPostTypesDto} from '../dto/blog-post-type.dto';
import {of, tap} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class BlogPostTypeService {
  private _cachedBlogPostTypes: Readonly<BlogPostTypesDto> | null = null;

  constructor(private _http: HttpClient) {
  }

  getBlogPostTypes() {
    if (this._cachedBlogPostTypes) {
      return of(this._cachedBlogPostTypes);
    }

    return this._http.get<Readonly<BlogPostTypesDto>>('/api/blog-post-type/').pipe(
      tap(data => this._cachedBlogPostTypes = data)
    );
  }
}
