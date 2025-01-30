import { Component, inject } from '@angular/core';
import { MatButton } from '@angular/material/button';
import { MatCheckbox } from '@angular/material/checkbox';
import { MAT_DIALOG_DATA, MatDialogActions, MatDialogClose, MatDialogContent, MatDialogRef, MatDialogTitle } from '@angular/material/dialog';
import { MatError, MatFormField, MatLabel } from '@angular/material/form-field';
import { MatInput } from '@angular/material/input';
import { TrackerEntity } from '../entity/tracker.entity';
import { UserEntity } from '../../feature-user/entity/user.entity';
import { UserSettingsDialog } from '../interface/user-settings-dialog.interface';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';

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
    MatCheckbox,
    MatFormField,
    MatLabel,
    ReactiveFormsModule,
    MatError
  ],
  templateUrl: './user-dialog.component.html',
  styleUrl: './user-dialog.component.scss'
})
export class UserDialogComponent {
  updateForm: FormGroup;
  readonly data = inject<UserSettingsDialog>(MAT_DIALOG_DATA);
  readonly dialogRef = inject(MatDialogRef<UserDialogComponent>);

  constructor() {
    this.updateForm = new FormGroup({
      username: new FormControl('', [Validators.required]),
      email: new FormControl('', [Validators.required, Validators.email]),
      deactivate : new FormControl('', [Validators.required]),
    });
    this.updateForm.setValue({
      username: this.data.user.username,
      email: this.data.user.email,
      deactivate: this.data.deactivate
    });
  }

  protected onCancel() {
    this.dialogRef.close();
  }

  protected onUpdate() {
    if (this.updateForm.valid) {
      const newDate: UserSettingsDialog = {
        user: this.data.user,
        deactivate: this.updateForm.value.deactivate
      };
      newDate.user.username = this.updateForm.value.username;
      newDate.user.email = this.updateForm.value.email;
      this.dialogRef.close(newDate);
    }
  }

  getErrorMessage(controlName: string): string {
    const control = this.updateForm.get(controlName);
    if (control && control.errors) {
      for (const error in control.errors) {
        if (control.errors.hasOwnProperty(error)) {
          switch (error) {
            case 'required':
              return 'This field is required';
            case 'email':
              return 'Please enter a valid email address';
            default:
              return 'Invalid field';
          }
        }
      }
    }
    return '';
  }
}
