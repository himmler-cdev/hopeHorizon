import {Component, OnInit} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatError, MatFormField, MatLabel} from '@angular/material/form-field';
import {MatInput} from '@angular/material/input';
import {BlogPostEntity} from '../entity/blog-post.entity';
import {ActivatedRoute, RouterLink} from '@angular/router';
import {BlogPostService} from '../service/blog-post.service';
import {MatButton} from '@angular/material/button';
import {UserService} from '../../feature-user/user.service';
import {CdkTextareaAutosize} from '@angular/cdk/text-field';

@Component({
  selector: 'app-blog-detail',
  standalone: true,
  imports: [
    FormsModule,
    MatFormField,
    MatInput,
    MatLabel,
    ReactiveFormsModule,
    MatButton,
    RouterLink,
    MatError,
    CdkTextareaAutosize
  ],
  templateUrl: './blog-detail.component.html',
  styleUrl: './blog-detail.component.scss'
})
export class BlogDetailComponent implements OnInit {
  blogPost: BlogPostEntity | null = null;
  userId = -1;

  constructor(private _route: ActivatedRoute, private _blogPostService: BlogPostService, private _userService: UserService) {
  }

  ngOnInit() {
    const blogPostId = Number(this._route.snapshot.paramMap.get('id'));

    if (blogPostId) {
      this._blogPostService.getBlogPost(blogPostId).subscribe((blogDto) => {
        this.blogPost = BlogPostEntity.fromDto(blogDto);
      });
    }

    this.userId = this._userService.getUserDataImmediate()?.id || -1;
  }
}
