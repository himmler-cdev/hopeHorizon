import {Component, EventEmitter, Input, Output} from '@angular/core';
import { FormControl, FormGroup, Validators, ValidatorFn, AbstractControl, ReactiveFormsModule } from '@angular/forms';
import { CommentEntity } from '../entity/comment.entity';
import { CommentService } from '../service/comment.service';
import { MatCard } from '@angular/material/card';
import { MatError, MatFormField, MatLabel } from '@angular/material/form-field';
import { MatInput } from '@angular/material/input';
import { MatButton } from '@angular/material/button';

@Component({
  selector: 'app-comment-form',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    MatCard,
    MatFormField,
    MatInput,
    MatButton,
    MatLabel,
    MatError
  ],
  templateUrl: './comment-form.component.html',
  styleUrl: './comment-form.component.scss'
})
export class CommentFormComponent {
  @Input() blogPostId!: number;
  @Output() commentAdded = new EventEmitter<CommentEntity>();
  submitting = false;

  commentForm = new FormGroup({
    content: new FormControl('', [
      Validators.required,
      Validators.maxLength(500),
      this.whitespaceValidator()
    ])
  });

  constructor(private commentService: CommentService) {}

  submitComment(): void {
    if (this.commentForm.invalid) return;

    this.submitting = true;

    // Create CommentEntity from form data
    const newCommentEntity = new CommentEntity({
      content: this.commentForm.value.content as string,
      blog_post_id: this.blogPostId // Ensure this ID is dynamically set
    });

    this.commentService.createComment(newCommentEntity.toDto()).subscribe(
      (commentDto) => {
        console.log('Comment Created:', commentDto);
        const createdComment = CommentEntity.fromDto(commentDto);
        this.commentAdded.emit(createdComment);

        // Reset the form and clear validation state
        this.commentForm.reset();
        this.commentForm.controls['content'].setErrors(null);
        this.commentForm.controls['content'].markAsPristine();
        this.commentForm.controls['content'].markAsUntouched();

        this.submitting = false;
      },
      (error) => {
        console.error('Failed to create comment', error);
        this.submitting = false;
      }
    );
  }

  private whitespaceValidator(): ValidatorFn {
    return (control: AbstractControl) => {
      if (!control.value) return null;
      const isWhitespace = (control.value || '').trim().length === 0;
      return isWhitespace ? { whitespace: true } : null;
    };
  }
}
