import {Component, OnInit} from '@angular/core';
import {AbstractControl, FormControl, FormGroup, ReactiveFormsModule, ValidatorFn, Validators} from '@angular/forms';
import {BlogPostTypeService} from '../service/blog-post-type.service';
import {BlogPostService} from '../service/blog-post.service';
import {BlogPostEntity} from '../entity/blog-post.entity';
import {Router, RouterLink} from '@angular/router';
import {MatError, MatFormField, MatLabel} from '@angular/material/form-field';
import {BlogPostTypeEntity} from '../entity/blog-post-type.entity';
import {MatInput} from '@angular/material/input';
import {MatOption, MatSelect} from '@angular/material/select';
import {MatButton} from '@angular/material/button';
import {MatDialog} from '@angular/material/dialog';
import {ConfirmDialogComponent} from '../../../shared/dialogs/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-blog-form',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    MatFormField,
    MatInput,
    MatSelect,
    MatOption,
    MatLabel,
    MatButton,
    RouterLink,
    MatError
  ],
  templateUrl: './blog-form.component.html',
  styleUrl: './blog-form.component.scss'
})
export class BlogFormComponent implements OnInit {
  blogFormGroup: FormGroup;
  blogPostId: number | undefined = undefined;
  blogPostTypes: BlogPostTypeEntity[] = [];

  constructor(
    private _blogPostTypeService: BlogPostTypeService,
    private _blogPostService: BlogPostService,
    private _router: Router,
    private _dialog: MatDialog
  ) {
    this.blogFormGroup = new FormGroup({
      id: new FormControl(null),
      title: new FormControl('', [Validators.maxLength(250), Validators.required, this.whitespaceValidator()]),
      date: new FormControl(''),
      content: new FormControl('', [Validators.required, this.whitespaceValidator()]),
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

  protected createOrUpdate() {
    if (this.blogFormGroup.invalid) {
      return;
    }

    const blogPostEntity = this.persistForm();

    if (this.blogPostId) {
      this._blogPostService.updateBlogPost(blogPostEntity.toDto()).subscribe((blog) => {
        this._router.navigate(['/blog/', blog.id]);
      });
    } else {
      this._blogPostService.createBlogPost(blogPostEntity.toDto()).subscribe((blog) => {
        this.blogFormGroup.reset();
        this._router.navigate(['/blog/', blog.id]);
      });
    }
  }

  protected openDeleteDialog() {
    const dialogRef = this._dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Delete Blog Post',
        message: 'Are you sure you want to delete this blog post?',
        confirmText: 'Delete',
        cancelText: 'Cancel'
      }
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this._deleteBlogPost();
      }
    });
  }

  protected openCancelDialog() {
    const dialogRef = this._dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Clear Form',
        message: 'Are you sure you want to clear the form?',
        confirmText: 'Clear',
        cancelText: 'Cancel'
      }
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this._clearForm();
      }
    });
  }

  private _clearForm() {
    // TODO: Discuss clear strategy with team
    this.blogFormGroup.reset();
  }

  private _deleteBlogPost() {
    if (!this.blogPostId) {
      return;
    }

    this._blogPostService.deleteBlogPost(this.blogPostId).subscribe(() => {
      this._router.navigate(['/journal']);
    });
  }

  private whitespaceValidator(): ValidatorFn {
    return (control: AbstractControl) => {
      if (!control.value) {
        return null;
      }
      const isWhitespace = (control.value || '').trim().length === 0;
      const isValid = !isWhitespace;
      return isValid ? null : {'whitespace': true};
    };
  }
}
