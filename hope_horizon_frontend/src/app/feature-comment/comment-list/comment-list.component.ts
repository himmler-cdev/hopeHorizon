import {Component, EventEmitter, Input, Output} from '@angular/core';
import {CommentCardComponent} from '../comment-card/comment-card.component';
import {MatList, MatListItem} from '@angular/material/list';
import {CommentEntity} from '../entity/comment.entity';

@Component({
  selector: 'app-comment-list',
  standalone: true,
  imports: [CommentCardComponent, MatList, MatListItem],
  templateUrl: './comment-list.component.html',
  styleUrl: './comment-list.component.scss'
})
export class CommentListComponent {
  @Input() comments: CommentEntity[] = [];
  @Output() commentDeleted = new EventEmitter<number>();

  removeComment(commentId: number): void {
    this.comments = this.comments.filter(comment => comment.id !== commentId);
    this.commentDeleted.emit(commentId);
  }
}
