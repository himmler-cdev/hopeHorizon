import {Component, EventEmitter, Input, Output} from '@angular/core';
import {NotificationEntity} from '../entity/notification.entity';
import {MatList, MatListItem} from '@angular/material/list';
import {NotificationListCardComponent} from '../notification-list-card/notification-list-card.component';

@Component({
  selector: 'app-notification-list',
  standalone: true,
  imports: [MatList, MatListItem, NotificationListCardComponent],
  templateUrl: './notification-list.component.html',
  styleUrl: './notification-list.component.scss',
})
export class NotificationListComponent {

  @Input() notifications: NotificationEntity[] = [];
  @Output() notificationDeleted = new EventEmitter<NotificationEntity>();

  constructor() {
  }

  onNotificationDeleted() {
    this.notificationDeleted.emit();
  }
}
