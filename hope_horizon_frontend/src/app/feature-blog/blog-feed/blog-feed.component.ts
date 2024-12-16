import {Component, OnInit} from '@angular/core';
import {BlogPostService} from '../service/blog-post.service';
import {BlogPostEntity} from '../entity/blog-post.entity';
import {BlogListComponent} from '../blog-list/blog-list.component';

@Component({
  selector: 'app-blog-feed',
  standalone: true,
  imports: [
    BlogListComponent
  ],
  templateUrl: './blog-feed.component.html'
})
export class BlogFeedComponent implements OnInit {
  blogPostList: BlogPostEntity[] = [];

  constructor(private _blogPostService: BlogPostService) {
  }

  ngOnInit() {
    this._blogPostService.getBlogPosts().subscribe((blogPosts) => {
      blogPosts.map((blogPost) => {
        this.blogPostList.push(BlogPostEntity.fromDto(blogPost));
      });
    });
  }
}
