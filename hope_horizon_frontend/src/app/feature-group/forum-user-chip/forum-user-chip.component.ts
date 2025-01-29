import {NgClass} from '@angular/common';
import {Component, computed, EventEmitter, inject, Input, model, Output, signal,} from '@angular/core';
import {FormControl, FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatButton, MatIconButton} from '@angular/material/button';
import {MatCard, MatCardContent, MatCardHeader, MatCardTitle,} from '@angular/material/card';
import {MatChip, MatChipInputEvent, MatChipOption, MatChipsModule,} from '@angular/material/chips';
import {MatOption} from '@angular/material/core';
import {MatFormField, MatFormFieldModule, MatLabel, MatSuffix,} from '@angular/material/form-field';
import {MatIcon, MatIconModule} from '@angular/material/icon';
import {MatInput} from '@angular/material/input';
import {MatSelect} from '@angular/material/select';
import {RouterLink} from '@angular/router';
import {MatAutocompleteModule, MatAutocompleteSelectedEvent,} from '@angular/material/autocomplete';
import {COMMA, ENTER} from '@angular/cdk/keycodes';
import {LiveAnnouncer} from '@angular/cdk/a11y';

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
export class ForumUserChipComponent {
  @Input({required: true}) forumUserNames!: string[];
  @Input({required: true}) allUserNames!: string[];
  @Output() updatedForumUserNames = new EventEmitter<string[]>();

  searchControl = new FormControl('');

  // Chip variables
  readonly separatorKeysCodes: number[] = [ENTER, COMMA];
  readonly currentUser = model('');
  readonly actualUserNames = signal<string[]>([]); // Initialize as an empty array

  //readonly allUsers = this.allUserNames;
  readonly filteredUsers = computed(() => {
    const currentUser = this.currentUser().toLowerCase();
    return currentUser
      ? this.allUserNames.filter(
        (user) =>
          user.toLowerCase().includes(currentUser) &&
          !this.actualUserNames().includes(user) // Exclude already selected users
      )
      : this.allUserNames.filter(
        (user) => !this.actualUserNames().includes(user)
      ); // Exclude already selected users
  });

  readonly announcer = inject(LiveAnnouncer);

  ngOnChanges() {
    if (this.forumUserNames) {
      this.actualUserNames.set(this.forumUserNames);
    }
  }

  add(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();

    if (value && this.filteredUsers().includes(value)) {
      this.actualUserNames.update((users) => [...users, value]);
    } else {
      console.warn('Invalid input or value not in the list.');
    }

    // Clear the input
    console.log('Clearing input field');
    this.currentUser.set('');
    event.chipInput!.clear(); // Clear the input visually
  }

  selected(event: MatAutocompleteSelectedEvent): void {
    const selectedValue = event.option.viewValue;

    if (!this.actualUserNames().includes(selectedValue)) {
      this.actualUserNames.update((actualUserNames) => [
        ...actualUserNames,
        selectedValue,
      ]);
    }

    // Clear the input
    console.log('Clearing input after selection');
    this.currentUser.set('');
    event.option.deselect();
  }

  remove(user: string): void {
    this.actualUserNames.update((users) => {
      const index = users.indexOf(user);
      if (index < 0) {
        return users;
      }

      users.splice(index, 1);
      this.announcer.announce(`Removed ${user}`);
      return [...users];
    });
  }

  // send updated list of forum user names to parent component
  updateNames() {
    this.updatedForumUserNames.emit(this.actualUserNames());
  }

  clearSearchFilter() {
    this.searchControl.setValue('');
  }
}
