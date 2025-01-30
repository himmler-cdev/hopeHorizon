import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { NotificationEntity } from '../entity/notification.entity';
import { MatCard, MatCardContent } from '@angular/material/card';
import { NotificationService } from '../service/notification.service';
import { ForumUserService } from '../../feature-group/service/forum-user.service';
import { UserService } from '../../feature-user/user.service';
import { UserEntity } from '../../feature-user/entity/user.entity';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../../../shared/dialogs/confirm-dialog/confirm-dialog.component';
import { ForumUserEntity } from '../../feature-group/entity/fourm-user.entity';
import { map } from 'rxjs';
import { ForumUsersDto } from '../../feature-group/dto/forum-user.dto';
import { MatButton } from '@angular/material/button';

@Component({
  selector: 'app-notification-list-card',
  standalone: true,
  imports: [MatCard, MatCardContent, MatButton],
  templateUrl: './notification-list-card.component.html',
  styleUrl: './notification-list-card.component.scss',
})
export class NotificationListCardComponent implements OnInit {
  @Input() notification: NotificationEntity | undefined;
  @Output() notificationDeleted = new EventEmitter<number>();
  
  forumId: number | null = null;
  content = '';
  loggedInUser: UserEntity | null = null;
  forumUser: ForumUserEntity | null = null;

  constructor(
    private _notificationService: NotificationService,
    private _forumUserService: ForumUserService,
    private _userService: UserService,
    private _dialog: MatDialog
  ) {}

  ngOnInit() {
    this.loggedInUser = this._userService.getUserDataImmediate();
    this.forumId = this.notification?.forumId || null;
    this.content = this.notification?.content || '';
    this.getForumUser();
  }

  deleteNotification() {
    //console.log('Delete button clicked:', this.notification?.id); // Debug log
    if (this.notification?.id) {
      this._notificationService.deleteNotification(this.notification.id).subscribe(
        () => {
          console.log('Notification deleted successfully');
          this.notificationDeleted.emit();
        },
        (error) => console.error('Error deleting notification:', error)
      );
    }
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
         if (this.forumUser && this.forumUser.id !== undefined && this.notification?.id) {
           this._forumUserService.deleteForumUser(this.forumUser.id).subscribe(() => {  });
            console.log('Forum user deleted successfully');
            this.deleteNotification();
         }
       }
     });
   }

   getForumUser() {
    console.log('Get Forum User button clicked'); // Debug log
  
    if (this.loggedInUser && this.notification?.id && this.forumId) {
      this._forumUserService.getForumUsers(this.forumId).pipe(
        map((response: ForumUsersDto) => 
          response.forum_users.filter((user) => user.user_id === this.loggedInUser?.id)
        )
      ).subscribe(
        (filteredUsers) => {
          if (filteredUsers.length > 0) {
            this.forumUser = ForumUserEntity.fromDto(filteredUsers[0]); // Take first matching user
            console.log('Forum user:', this.forumUser);
          } else {
            console.warn('No matching forum user found');
          }
        },
        (error) => console.error('Error getting forum user:', error)
      );
    }
  }
  
}  