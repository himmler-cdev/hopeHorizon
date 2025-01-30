import {Injectable} from '@angular/core';
import {BlogPostDto, BlogPostsDto} from '../dto/blog-post.dto';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class BlogPostService {

  constructor(private _http: HttpClient) {
  }

  getBlogPosts(queryParams?: Record<string, string | number | boolean>) {
    return this._http.get<Readonly<BlogPostsDto>>('/api/blog-post/', {params: queryParams});
  }

  getBlogPost(id: number) {
    return this._http.get<Readonly<BlogPostDto>>(`/api/blog-post/${id}/`);
  }

  createBlogPost(blogPost: BlogPostDto) {
    return this._http.post<Readonly<BlogPostDto>>('/api/blog-post/', blogPost);
  }

  updateBlogPost(blogPost: BlogPostDto) {
    if (blogPost.id === undefined) {
      throw new Error('Cannot update a blog post without an id');
    }

    return this._http.put<Readonly<BlogPostDto>>(`/api/blog-post/${blogPost.id}/`, blogPost);
  }

  deleteBlogPost(id: number) {
    return this._http.delete(`/api/blog-post/${id}/`);
  }
}
