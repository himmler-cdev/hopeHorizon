import {Component, OnInit} from '@angular/core';
import {BlogPostService} from '../blog-post.service';
import {BlogPostEntity} from '../entity/blog-post.entity';
import {DatePipe, NgClass, NgForOf} from '@angular/common';
import {MatCard, MatCardContent, MatCardHeader, MatCardTitle} from '@angular/material/card';
import {MatButton, MatIconButton} from '@angular/material/button';
import {MatIcon} from '@angular/material/icon';
import {BlogListCardComponent} from '../blog-list-card/blog-list-card.component';
import {MatFormField, MatLabel, MatSuffix} from '@angular/material/form-field';
import {MatInput} from '@angular/material/input';
import {MatOption, MatSelect} from '@angular/material/select';
import {FormControl, ReactiveFormsModule} from '@angular/forms';
import {MatChip} from '@angular/material/chips';

@Component({
  selector: 'app-blog-list',
  standalone: true,
  imports: [
    NgForOf,
    DatePipe,
    MatCard,
    MatCardTitle,
    MatCardHeader,
    MatCardContent,
    MatIconButton,
    MatIcon,
    BlogListCardComponent,
    MatFormField,
    MatInput,
    MatSelect,
    MatOption,
    MatLabel,
    MatSuffix,
    ReactiveFormsModule,
    MatChip,
    NgClass,
    MatButton
  ],
  templateUrl: './blog-list.component.html',
  styleUrl: './blog-list.component.scss'
})
export class BlogListComponent implements OnInit {
  blogPostList: BlogPostEntity[] = [];
  searchControl = new FormControl('');
  filterControl = new FormControl(null);
  options = [
    {value: 'option1', viewValue: 'Option 1'},
    {value: 'option2', viewValue: 'Option 2'},
    {value: 'option3', viewValue: 'Option 3'}
  ];

  constructor(private _blogPostService: BlogPostService) {
  }

  ngOnInit() {
    this._blogPostService.getBlogPosts().subscribe((blogPosts) => {
      blogPosts.map((blogPost) => {
        this.blogPostList.push(BlogPostEntity.fromDto(blogPost));
      });
    });
  }

  clearSearchFilter() {
    this.searchControl.setValue('');
  }
}
