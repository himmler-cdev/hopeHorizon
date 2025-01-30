import {Component, OnInit, ViewChild} from '@angular/core';
import {BlogPostService} from '../service/blog-post.service';
import {BlogPostEntity} from '../entity/blog-post.entity';
import {BlogListComponent} from '../blog-list/blog-list.component';
import {MatPaginator, PageEvent} from '@angular/material/paginator';
import {UserService} from '../../feature-user/user.service';
import {UserEntity} from '../../feature-user/entity/user.entity';

@Component({
  selector: 'app-blog-feed',
  standalone: true,
  imports: [
    BlogListComponent,
    MatPaginator
  ],
  templateUrl: './blog-feed.component.html'
})
export class BlogFeedComponent implements OnInit {
  blogPostList: BlogPostEntity[] = [];
  pageSizeOptions = [5, 10, 25];
  pageSize = 10;
  blogListLength = 10;
  currentPage = 0;
  searchQuery: string | null = '';
  user: UserEntity | null = null;

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(private _blogPostService: BlogPostService, private _userService: UserService) {
  }

  ngOnInit() {
    this.user = this._userService.getUserDataImmediate();
    this.loadBlogPosts();
  }

  protected loadBlogPosts() {
    const queryParams: any = {
      owned: 'false',
      page: (this.currentPage + 1).toString(),
      page_size: this.pageSize.toString(),
      search: this.searchQuery || ''
    };

    this._blogPostService.getBlogPosts(queryParams).subscribe((response) => {
      this.blogPostList = response.blog_posts.map(BlogPostEntity.fromDto);
      this.blogListLength = response.page_information.total_size;
    });
  }

  protected onPageChange(event: PageEvent) {
    this.currentPage = event.pageIndex;
    this.pageSize = event.pageSize;
    this.loadBlogPosts();
  }

  protected onSearchChange(searchValue: string | null) {
    this.searchQuery = searchValue?.trim() || '';
    this.currentPage = 0;
    this.loadBlogPosts();
  }
}
