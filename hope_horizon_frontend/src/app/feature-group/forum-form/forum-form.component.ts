import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import {
  AbstractControl,
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  ValidatorFn,
  Validators,
} from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { MatError, MatFormField, MatLabel } from '@angular/material/form-field';
import { MatInput } from '@angular/material/input';
import { MatOption, MatSelect } from '@angular/material/select';
import { MatButton, MatIconButton } from '@angular/material/button';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../../../shared/dialogs/confirm-dialog/confirm-dialog.component';
import { ForumService } from '../service/forum.service';
import { ForumEntity } from '../entity/forum.entity';
import { MatIcon } from '@angular/material/icon';
import { ForumUserEntity } from '../entity/fourm-user.entity';
import { ForumUserService } from '../service/forum-user.service';
import { MockData } from '../service/mockdata';
import { ForumUserDto, ForumUserPostDto } from '../dto/forum-user.dto';
import { ForumUserChipComponent } from '../forum-user-chip/forum-user-chip.component';
import { UserService } from '../../feature-user/user.service';
import { UserEntity } from '../../feature-user/entity/user.entity';

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
    ForumUserChipComponent,
  ],
  templateUrl: './forum-form.component.html',
  styleUrl: './forum-form.component.scss',
})
export class ForumFormComponent implements OnInit {
  forumFormGroup: FormGroup;
  forumId: number | undefined;
  searchControl = new FormControl('');
  forumUserNames: string[] = [];
  updatedForumUsers: ForumUserEntity[] = [];
  allUserNames: string[] = [];
  allUsers: UserEntity[] = [];
  oldForumUsers: ForumUserEntity[] = [];
  updatedUsers: ForumUserEntity[] = [];
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
    //this.forumId = 1;
    this._route.paramMap.subscribe((params) => {
      this.forumId = Number(params.get('id'));
    });
    if (this.forumId) {
      this.loadForumUsers(this.forumId);
      this.loadAllUsers();
      this.cdr.detectChanges(); // Ensure change detection runs
      //this.updatedUsers = this.forumUserNames;
      this._forumService.getForum(this.forumId).subscribe((response) => {
        this.forumFormGroup.patchValue({
          id: response.id,
          name: response.name,
          description: response.description,
        });
      });
    }
  }

  /*
  onUsersUpdated(updatedUsers: ForumUserEntity[]): void {
    this.updatedUsers = updatedUsers;
  }
  */

  loadForumUsers(forumId: number) {
    this._forumUserService.getForumUsers(forumId).subscribe((users) => {
      users.forum_users.map((user) => {
        if (user.username) {
          this.forumUserNames.push(user.username);
          this.oldForumUsers.push(ForumUserEntity.fromDto(user));
        }
      });
      console.log('Loaded Forum User Names:', this.forumUserNames);
    });
  }

  loadAllUsers() {
    this._userService.getAllUsers().subscribe(
      (users) => {
        if (users && users.length > 0) {
          this.allUsers = users.map((user) => UserEntity.fromDto(user));
          this.allUserNames = users
            .map((user) => user.username)
            .filter((username): username is string => !!username);
        } else {
          this.allUserNames = [];
        }
        console.log('Loaded All User Names:', this.allUserNames);
      },
      (error) => {
        console.error('Error loading users:', error);
      }
    );
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
      this._forumService.updateForum(forumEntity.toDto()).subscribe((forum) => {

        if (!forum.id) {
          console.error('Forum ID is undefined. Skipping user assignment.');
          return;
        }
      
        console.log('Forum updated successfully with ID:', forum.id);
        // ✅ Extract usernames from `ForumUserEntity[]`
        const oldForumUserNames = this.oldForumUsers.map(
          (forumUser) => forumUser.username
        );

        const updatedForumUserNames = this.updatedUsers.map(
          (forumUser) => forumUser.username
        );

        const userIds = [
          ...new Set(this.newForumUsers.map((user) => user.id)),
        ];

        const newForumUserDTO = new ForumUserPostDto(this.forumId, userIds.filter((id): id is number => id !== undefined));

        // ✅ Extract usernames from `UserEntity[]` (New users to be added)
        const newForumUserNames = [
          ...new Set(this.newForumUsers.map((user) => user.username)),
        ];

        const usersToDelete = this.oldForumUsers.filter(
          (forumUser) =>
            this.updatedUsers.some((updatedUser) => updatedUser.user_id === forumUser.user_id)
        );
        console.log('Old Users:', this.oldForumUsers);
        console.log('Users to Add:', newForumUserNames);
        console.log('Users to Delete:', usersToDelete);

        // ✅ Send API request to create new forum users

        if ((newForumUserDTO.users ?? []).length > 0) {
          this._forumUserService.createForumUsers(newForumUserDTO).subscribe({
            next: () => console.log('New forum users added successfully'),
            error: (err) => console.error('Error adding forum users:', err),
          });
        } else {
          console.log('No new users to add, skipping API call.');
        }

        // ✅ Handle user deletions (Optional API call)
        if (usersToDelete.length > 0) {
          this._forumUserService
            .deleteForumUsers(
              usersToDelete
                .map((user) => user.id)
                .filter((id): id is number => id !== undefined)
            )
            .subscribe({
              next: () => console.log('All users deleted successfully'),
              error: (err) => console.error('Error deleting users:', err),
            });
        }

        // ✅ Navigate back to the updated forum page
        this._router.navigate(['/forum/', forum.id]);
      });
    } else {
      this._forumService.createForum(forumEntity.toDto()).subscribe((forum) => {
        // ✅ Ensure new users are unique
        const userIds = [
          ...new Set(this.newForumUsers.map((user) => user.id)),
        ];

        const newForumUserDTO = new ForumUserPostDto(this.forumId, userIds.filter((id): id is number => id !== undefined));

        // ✅ Extract usernames from `UserEntity[]` (New users to be added)
        const newForumUserNames = [
          ...new Set(this.newForumUsers.map((user) => user.username)),
        ];

        
        if ((newForumUserDTO.users ?? []).length > 0) {
          this._forumUserService.createForumUsers(newForumUserDTO).subscribe({
            next: () => console.log('New forum users added successfully'),
            error: (err) => console.error('Error adding forum users:', err),
          });
        } else {
          console.log('No new users to add, skipping API call.');
        }

        // ✅ Reset form and navigate
        this.forumFormGroup.reset();
        this._router.navigate(['/forum/']);
      });
    }
  }

  onForumUsersChange(updatedForumUsers: (UserEntity | ForumUserEntity)[]) {
    // ✅ Separate new users (UserEntity) from existing forum users (ForumUserEntity)
    this.newForumUsers = updatedForumUsers.filter(
      (user): user is UserEntity => !('forum_id' in user) // ✅ UserEntity doesn't have `forum_id`
    );
  
    this.updatedForumUsers = updatedForumUsers.filter(
      (user): user is ForumUserEntity => 'forum_id' in user // ✅ ForumUserEntity has `forum_id`
    );
  
    console.log('New Users:', this.newForumUsers);
    console.log('Existing Forum Users:', this.updatedForumUsers);
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
        title: 'Cancel Cahnges made to Forum',
        message: 'Are you sure you want to go back?',
        confirmText: 'Cancel',
        cancelText: 'Stay',
      },
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this._router.navigate(['/forum']);
      }
    });
  }

  private _clearForm() {
    // TODO: Discuss clear strategy with team
    this.forumFormGroup.reset();
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
      return isValid ? null : { whitespace: true };
    };
  }
}
