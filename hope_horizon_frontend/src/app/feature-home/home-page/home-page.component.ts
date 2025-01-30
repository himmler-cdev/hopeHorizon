import { Component, OnInit } from '@angular/core';
import { MatDivider } from '@angular/material/divider';
import { QuoteService } from '../service/quote.service';
import { QuoteEntity } from '../entity/quote.entity';
import { MatButton } from '@angular/material/button';
import { RouterLink } from '@angular/router';
import { TrackerService } from '../../feature-settings/tracker-service';
import { StatusDialogComponent } from '../status-dialog/status-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { TrackerEntity } from '../../feature-settings/entity/tracker.entity';
import { TrackerDto } from '../../feature-settings/dto/tracker.dto';
import { UserStatusService } from '../service/user-status.service';
import { NotificationSectionComponent } from "../../feature-notification/notification-section/notification-section.component";

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [
    MatDivider,
    MatButton,
    RouterLink,
    NotificationSectionComponent
],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.scss'
})
export class HomePageComponent implements OnInit {
  quote?: QuoteEntity;

  constructor(
    private quoteService: QuoteService,
    private trackerService: TrackerService,
    private userStatusService: UserStatusService,
    private _dialog: MatDialog) {
  }

  ngOnInit() {
    this.quoteService.getRandomQuote().subscribe((quote) => {
      this.quote = QuoteEntity.fromDto(quote);
    });
    this.openStatusDialog();
  }

  protected openStatusDialog() {
    this.userStatusService.getUserStatus(new Date()).subscribe({
      next: (userStatusesDto) => {
        if ((userStatusesDto.user_statuses?.length ?? 0) == 0) {
          this.trackerService.getUserTracker().subscribe({
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
                    this.userStatusService.createUserStatus(result.toDto()).subscribe({});
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
