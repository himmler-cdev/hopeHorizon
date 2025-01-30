import {Component, Input} from '@angular/core';
import { CommentCardComponent } from '../comment-card/comment-card.component';
import {CommentDto} from '../dto/comment.dto';
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
}
