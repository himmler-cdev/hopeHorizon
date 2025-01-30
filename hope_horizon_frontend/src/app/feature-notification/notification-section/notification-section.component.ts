import {ChangeDetectorRef, Component, OnInit} from '@angular/core';
import {NotificationListComponent} from '../notification-list/notification-list.component';
import {MatCard} from '@angular/material/card';
import {NotificationService} from '../service/notification.service';
import {NotificationEntity} from '../entity/notification.entity';

@Component({
  selector: 'app-notification-section',
  standalone: true,
  imports: [NotificationListComponent, MatCard],
  templateUrl: './notification-section.component.html',
  styleUrl: './notification-section.component.scss',
})
export class NotificationSectionComponent implements OnInit {
  notifications: NotificationEntity[] = [];

  constructor(private _notificationService: NotificationService, private cdr: ChangeDetectorRef) {
  }

  ngOnInit(): void {
    this.loadNotifications();
    console.log('Notifications: ', this.notifications);
  }

  loadNotifications() {
    this._notificationService.getNotifications().subscribe((notifications) => {
      this.notifications = notifications.map(NotificationEntity.fromDto);
    });
  }

  onNotificationDeleted() {
    this.cdr.detectChanges();
    this.ngOnInit();
  }
}
