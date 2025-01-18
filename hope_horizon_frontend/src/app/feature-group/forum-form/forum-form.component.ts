import { Component, Input, OnInit } from '@angular/core';
import {
  AbstractControl,
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  ValidatorFn,
  Validators,
} from '@angular/forms';
import { Router, RouterLink, ActivatedRoute } from '@angular/router';
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
import { ForumChipsUserComponent } from '../forum-chips-user/forum-chips-user.component';
import { MockData } from '../service/mockdata';

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
    ForumChipsUserComponent
  ],
  templateUrl: './forum-form.component.html',
  styleUrl: './forum-form.component.scss',
})
export class ForumFormComponent implements OnInit {
  forumFormGroup: FormGroup;
  forumId: number | undefined;
  searchControl = new FormControl('');
  forumUsers: ForumUserEntity[] = [];
  allUsers: ForumUserEntity[] = [];

  private mockData = new MockData();
  loggedInUser = this.mockData.loggedInUser;
  

  constructor(
    private _forumService: ForumService,
    private _router: Router,
    private _dialog: MatDialog,
    private _forumUserService: ForumUserService,
    private _route: ActivatedRoute
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
    })
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

  loadAllUsers() {
    this._forumUserService.getAllUsers().subscribe((users) => {
      users.forum_users.map((user) => {
        if (user.user_id === this.loggedInUser.id) {
          return; // Skip the logged in user
        }
        if (this.forumUsers.find((u) => u.id === user.user_id)) {
          return; // Skip users already in the forum
        }
        this.allUsers.push(ForumUserEntity.fromDto(user));
      });
  })};

  loadForumUsers(forumId: number) {
    this._forumUserService.getForumUsers(forumId).subscribe((users) => {
      users.forum_users.map((user) => {
        if (user.user_id === this.loggedInUser.id) {
          return; // Skip the logged in user
        }
        this.forumUsers.push(ForumUserEntity.fromDto(user));
      });
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
        this._router.navigate(['/forum/', forum.id]);
      });
    } else {
      this._forumService.createForum(forumEntity.toDto()).subscribe((forum) => {
        this.forumFormGroup.reset();
        this._router.navigate(['/forum/', forum.id]);
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
      return isValid ? null : { whitespace: true };
    };
  }
}
