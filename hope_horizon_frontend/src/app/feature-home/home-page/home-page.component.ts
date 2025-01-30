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
import {
  NotificationSectionComponent
} from "../../feature-notification/notification-section/notification-section.component";
import {MatFormField, MatFormFieldModule, MatHint, MatLabel} from '@angular/material/form-field';
import {
  MatDatepicker,
  MatDatepickerInput,
  MatDatepickerModule,
  MatDatepickerToggle,
  MatDateRangeInput,
  MatDateRangePicker
} from '@angular/material/datepicker';
import {
  AbstractControl,
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  ValidationErrors,
  ValidatorFn
} from '@angular/forms';
import {provideNativeDateAdapter} from '@angular/material/core';
import {JsonPipe} from '@angular/common';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [
    MatDivider,
    MatButton,
    RouterLink,
    NotificationSectionComponent,
    NgxChartsModule,
    MatFormField,
    MatDateRangeInput,
    ReactiveFormsModule,
    MatDatepickerToggle,
    MatDateRangePicker,
    MatLabel,
    MatHint,
    MatDatepicker,
    MatDatepickerInput,
    MatFormFieldModule,
    MatDatepickerModule,
    FormsModule,
    JsonPipe
  ],
  providers: [provideNativeDateAdapter()],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.scss'
})
export class HomePageComponent implements OnInit {
  quote?: QuoteEntity;
  userData: UserStatusEntity[] | undefined = [];
  multiLineData: any[] = [];
  isTrackerEnabled = true;
  today = new Date();

  readonly range = new FormGroup({
    start: new FormControl<Date | null>(null),
    end: new FormControl<Date | null>(null)
  });

  constructor(
    private _quoteService: QuoteService,
    private _trackerService: TrackerService,
    private _userStatusService: UserStatusService,
    private _dialog: MatDialog) {
  }

  ngOnInit() {
    const today = new Date();
    const lastWeek = new Date();
    lastWeek.setDate(today.getDate() - 7);

    this.range.setValue({
      start: lastWeek,
      end: today,
    });

    this._quoteService.getRandomQuote().subscribe((quote) => {
      this.quote = QuoteEntity.fromDto(quote);
    });

    this.openStatusDialog();

    this.range.valueChanges.subscribe((range) => {
      if (range.start && range.end) {
        this.fetchUserStatuses(range.start, range.end);
      }
    });

    this.fetchUserStatuses(lastWeek, today);
  }

  private fetchUserStatuses(fromDate: Date, toDate: Date) {
    this._userStatusService.getUserStatus(fromDate, toDate).subscribe({
      next: (userStatusesDto) => {
        this.userData = userStatusesDto?.user_statuses?.map(UserStatusEntity.fromDto);

        this._trackerService.getUserTracker().subscribe({
          next: (tracker) => {
            if (!tracker.is_enabled) {
              this.isTrackerEnabled = false;
              return;
            } else {
              this.isTrackerEnabled = true;
            }

            const availableData = [];

            if (tracker.track_mood) {
              availableData.push({
                name: 'Mood',
                series: this.userData?.map((data) => ({
                  name: data.date,
                  value: data.mood ?? 0,
                })),
              });
            }

            if (tracker.track_energy_level) {
              availableData.push({
                name: 'Energy Level',
                series: this.userData?.map((data) => ({
                  name: data.date,
                  value: data.energyLevel ?? 0,
                })),
              });
            }

            if (tracker.track_sleep_quality) {
              availableData.push({
                name: 'Sleep Quality',
                series: this.userData?.map((data) => ({
                  name: data.date,
                  value: data.sleepQuality ?? 0,
                })),
              });
            }

            if (tracker.track_anxiety_level) {
              availableData.push({
                name: 'Anxiety Level',
                series: this.userData?.map((data) => ({
                  name: data.date,
                  value: data.anxietyLevel ?? 0,
                })),
              });
            }

            if (tracker.track_appetite) {
              availableData.push({
                name: 'Appetite',
                series: this.userData?.map((data) => ({
                  name: data.date,
                  value: data.appetite ?? 0,
                })),
              });
            }

            this.multiLineData = availableData;
          },
        });
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
