import { Component } from '@angular/core';
import { MatToolbar } from '@angular/material/toolbar';
import { MatIcon } from '@angular/material/icon';
import { MatAnchor, MatButton, MatIconButton } from '@angular/material/button';
import { NgOptimizedImage } from '@angular/common';
import { RouterLink } from '@angular/router';
import { MatMenu, MatMenuModule } from '@angular/material/menu';
import { UserService } from '../../feature-user/user.service';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../../../shared/dialogs/confirm-dialog/confirm-dialog.component';
import { TrackerDialogComponent } from '../../feature-settings/tracker-dialog/tracker-dialog.component';
import { TrackerService } from '../../feature-settings/tracker-service';
import { UserDialogComponent } from '../../feature-settings/user-dialog/user-dialog.component';
import { UserDto } from '../../feature-user/dto/user.dto';
import { UserEntity } from '../../feature-user/entity/user.entity';
import { TrackerEntity } from '../../feature-settings/entity/tracker.entity';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    MatToolbar,
    MatIcon,
    MatIconButton,
    NgOptimizedImage,
    MatButton,
    MatAnchor,
    RouterLink,
    MatAnchor,
    MatMenu,
    MatMenuModule
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {

  constructor(
    private userService: UserService,
    private trackerService: TrackerService,
    private _dialog: MatDialog,
  ) { }

  protected openLogoutDialog() {
    const dialogRef = this._dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Logout Confirmation',
        message: 'Are you sure you want to logout?',
        confirmText: 'Logout',
        cancelText: 'Cancel'
      }
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.userService.logout();
      }
    });
  }

  protected openTrackerDialog() {
    this.trackerService.getUserTracker().subscribe({
      next: (tracker) => {
        const dialogRef = this._dialog.open(TrackerDialogComponent, {
          data: TrackerEntity.fromDto(tracker),
        });
        dialogRef.afterClosed().subscribe((result: TrackerEntity) => {
          if (result) {
            this.trackerService.updateUserTracker(result.toDto()).subscribe({});
          }
        });
      },
    });
  }

  protected openUserDialog() {
    const dialogRef = this._dialog.open(UserDialogComponent, {
      data: {
        user: this.userService.getUserDataImmediate(),
        deactivate: false,
      },
    });
    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        if (result.deactivate) {
          this.userService.delete(result.user).subscribe({});
          this.userService.logout();
        } else {
          this.userService.update(result.user).subscribe({
            next: (response: UserDto) => {
              this.userService.loggedInUser = UserEntity.fromDto(response);
              localStorage.setItem('user', JSON.stringify(response));
            }
          });
        }
      }
    });
  }
}
