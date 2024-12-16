import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {BlogPostTypeService} from '../service/blog-post-type.service';
import {BlogPostService} from '../service/blog-post.service';
import {BlogPostEntity} from '../entity/blog-post.entity';
import {Router} from '@angular/router';
import {MatFormField, MatLabel, MatSuffix} from '@angular/material/form-field';
import {BlogPostTypeEntity} from '../entity/blog-post-type.entity';
import {MatInput} from '@angular/material/input';
import {MatOption, MatSelect} from '@angular/material/select';
import {DatePipe, NgClass} from '@angular/common';
import {MatCard, MatCardContent, MatCardHeader, MatCardTitle} from '@angular/material/card';
import {MatButton, MatIconButton} from '@angular/material/button';
import {MatIcon} from '@angular/material/icon';
import {BlogListCardComponent} from '../blog-list-card/blog-list-card.component';
import {MatChip} from '@angular/material/chips';

@Component({
  selector: 'app-blog-form',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    MatFormField,
    MatInput,
    MatSelect,
    MatOption,
    MatLabel
  ],
  templateUrl: './blog-form.component.html',
  styleUrl: './blog-form.component.scss'
})
export class BlogFormComponent implements OnInit {
  blogFormGroup: FormGroup;
  blogPostId: number | undefined = undefined;
  blogPostTypes: BlogPostTypeEntity[] = [];

  constructor(private _blogPostTypeService: BlogPostTypeService, private _blogPostService: BlogPostService, private _router: Router) {
    this.blogFormGroup = new FormGroup({
      id: new FormControl(null),
      title: new FormControl('', [Validators.maxLength(250), Validators.required]),
      date: new FormControl(''),
      content: new FormControl('', Validators.required),
      blogPostTypeId: new FormControl(null, Validators.required)
    });
  }

  ngOnInit() {
    this._blogPostTypeService.getBlogPostTypes().subscribe((response) => {
      response.blog_post_types.map((blogPostType) => {
        this.blogPostTypes.push(BlogPostTypeEntity.fromDto(blogPostType));
      });
    });
  }

  private persistForm(): BlogPostEntity {
    const formValue = this.blogFormGroup.value;
    const entity = new BlogPostEntity();

    entity.id = formValue.id;
    entity.title = formValue.title;
    entity.date = formValue.date ? new Date(formValue.date) : undefined;
    entity.content = formValue.content;
    entity.blogPostTypeId = formValue.blogPostTypeId;

    return entity;
  }

  createOrUpdate() {
    if (this.blogFormGroup.invalid) {
      return;
    }

    const blogPostEntity = this.persistForm();

    if (this.blogPostId) {
      this._blogPostService.updateBlogPost(blogPostEntity.toDto()).subscribe((blog) => {
        this.blogFormGroup.reset();
        // this._router.navigate(['/blog', blog.id]);
      });
    } else {
      this._blogPostService.createBlogPost(blogPostEntity.toDto()).subscribe((blog) => {
        this.blogFormGroup.reset();
        // this._router.navigate(['/blog', blog.id]);
      });
    }
  }
}
