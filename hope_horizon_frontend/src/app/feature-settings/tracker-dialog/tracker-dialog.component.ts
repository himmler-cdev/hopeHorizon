import { Component, inject } from '@angular/core';
import { MatButton } from '@angular/material/button';
import { MatCheckbox } from '@angular/material/checkbox';
import { MAT_DIALOG_DATA, MatDialogActions, MatDialogClose, MatDialogContent, MatDialogRef, MatDialogTitle } from '@angular/material/dialog';
import { MatFormField } from '@angular/material/form-field';
import { MatInput } from '@angular/material/input';
import { TrackerEntity } from '../entity/tracker.entity';

@Component({
  selector: 'app-tracker-dialog',
  standalone: true,
  imports: [
    MatDialogTitle,
    MatDialogContent,
    MatFormField,
    MatInput,
    MatDialogActions,
    MatButton,
    MatDialogClose,
    MatCheckbox
  ],
  templateUrl: './tracker-dialog.component.html',
  styleUrl: './tracker-dialog.component.scss'
})
export class TrackerDialogComponent {
    readonly data = inject<TrackerEntity>(MAT_DIALOG_DATA);
    readonly dialogRef = inject(MatDialogRef<TrackerDialogComponent>);

    protected onCancel() {
        this.dialogRef.close();
    }

    protected onConfirm(): void {
      this.dialogRef.close(this.data); // Return the modified data
    }
}
