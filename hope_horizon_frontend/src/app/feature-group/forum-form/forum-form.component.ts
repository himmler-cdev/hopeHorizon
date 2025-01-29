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
import {MockData} from '../service/mockdata';
import {ForumUsersDto} from '../dto/forum-user.dto';
import {ForumUserChipComponent} from '../forum-user-chip/forum-user-chip.component';

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
  updtedForumUserNames: string[] = [];
  allUserNames: string[] = [];
  oldForumUsers: ForumUserEntity[] = [];
  updatedUsers: ForumUserEntity[] = [];

  private mockData = new MockData();
  loggedInUser = this.mockData.loggedInUser;

  constructor(
    private _forumService: ForumService,
    private _router: Router,
    private _dialog: MatDialog,
    private _forumUserService: ForumUserService,
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
        if (user.user_id === this.loggedInUser.id) {
          return; // Skip the logged in user
        }
        if (user.username) {
          this.forumUserNames.push(user.username);
          this.oldForumUsers.push(ForumUserEntity.fromDto(user));
        }
      });
      console.log('Loaded Forum User Names:', this.forumUserNames);
    });
  }

  loadAllUsers() {
    //TODO: Change to user later on
    this._forumUserService.getAllUsers().subscribe((users) => {
      users.forum_users.map((user) => {
        if (user === this.loggedInUser.username) {
          return; // Skip the logged in user
        }
        if (user) {
          this.allUserNames.push(user);
        }
      });
      console.log('Loaded All User Names:', this.allUserNames);
    });
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
        // Update forum users
        const oldForumUserNames = this.oldForumUsers.map(
          (user) => user.username
        );
        const uniqueUpdatedForumUserNames = [...new Set(this.updtedForumUserNames)];
        const updatedForumUserNames = uniqueUpdatedForumUserNames.filter(
          (name) => !oldForumUserNames.includes(name)
        );

        // Find users to delete (present in old list but not in updated list)
        const usersToDelete = oldForumUserNames.filter(
          (name) => name !== undefined && !uniqueUpdatedForumUserNames.includes(name)
        );

        //create FourmUserEntity objects for each user
        //TODO: Change later on after implementing user
        this.updatedUsers = updatedForumUserNames.map((name) => {
          const user = new ForumUserEntity();
          user.username = name;
          return user;
        });

        const dtoForumUserList = this.updatedUsers.map((user) => user.toDto());
        dtoForumUserList.map((user) => {
          user.forum_id = forum.id;
          user.username = user.username;
          user.is_owner = false;
        });

        const dtoForumUsers: ForumUsersDto = {forum_users: dtoForumUserList};

        this._forumUserService.createForumUsers(dtoForumUsers).subscribe();

        this._router.navigate(['/forum/', forum.id]);
      });
    } else {
      this._forumService.createForum(forumEntity.toDto()).subscribe((forum) => {
        //create FourmUserEntity objects for each user
        const uniqueUpdatedForumUserNames = [...new Set(this.updtedForumUserNames)];

        const newForumUsers = uniqueUpdatedForumUserNames.map((name) => {
          const user = new ForumUserEntity();
          user.username = name;
          return user;
        });

        const dtoForumUserList = newForumUsers.map((user) => user.toDto());
        dtoForumUserList.map((user) => {
          user.forum_id = forum.id;
          user.username = user.username;
          user.is_owner = false;
        });

        const dtoForumUsers: ForumUsersDto = {forum_users: dtoForumUserList};
        this._forumUserService.createForumUsers(dtoForumUsers).subscribe();

        this.forumFormGroup.reset();
        this._router.navigate(['/forum/', forum.id]);
      });
    }
  }

  onForumUserNamesChange(updatedForumUserNames: string[]) {
    this.updtedForumUserNames = updatedForumUserNames;
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
        title: 'Clear Form',
        message: 'Are you sure you want to clear the form?',
        confirmText: 'Clear',
        cancelText: 'Cancel',
      },
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this._clearForm();
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
      return isValid ? null : {whitespace: true};
    };
  }
}


