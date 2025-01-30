import {Component, inject} from '@angular/core';
import {TrackerEntity} from '../../feature-settings/entity/tracker.entity';
import {
  MAT_DIALOG_DATA,
  MatDialogActions,
  MatDialogClose,
  MatDialogContent,
  MatDialogRef,
  MatDialogTitle
} from '@angular/material/dialog';
import {MatSliderModule} from '@angular/material/slider';
import {MatFormField, MatInput, MatLabel} from '@angular/material/input';
import {MatButton} from '@angular/material/button';
import {FormControl, FormGroup, ReactiveFormsModule} from '@angular/forms';
import {UserStatusEntity} from '../entity/user-status.entity';
import {CdkTextareaAutosize} from '@angular/cdk/text-field';

@Component({
  selector: 'app-status-dialog',
  standalone: true,
  imports: [
    MatDialogTitle,
    MatDialogContent,
    MatFormField,
    MatInput,
    MatDialogActions,
    MatButton,
    MatDialogClose,
    MatSliderModule,
    MatLabel,
    ReactiveFormsModule,
    CdkTextareaAutosize
  ],
  templateUrl: './status-dialog.component.html',
  styleUrl: './status-dialog.component.scss'
})
export class StatusDialogComponent {
  statusForm: FormGroup;

  readonly data = inject<TrackerEntity>(MAT_DIALOG_DATA);
  readonly dialogRef = inject(MatDialogRef<StatusDialogComponent>);

  constructor() {
    this.statusForm = new FormGroup({
      moodLevel: new FormControl(5, []),
      energyLevel: new FormControl(5, []),
      sleepQuality: new FormControl(5, []),
      anxietyLevel: new FormControl(5, []),
      appetite: new FormControl(5, []),
      content: new FormControl("", []),
    });
    this.statusForm.setValue({
      moodLevel: 5,
      energyLevel: 5,
      sleepQuality: 5,
      anxietyLevel: 5,
      appetite: 5,
      content: "Content",
    });
  }

  protected onCancel() {
    this.dialogRef.close();
  }

  protected onConfirm(): void {
    let userStatus: UserStatusEntity = new UserStatusEntity();
    userStatus.mood = this.statusForm.value.moodLevel;
    userStatus.energyLevel = this.statusForm.value.energyLevel;
    userStatus.sleepQuality = this.statusForm.value.sleepQuality;
    userStatus.anxietyLevel = this.statusForm.value.anxietyLevel;
    userStatus.appetite = this.statusForm.value.appetite;
    userStatus.content = this.statusForm.value.content;
    console.log(userStatus);
    this.dialogRef.close(userStatus);
  }

  formatLabel(value: number): string {
    return value.toString();
  }
}
