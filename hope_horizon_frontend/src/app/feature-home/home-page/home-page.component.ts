import {Component, OnInit} from '@angular/core';
import {MatDivider} from '@angular/material/divider';
import {QuoteService} from '../service/quote.service';
import {QuoteEntity} from '../entity/quote.entity';
import {MatButton} from '@angular/material/button';
import {RouterLink} from '@angular/router';
import {TrackerService} from '../../feature-settings/tracker-service';
import {StatusDialogComponent} from '../status-dialog/status-dialog.component';
import {MatDialog} from '@angular/material/dialog';
import {TrackerEntity} from '../../feature-settings/entity/tracker.entity';
import {UserStatusService} from '../service/user-status.service';
import {UserStatusEntity} from '../entity/user-status.entity';
import {NgxChartsModule} from '@swimlane/ngx-charts';
import { NotificationSectionComponent } from "../../feature-notification/notification-section/notification-section.component";


@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [
    MatDivider,
    MatButton,
    RouterLink,
    NotificationSectionComponent,
    NgxChartsModule
],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.scss'
})
export class HomePageComponent implements OnInit {
  quote?: QuoteEntity;
  userData: UserStatusEntity[] | undefined = [];
  multiLineData: any[] = [];

  constructor(
    private _quoteService: QuoteService,
    private _trackerService: TrackerService,
    private _userStatusService: UserStatusService,
    private _dialog: MatDialog) {
  }

  ngOnInit() {
    this._quoteService.getRandomQuote().subscribe((quote) => {
      this.quote = QuoteEntity.fromDto(quote);
    });
    this.openStatusDialog();

    this._userStatusService.getUserStatus(new Date(Date.now() - 3 * 24 * 60 * 60 * 1000)).subscribe({
      next: (userStatusesDto) => {
        this.userData = userStatusesDto?.user_statuses?.map(UserStatusEntity.fromDto);

        this._trackerService.getUserTracker().subscribe((tracker) => {
          const trackerEntity = TrackerEntity.fromDto(tracker);


        });

        this.multiLineData = [
          {
            name: 'Mood',
            series: this.userData?.map((data) => {
              return {
                name: data.date,
                value: data.mood,
              };
            }),
          },
          {
            name: 'Energy Level',
            series: this.userData?.map((data) => {
              return {
                name: data.date,
                value: data.energyLevel,
              };
            }),
          },
          {
            name: 'Sleep Quality',
            series: this.userData?.map((data) => {
              return {
                name: data.date,
                value: data.sleepQuality,
              };
            }),
          },
          {
            name: 'Anxiety Level',
            series: this.userData?.map((data) => {
              return {
                name: data.date,
                value: data.anxietyLevel,
              };
            }),
          },
          {
            name: 'Appetite',
            series: this.userData?.map((data) => {
              return {
                name: data.date,
                value: data.appetite,
              };
            }),
          },
        ];
      }
    });
  }

  protected openStatusDialog() {
    this._userStatusService.getUserStatus(new Date()).subscribe({
      next: (userStatusesDto) => {
        if ((userStatusesDto.user_statuses?.length ?? 0) == 0) {
          this._trackerService.getUserTracker().subscribe({
            next: (tracker) => {
              if (tracker.is_enabled && (
                tracker.track_mood ||
                tracker.track_energy_level ||
                tracker.track_sleep_quality ||
                tracker.track_anxiety_level ||
                tracker.track_appetite ||
                tracker.track_content
              )) {
                const dialogRef = this._dialog.open(StatusDialogComponent, {
                  data: TrackerEntity.fromDto(tracker),
                });
                dialogRef.afterClosed().subscribe((result: TrackerEntity) => {
                  if (result) {
                    this._userStatusService.createUserStatus(result.toDto()).subscribe({});
                  }
                });
              }
            },
          });
        }
      }
    });
  }
}
