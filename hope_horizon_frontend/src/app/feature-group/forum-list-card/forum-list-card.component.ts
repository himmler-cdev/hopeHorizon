import {Component, EventEmitter, Input, Output} from '@angular/core';
import {MatCard, MatCardContent, MatCardHeader, MatCardTitle} from "@angular/material/card";
import {MatIcon} from "@angular/material/icon";
import {MatIconButton} from "@angular/material/button";
import {ForumEntity} from '../entity/forum.entity';
import {Router} from '@angular/router';
import {ForumUserEntity} from '../entity/fourm-user.entity';
import {ForumUserService} from '../service/forum-user.service';
import {MatDialog} from '@angular/material/dialog';
import {ConfirmDialogComponent} from '../../../shared/dialogs/confirm-dialog/confirm-dialog.component';

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
  @Input({required: true}) forumUser!: ForumUserEntity;

  @Output() forumUserLeft = new EventEmitter<number>();


  constructor(private _router: Router, private _forumUserService: ForumUserService, private _dialog: MatDialog) {
  }

  openForum() {
    this._router.navigate(['/forum/', this.forum.id]);
  }

  openJournal() {
    //TODO: Himmler
    this._router.navigate(['/journal/']);
  }

  leaveForum() {
    const dialogRef = this._dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Leave Forum',
        message: 'Are you sure you want to leave this forum?',
        cancelText: 'Cancel',
        confirmText: 'Leave'
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result === 'confirm') {
        if (this.forumUser.id !== undefined) {
          this._forumUserService.deleteForumUser(this.forumUser.id).subscribe(() => {
            this.forumUserLeft.emit(this.forum.id);
          });
        }
      }
    });
  }
}
