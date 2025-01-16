import { NgClass } from '@angular/common';
import { Component } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatIconButton, MatButton } from '@angular/material/button';
import {
  MatCard,
  MatCardContent,
  MatCardHeader,
  MatCardTitle,
} from '@angular/material/card';
import { MatChip } from '@angular/material/chips';
import { MatOption } from '@angular/material/core';
import {
  MatFormField,
  MatLabel,
  MatSuffix,
} from '@angular/material/form-field';
import { MatIcon } from '@angular/material/icon';
import { MatInput } from '@angular/material/input';
import { MatSelect } from '@angular/material/select';
import { RouterLink } from '@angular/router';
import { ForumUserEntity } from '../entity/fourm-user.entity';
import { ForumUserService } from '../service/forum-user.service';
import { ForumUserDto } from '../dto/forum-user.dto';

@Component({
  selector: 'app-forum-form-user',
  standalone: true,
  imports: [
    MatCard,
    MatCardTitle,
    MatCardHeader,
    MatCardContent,
    MatIconButton,
    MatIcon,
    MatFormField,
    MatInput,
    MatSelect,
    MatOption,
    MatLabel,
    MatSuffix,
    ReactiveFormsModule,
    MatChip,
    NgClass,
    MatButton,
    RouterLink
  ],
  templateUrl: './forum-form-user.component.html',
  styleUrl: './forum-form-user.component.scss',
})
export class ForumFormUserComponent {
  searchControl = new FormControl('');
  forumUsers: ForumUserEntity[] = [];
  selectedUsers: ForumUserEntity[] = [];

  constructor(private _forumUserService: ForumUserService) {}

  ngOnInit() {
    this.loadForumUsers();
  }

  loadForumUsers() {
    this._forumUserService.getForumUsers().subscribe((users) => {
      users.forum_users.map((user) => {
        this.forumUsers.push(ForumUserEntity.fromDto(user));
      });
    });
  }

  clearSearchFilter() {
    this.searchControl.setValue('');
  }

  selectUser(user: ForumUserEntity) {
    if (!this.selectedUsers.includes(user)) {
      this.selectedUsers.push(user);
    }
    this.clearSearchFilter();
  }

  removeUser(user: ForumUserEntity) {
    this.selectedUsers = this.selectedUsers.filter(u => u !== user);
  }

  deleteUser(user: ForumUserEntity) {
    if (user.id === undefined) {
      throw new Error('User ID is undefined. Cannot delete user.');
    }
    this._forumUserService.deleteForumUser(user.id).subscribe(() => {
      this.forumUsers = this.forumUsers.filter(u => u !== user);
    });
  }
}
