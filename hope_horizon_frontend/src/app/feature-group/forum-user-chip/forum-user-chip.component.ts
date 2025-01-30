import { NgClass } from '@angular/common';
import {
  AfterViewInit,
  ChangeDetectorRef,
  Component,
  computed,
  EventEmitter,
  inject,
  Input,
  model,
  OnChanges,
  OnInit,
  Output,
  signal,
  SimpleChanges,
} from '@angular/core';
import { FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButton, MatIconButton } from '@angular/material/button';
import {
  MatCard,
  MatCardContent,
  MatCardHeader,
  MatCardTitle,
} from '@angular/material/card';
import {
  MatChip,
  MatChipInputEvent,
  MatChipOption,
  MatChipsModule,
} from '@angular/material/chips';
import { MatOption } from '@angular/material/core';
import {
  MatFormField,
  MatFormFieldModule,
  MatLabel,
  MatSuffix,
} from '@angular/material/form-field';
import { MatIcon, MatIconModule } from '@angular/material/icon';
import { MatInput } from '@angular/material/input';
import { MatSelect } from '@angular/material/select';
import { RouterLink } from '@angular/router';
import {
  MatAutocompleteModule,
  MatAutocompleteSelectedEvent,
} from '@angular/material/autocomplete';
import { COMMA, ENTER } from '@angular/cdk/keycodes';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { UserEntity } from '../../feature-user/entity/user.entity';
import { ForumUserEntity } from '../entity/fourm-user.entity';
import { UserService } from '../../feature-user/user.service';

@Component({
  selector: 'app-forum-user-chip',
  standalone: true,
  imports: [
    MatChip,
    MatChipOption,
    MatIcon,
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
  templateUrl: './forum-user-chip.component.html',
  styleUrl: './forum-user-chip.component.scss',
})
export class ForumUserChipComponent implements OnInit, OnChanges {
  private cdr = inject(ChangeDetectorRef);

  @Input({ required: true }) forumUsers!: ForumUserEntity[];
  @Input({ required: true }) allUsers!: UserEntity[];
  currentUserId = -1;
  @Output() updatedForumUsers = new EventEmitter<
    (UserEntity | ForumUserEntity)[]
  >();

  searchControl = new FormControl('');
  combinedUsers: (UserEntity | ForumUserEntity)[] = [];
  readonly separatorKeysCodes: number[] = [ENTER, COMMA];
  readonly currentUser = model('');
  readonly selectedUsers = signal<UserEntity[]>([]);

  readonly filteredUsers = computed(() => {
    const currentUser = this.currentUser().toLowerCase();
    
    return currentUser
      ? this.allUsers.filter((user) => {
          const userId = user.id; //Always compare `id` from `UserEntity`
          
          return (
            user.username!.toLowerCase().includes(currentUser) &&
            userId !== this.currentUserId && // Exclude the current user
            !this.selectedUsers().some((selected) => {
              const selectedUserId = 'user_id' in selected ? selected.user_id : selected.id; //Handle ForumUserEntity
              return selectedUserId === userId;
            })
          );
        })
      : this.allUsers.filter((user) => {
          const userId = user.id;
  
          return (
            userId !== this.currentUserId &&
            !this.selectedUsers().some((selected) => {
              const selectedUserId = 'user_id' in selected ? selected.user_id : selected.id;
              return selectedUserId === userId;
            })
          );
        });
  });
  

  readonly announcer = inject(LiveAnnouncer);


  constructor(private _userService: UserService) {}

  ngOnInit() {
    this.currentUserId = this._userService.getUserId();
    console.log('Current User ID:', this.currentUserId);
    this.updateForumUsers();
  }
  

  ngOnChanges(changes: SimpleChanges) {
    if (changes['forumUsers'] && this.forumUsers) {
      this.selectedUsers.set(this.forumUsers);
      this.combinedUsers = [...this.forumUsers];
      this.updateForumUsers();
    }
    
  }

  add(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();
    const user = this.allUsers.find((user) => user.username === value);

    if (user && !this.selectedUsers().some((u) => u.id === user.id)) {
      this.selectedUsers.update((users) => [...users, user]);
      this.updateForumUsers();
    } else {
      console.warn('Invalid input or user not in the list.');
    }

    // Clear the input
    this.currentUser.set('');
    event.chipInput!.clear();
  }

  selected(event: MatAutocompleteSelectedEvent): void {
    const selectedValue = event.option.viewValue;
    const user = this.allUsers.find((user) => user.username === selectedValue);

    if (user && !this.selectedUsers().some((u) => u.id === user.id)) {
      this.selectedUsers.update((users) => [...users, user]);
      this.updateForumUsers();
    }

    // Clear the input
    console.log('Clearing input after selection');
    this.currentUser.set('');
    event.option.deselect();
  }

  remove(user: UserEntity): void {
    this.selectedUsers.update((users) => {
      return users.filter((u) => u.id !== user.id);
    });

    this.announcer.announce(`Removed ${user.username}`);
    this.updateForumUsers();
  }

  // Send updated list of forum users to parent component
  updateForumUsers() {
    this.combinedUsers = [...this.forumUsers, ...this.selectedUsers()]

    this.updatedForumUsers.emit(this.combinedUsers);
    console.log('Updated forum users:', this.combinedUsers);
    this.cdr.detectChanges();
  }
}
