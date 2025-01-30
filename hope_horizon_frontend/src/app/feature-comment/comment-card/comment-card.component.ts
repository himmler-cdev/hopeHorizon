import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
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
import {ConfirmDialogComponent} from '../../../shared/dialogs/confirm-dialog/confirm-dialog.component';
import {MatDialog} from '@angular/material/dialog';
import {UserService} from '../../feature-user/user.service';
import {MatInput} from '@angular/material/input';

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
    MatButton,
    MatInput
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
    private _fb: FormBuilder,
    private _commentService: CommentService,
    private _userService: UserService,
    private _snackBar: MatSnackBar,
    private _dialog: MatDialog,
  ) {
  }

  ngOnInit(): void {
    this.editForm = this._fb.group({
      content: [this.comment.content, [Validators.required, Validators.maxLength(500), this.whitespaceValidator()]]
    });
  }

  get displayUsername(): string {
    return this.comment.username || 'Anonymous';
  }

  canEditComment(): boolean {
    const user = this._userService.getUserDataImmediate();
    return user?.id === this.comment.userId || user?.user_role === 'Moderator';

  }

  startEdit(): void {
    if (this.isEditing) {
      this.cancelEdit();
    }

    this.isEditing = true;
    this.editForm.setValue({content: this.comment.content});
  }

  confirmEdit(): void {
    if (this.editForm.invalid) {
      this.editForm.markAllAsTouched();
      this._snackBar.open('Comment must be between 1 and 500 characters.', 'Close', {duration: 3000});
      return;
    }

    const updatedComment = new CommentEntity({
      ...this.comment,
      content: this.editForm.value.content,
      user_id: this.comment.userId,
      blog_post_id: this.comment.blogPostId,
      date: new Date().toDateString()
    });

    this._commentService.updateComment(updatedComment.toDto()).subscribe({
      next: (commentDto) => {
        this.comment = CommentEntity.fromDto(commentDto);

        this.comment.id = updatedComment.id;
        this.comment.blogPostId = updatedComment.blogPostId;
        this.comment.userId = updatedComment.userId;
        this.comment.username = updatedComment.username;
        this.comment.date = updatedComment.date;

        this.isEditing = false;
        this._snackBar.open('Comment updated successfully', 'Close', {duration: 3000});
      },
      error: (err) => {
        this._snackBar.open('Failed to update comment', 'Close', {duration: 3000});
        console.error(err);
      }
    });
  }

  cancelEdit(): void {
    const dialogRef = this._dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Cancel Edit',
        message: 'Are you sure you want to cancel editing this comment?',
        confirmText: 'Yes',
        cancelText: 'No'
      }
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.isEditing = false;
      }
    });
  }

  protected openDeleteDialog() {
    const dialogRef = this._dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Delete Comment',
        message: 'Are you sure you want to delete this comment?',
        confirmText: 'Delete',
        cancelText: 'Cancel'
      }
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        const commentDto = this.comment.toDto();
        this._commentService.deleteComment(commentDto).subscribe(() => {
          this.commentDeleted.emit(this.comment.id);
        })
        this._snackBar.open('Comment deleted successfully', 'Close', {duration: 3000});
      }
    });
  }

  private whitespaceValidator(): ValidatorFn {
    return (control: AbstractControl) => {
      if (!control.value) return null;
      const isWhitespace = (control.value || '').trim().length === 0;
      return isWhitespace ? {whitespace: true} : null;
    };
  }
}
