import {Component, inject} from '@angular/core';
import {
    MAT_DIALOG_DATA,
    MatDialogActions,
    MatDialogClose,
    MatDialogContent,
    MatDialogRef,
    MatDialogTitle
} from '@angular/material/dialog';
import {MatFormField} from '@angular/material/form-field';
import {MatInput} from '@angular/material/input';
import {MatButton} from '@angular/material/button';
import {ConfirmDialogData} from '../../interface/confirm-dialog-data.interface';

@Component({
    selector: 'app-confirm-dialog',
    standalone: true,
    imports: [
        MatDialogTitle,
        MatDialogContent,
        MatFormField,
        MatInput,
        MatDialogActions,
        MatButton,
        MatDialogClose
    ],
    templateUrl: './confirm-dialog.component.html',
    styleUrl: './confirm-dialog.component.scss'
})
export class ConfirmDialogComponent {
    readonly data = inject<ConfirmDialogData>(MAT_DIALOG_DATA);
    readonly dialogRef = inject(MatDialogRef<ConfirmDialogComponent>);

    protected onCancel() {
        this.dialogRef.close();
    }
}
