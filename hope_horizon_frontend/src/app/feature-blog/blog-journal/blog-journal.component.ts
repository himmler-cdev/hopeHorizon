import {Component, OnInit} from '@angular/core';
import {BlogListComponent} from '../blog-list/blog-list.component';
import {BlogPostEntity} from '../entity/blog-post.entity';
import {BlogPostService} from '../service/blog-post.service';
import {BlogPostTypeEntity} from '../entity/blog-post-type.entity';
import {BlogPostTypeService} from '../service/blog-post-type.service';
import {MatPaginator, PageEvent} from '@angular/material/paginator';

@Component({
  selector: 'app-blog-journal',
  standalone: true,
  imports: [
    BlogListComponent,
    MatPaginator
  ],
  templateUrl: './blog-journal.component.html'
})
export class BlogJournalComponent implements OnInit {
  blogPostList: BlogPostEntity[] = [];
  filterOptions: BlogPostTypeEntity[] = [];
  pageSizeOptions = [5, 10, 25];
  pageSize = 10;
  blogListLength = 10;
  currentPage = 0;
  searchQuery: string | null = '';
  selectedFilter: number | null = null;

  constructor(private _blogPostService: BlogPostService, private _blogPostTypeService: BlogPostTypeService) {
  }

  ngOnInit() {
    this.loadBlogPosts();

    this._blogPostTypeService.getBlogPostTypes().subscribe((response) => {
      response.blog_post_types.map((blogPostType) => {
        this.filterOptions.push(BlogPostTypeEntity.fromDto(blogPostType));
      });
    });
  }

  protected loadBlogPosts() {
    this._blogPostService.getBlogPosts({
      owned: 'true',
      page: (this.currentPage + 1).toString(),
      page_size: this.pageSize.toString(),
      search: this.searchQuery || '',
      blog_post_type_id: this.selectedFilter || ''
    }).subscribe((response) => {
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

  protected onFilterChange(filterValue: number | null) {
    this.selectedFilter = filterValue;
    this.currentPage = 0;
    this.loadBlogPosts();
  }
}
