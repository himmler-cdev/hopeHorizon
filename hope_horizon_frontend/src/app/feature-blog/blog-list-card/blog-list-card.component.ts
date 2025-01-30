import {Component, Input, OnInit} from '@angular/core';
import {MatCard, MatCardContent, MatCardHeader, MatCardTitle} from "@angular/material/card";
import {MatIcon} from "@angular/material/icon";
import {MatIconButton} from "@angular/material/button";
import {BlogPostEntity} from '../entity/blog-post.entity';
import {Router} from '@angular/router';
import {BlogPostTypeEntity} from '../entity/blog-post-type.entity';

@Component({
  selector: 'app-blog-list-card',
  standalone: true,
  imports: [
    MatCard,
    MatCardContent,
    MatCardHeader,
    MatCardTitle,
    MatIcon,
    MatIconButton
  ],
  templateUrl: './blog-list-card.component.html',
  styleUrl: './blog-list-card.component.scss'
})
export class BlogListCardComponent {
  @Input({required: true}) blog!: BlogPostEntity;
  @Input({required: true}) blogPostTypes!: BlogPostTypeEntity[];
  @Input({required: true}) blogPostType!: string;
  @Input() forumName: string | null = null;

  constructor(private _router: Router) {
  }

  openBlogPost() {
    this._router.navigate(['/blog/', this.blog.id]);
  }
}
