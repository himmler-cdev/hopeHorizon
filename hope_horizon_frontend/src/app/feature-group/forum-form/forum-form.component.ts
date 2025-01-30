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
import { ForumUserPostDto } from '../dto/forum-user.dto';
import { UserService } from '../../feature-user/user.service';
import { UserEntity } from '../../feature-user/entity/user.entity';
import { setThrowInvalidWriteToSignalError } from '@angular/core/primitives/signals';

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
  userId = -1;
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
    this.userId = this._userService.getUserId();
    this._route.paramMap.subscribe((params) => {
      this.forumId = Number(params.get('id'));
    });
    if (this.forumId) {
      this.loadForumUsers(this.forumId);
      this.loadAllUsers();
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
        if (user.username && user.id !== this.userId) {
          this.oldForumUsers.push(ForumUserEntity.fromDto(user));
        }
      });
    });
  }

  loadAllUsers() {
    this._userService.getAllUsers().subscribe(
      (users) => {
        if (users && users.length > 0) {
          this.allUsers = users
            .map((user) => UserEntity.fromDto(user))
            .filter((user) => user.id !== this.userId);

          this.oldForumUsersAsUsers = this.mapForumUsersToUserEntities(
            this.allUsers
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
    this.userSelectForm.setValue(this.oldForumUsersAsUsers);
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

        

        this._router.navigate(['/forum']);
      });
    } else {
      this._forumService.createForum(forumEntity).subscribe((response) => {
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
