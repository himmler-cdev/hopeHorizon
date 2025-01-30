import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {CommentDto} from '../dto/comment.dto';
import {MatCard, MatCardActions, MatCardContent, MatCardHeader, MatCardTitle} from '@angular/material/card';
import {MatDivider} from '@angular/material/divider';
import {MatIcon} from '@angular/material/icon';
import {MatButton, MatIconButton} from '@angular/material/button';
import {MatToolbar} from '@angular/material/toolbar';
import {MatFormField, MatLabel} from '@angular/material/form-field';
import {CommentEntity} from '../entity/comment.entity';
import {AbstractControl, FormBuilder, FormGroup, ReactiveFormsModule, ValidatorFn, Validators} from '@angular/forms';
import {MatSnackBar} from '@angular/material/snack-bar';
import {CommentService} from '../service/comment.service';

@Component({
  selector: 'app-comment-card',
  standalone: true,
  imports: [
    MatCard,
    MatCardHeader,
    MatCardContent,
    MatDivider,
    MatCardActions,
    MatIcon,
    MatIconButton,
    MatCardTitle,
    MatToolbar,
    MatFormField,
    MatLabel,
    ReactiveFormsModule,
    MatButton
  ],
  templateUrl: './comment-card.component.html',
  styleUrl: './comment-card.component.scss'
})
export class CommentCardComponent implements OnInit {
  @Input() comment!: CommentEntity;
  @Output() commentDeleted = new EventEmitter<number>(); // Emit event when comment is deleted

  isEditing = false;
  editForm!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private commentService: CommentService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.editForm = this.fb.group({
      content: [this.comment.content, [Validators.required, Validators.maxLength(500), this.whitespaceValidator()]]
    });
  }

  get displayUsername(): string {
    return this.comment.username || 'Anonymous';
  }

  canEditComment(): boolean {
    // Implement logic to check if the current user can edit this comment
    // For example, check if the current user is the author of the comment
    return true; // Replace with actual logic
  }

  startEdit(): void {
    this.isEditing = true;
    this.editForm.setValue({ content: this.comment.content });
  }

  confirmEdit(): void {
    if (this.editForm.invalid) {
      return;
    }

    const updatedComment = new CommentEntity({
      ...this.comment,
      content: this.editForm.value.content,
      blog_post_id: this.editForm.value.blog_post_id,
      date: Date.now().toString()
    });

    this.commentService.updateComment(updatedComment.toDto()).subscribe({
      next: (commentDto) => {
        const updatedCommentEntity = CommentEntity.fromDto(commentDto);
        this.comment = updatedCommentEntity;
        this.isEditing = false;
        this.snackBar.open('Comment updated successfully', 'Close', { duration: 3000 });
      },
      error: (err) => {
        this.snackBar.open('Failed to update comment', 'Close', { duration: 3000 });
        console.error(err);
      }
    });
  }

  cancelEdit(): void {
    this.isEditing = false;
  }

  deleteComment(): void {
    if (confirm('Are you sure you want to delete this comment?')) {
      this.commentService.deleteComment(this.comment.id!).subscribe({
        next: () => {
          this.snackBar.open('Comment deleted successfully', 'Close', { duration: 3000 });
          this.commentDeleted.emit(this.comment.id); // Notify parent component
        },
        error: (err) => {
          this.snackBar.open('Failed to delete comment', 'Close', { duration: 3000 });
          console.error(err);
        }
      });
    }
  }

  private whitespaceValidator(): ValidatorFn {
    return (control: AbstractControl) => {
      if (!control.value) return null;
      const isWhitespace = (control.value || '').trim().length === 0;
      return isWhitespace ? { whitespace: true } : null;
    };
  }
}
