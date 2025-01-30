import {ChangeDetectorRef, Component, OnInit} from '@angular/core';
import {AbstractControl, FormControl, FormGroup, ReactiveFormsModule, ValidatorFn, Validators,} from '@angular/forms';
import {ActivatedRoute, Router, RouterLink} from '@angular/router';
import {MatError, MatFormField, MatLabel} from '@angular/material/form-field';
import {MatInput} from '@angular/material/input';
import {MatOption, MatSelect} from '@angular/material/select';
import {MatButton, MatIconButton} from '@angular/material/button';
import {MatDialog} from '@angular/material/dialog';
import {ConfirmDialogComponent} from '../../../shared/dialogs/confirm-dialog/confirm-dialog.component';
import {ForumService} from '../service/forum.service';
import {ForumEntity} from '../entity/forum.entity';
import {MatIcon} from '@angular/material/icon';
import {ForumUserEntity} from '../entity/fourm-user.entity';
import {ForumUserService} from '../service/forum-user.service';
import {UserService} from '../../feature-user/user.service';
import {UserEntity} from '../../feature-user/entity/user.entity';
import {ForumUserPostDto} from '../dto/forum-user.dto';

@Component({
  selector: 'app-forum-form',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    MatFormField,
    MatInput,
    MatIconButton,
    MatIcon,
    MatFormField,
    MatSelect,
    MatOption,
    MatLabel,
    MatButton,
    RouterLink,
    MatError,
  ],
  templateUrl: './forum-form.component.html',
  styleUrl: './forum-form.component.scss',
})
export class ForumFormComponent implements OnInit {
  userSelectForm = new FormControl();
  forumFormGroup: FormGroup;
  forumId: number | undefined;
  searchControl = new FormControl('');
  allUsers: UserEntity[] = [];
  oldForumUsers: ForumUserEntity[] = [];
  loggedInUser = new UserEntity();
  oldForumUsersAsUsers: UserEntity[] = [];
  newForumUsers: UserEntity[] = [];

  constructor(
    private _forumService: ForumService,
    private _router: Router,
    private _dialog: MatDialog,
    private _forumUserService: ForumUserService,
    private _userService: UserService,
    private _route: ActivatedRoute,
    private cdr: ChangeDetectorRef
  ) {
    this.forumFormGroup = new FormGroup({
      id: new FormControl(null),
      name: new FormControl('', [
        Validators.maxLength(250),
        Validators.required,
        this.whitespaceValidator(),
      ]),
      description: new FormControl('', [
        Validators.required,
        this.whitespaceValidator(),
      ]),
    });
  }

  ngOnInit() {
    const userData = this._userService.getUserDataImmediate();
    if (userData) {
      this.loggedInUser = userData;
    } else {
      console.error('User data is null');
    }
    this._route.paramMap.subscribe((params) => {
      this.forumId = Number(params.get('id'));
    });
    if (this.forumId) {
      this.loadForumUsers(this.forumId);

      this._forumService.getForum(this.forumId).subscribe((response) => {
        this.forumFormGroup.patchValue({
          id: response.id,
          name: response.name,
          description: response.description,
        });
      });
    }
  }

  loadForumUsers(forumId: number) {
    this._forumUserService.getForumUsers(forumId).subscribe((users) => {
      users.forum_users.map((user) => {
        if (user.username) {
          this.oldForumUsers.push(ForumUserEntity.fromDto(user));
        }
      });
      this.loadAllUsers();
    });
  }

  loadAllUsers() {
    this._userService.getAllUsers().subscribe(
      (users) => {
        if (users && users.length > 0) {
          this.allUsers = users
            .map((user) => UserEntity.fromDto(user))
            .filter((user) => user.id !== this.loggedInUser.id);

          this.oldForumUsersAsUsers = this.mapForumUsersToUserEntities(
            this.oldForumUsers
          );
          this.preselectUsers();
        }
      },
      (error) => {
        console.error('Error loading users:', error);
      }
    );
  }

  mapForumUsersToUserEntities(forumUsers: ForumUserEntity[]): UserEntity[] {
    return forumUsers
      .map((forumUser) => {
        return this.allUsers.find((user) => user.id === forumUser.user_id);
      })
      .filter((user): user is UserEntity => !!user);
  }

