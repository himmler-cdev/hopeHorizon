import { NgClass } from '@angular/common';
import { Component, Input } from '@angular/core';
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
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { COMMA, ENTER } from '@angular/cdk/keycodes';
import {
  ChangeDetectionStrategy,
  computed,
  inject,
  model,
  signal,
} from '@angular/core';
import { FormsModule } from '@angular/forms';
import {
  MatAutocompleteModule,
  MatAutocompleteSelectedEvent,
} from '@angular/material/autocomplete';
import { MatChipInputEvent, MatChipsModule } from '@angular/material/chips';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { map, startWith } from 'rxjs';

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
    RouterLink,
    MatFormFieldModule,
    MatChipsModule,
    MatIconModule,
    MatAutocompleteModule,
    FormsModule,
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './forum-form-user.component.html',
  styleUrl: './forum-form-user.component.scss',
})
export class ForumFormUserComponent {
  @Input({ required: true }) forumUsers!: ForumUserEntity[];
  @Input({ required: true }) allUsers!: ForumUserEntity[]; //TODO: get all users from database
  readonly separatorKeysCodes: number[] = [ENTER, COMMA];
  readonly currentUser = model('');
  readonly filteredUsers = computed(() => {
    const currentUser = this.currentUser().toLowerCase();
    const selectedUserIds = new Set(this.forumUsers.map((user) => user.id)); // Create a Set of selected user IDs
  
    return currentUser
      ? this.allUsers
          .filter(
            (user) =>
              user.username &&
              user.username.toLowerCase().includes(currentUser) &&
              !selectedUserIds.has(user.id) // Exclude users that are already selected
          )
      : this.allUsers.filter((user) => !selectedUserIds.has(user.id)); // Exclude selected users
  });

  readonly announcer = inject(LiveAnnouncer);

  constructor(private _forumUserService: ForumUserService) {}

  add(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();
  if (value) {
    const userDto = this.allUsers.find((u) => u.username === value);
    if (userDto) {
      this._forumUserService
        .createForumUsers({ forum_id: 1, users: [{ user_id: userDto.user_id! }] }) // Mocking `forum_id` for now
        .subscribe({
          next: (response) => {
            // Convert all DTOs to Entities and update the local list
            this.forumUsers = response.forum_users.map(ForumUserEntity.fromDto);
          },
          error: (err) => {
            console.error('Failed to add user:', err);
          },
        });
    }
  }

    this.currentUser.set('');
  }

  remove(user: ForumUserEntity): void {
    this._forumUserService.deleteForumUser(user.id!).subscribe({
      next: (response) => {
        // Convert all DTOs to Entities and update the local list
        this.forumUsers = response.forum_users.map(ForumUserEntity.fromDto);
        this.announcer.announce(`Removed ${user.username}`);
      },
      error: (err) => {
        console.error('Failed to remove user:', err);
      },
    });
    this.announcer.announce(`Removed ${user.username}`);
  }

  selected(event: MatAutocompleteSelectedEvent): void {
    const user = event.option.value as ForumUserEntity;
    this.forumUsers.push(user); // TODO: logic to add it to database maybe @output

    this.currentUser.set('');
    event.option.deselect();
  }

}
