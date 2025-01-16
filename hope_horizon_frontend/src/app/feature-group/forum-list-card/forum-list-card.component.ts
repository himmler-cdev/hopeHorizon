import {Component, Input} from '@angular/core';
import {MatCard, MatCardContent, MatCardHeader, MatCardTitle} from "@angular/material/card";
import {MatIcon} from "@angular/material/icon";
import {MatIconButton} from "@angular/material/button";
import {ForumEntity} from '../entity/forum.entity';
import {Router, RouterLink} from '@angular/router';

@Component({
  selector: 'app-forum-list-card',
  standalone: true,
  imports: [
    MatCard,
    MatCardContent,
    MatCardHeader,
    MatCardTitle,
    MatIcon,
    MatIconButton
  ],
  templateUrl: './forum-list-card.component.html',
  styleUrl: './forum-list-card.component.scss'
})
export class ForumListCardComponent {
  @Input({required: true}) forum!: ForumEntity;

  constructor(private _router: Router,) {}

  openForum() {
    this._router.navigate(['/forum/', this.forum.id]);
  }
}
