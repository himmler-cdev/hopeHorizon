import {Component, OnInit} from '@angular/core';
import {BlogListComponent} from '../blog-list/blog-list.component';
import {BlogPostEntity} from '../entity/blog-post.entity';
import {BlogPostService} from '../service/blog-post.service';
import {BlogPostTypeEntity} from '../entity/blog-post-type.entity';
import {BlogPostTypeService} from '../service/blog-post-type.service';

@Component({
  selector: 'app-blog-journal',
  standalone: true,
  imports: [
    BlogListComponent
  ],
  templateUrl: './blog-journal.component.html'
})
export class BlogJournalComponent implements OnInit {
  blogPostList: BlogPostEntity[] = [];
  filterOptions: BlogPostTypeEntity[] = [];

  constructor(private _blogPostService: BlogPostService, private _blogPostTypeService: BlogPostTypeService) {
  }

  ngOnInit() {
    this._blogPostService.getBlogPosts().subscribe((blogPosts) => {
      blogPosts.map((blogPost) => {
        this.blogPostList.push(BlogPostEntity.fromDto(blogPost));
      });
    });

    this._blogPostTypeService.getBlogPostTypes().subscribe((response) => {
      response.blog_post_types.map((blogPostType) => {
        this.filterOptions.push(BlogPostTypeEntity.fromDto(blogPostType));
      });
    });
  }
}