  preselectUsers() {
    if (this.oldForumUsersAsUsers.length > 0) {
      const selectedUserIds = this.oldForumUsersAsUsers.map((user) => user.id); // Extract IDs
      console.log('Preselecting users:', selectedUserIds);

      this.userSelectForm.setValue(selectedUserIds); // Set IDs instead of objects
    }
  }

  private persistForm(): ForumEntity {
    const formValue = this.forumFormGroup.value;
    const entity = new ForumEntity();

    entity.id = formValue.id;
    entity.name = formValue.name;
    entity.description = formValue.description;

    return entity;
  }

  clearSearchFilter() {
    this.searchControl.setValue('');
  }

  protected createOrUpdate() {
    if (this.forumFormGroup.invalid) {
      return;
    }

    const forumEntity = this.persistForm();

    if (this.forumId) {
      this._forumService.updateForum(forumEntity).subscribe(() => {
        this.userSelectForm.value.map((userId: Number) => {
          const user = this.allUsers.find((user) => user.id === userId);

          if (user && !this.oldForumUsersAsUsers.includes(user)) {
            this.newForumUsers.push(user);
          }
        });

        const userIds = [...new Set(this.newForumUsers.map((user) => user.id))];

        const newForumUserDTO = new ForumUserPostDto(
          this.forumId,
          userIds
            .filter((id): id is number => id !== undefined)
            .filter(
              (id) =>
                !this.oldForumUsersAsUsers.some((oldUser) => oldUser.id === id)
            )
        );

        if (newForumUserDTO.users && newForumUserDTO.users.length > 0) {
          this._forumUserService.createForumUsers(newForumUserDTO).subscribe({
            next: () => console.log('New forum users added successfully'),
            error: (err) => console.error('Error adding forum users:', err),
          });
        } else {
          console.log('No new users to add, skipping API call.');
        }

        const selectedUserIds = this.userSelectForm.value as number[]; // Get selected IDs

        /*
        Not implemented correctly in backend, TODO for v2
        +++++++++++++++++++++++++++++++++++++++++++++++


        const usersToDelete = this.oldForumUsersAsUsers.filter(
          (oldUser) =>
            oldUser.id !== this.loggedInUser.id && // Exclude logged-in user
            !selectedUserIds.includes(oldUser.id!) // Compare IDs, not objects
        );

        // Extract only the IDs
        const userIdsToDelete = usersToDelete
          .map((user) => user.id) // Get only IDs
          .filter((id): id is number => id !== undefined); // Ensure IDs are valid

        if (userIdsToDelete.length > 0) {
          console.log("Deleting users:", userIdsToDelete); // Debugging log

          this._forumUserService.deleteForumUsers(userIdsToDelete).subscribe({
            next: () => console.log("Users deleted successfully"),
            error: (err) => console.error("Error deleting users:", err),
          });
        }
          */

        this._router.navigate(['/forum']);
      });
    } else {
      this._forumService
        .createForum(forumEntity.toDto())
        .subscribe((response) => {
          this._router.navigate(['/forum']);
        });
    }
  }

  protected openDeleteDialog() {
    const dialogRef = this._dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Delete Forum',
        message: 'Are you sure you want to delete this forum?',
        confirmText: 'Delete',
        cancelText: 'Cancel',
      },
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this._deleteForum();
      }
    });
  }

  protected openCancelDialog() {
    const dialogRef = this._dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Cancel Changes made to Forum',
        message: 'Are you sure you want to go back?',
        confirmText: 'Go Back',
        cancelText: 'Stay',
      },
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this._router.navigate(['/forum']);
      }
    });
  }

  private _deleteForum() {
    if (!this.forumId) {
      return;
    }

    this._forumService.deleteForum(this.forumId).subscribe(() => {
      this._router.navigate(['/forum']);
    });
  }

  private whitespaceValidator(): ValidatorFn {
    return (control: AbstractControl) => {
      if (!control.value) {
        return null;
      }
      const isWhitespace = (control.value || '').trim().length === 0;
      const isValid = !isWhitespace;
      return isValid ? null : {whitespace: true};
    };
  }
}
