import {
  ChangeDetectorRef,
  Component,
  EventEmitter,
  Input,
  Output,
  SimpleChanges,
} from '@angular/core';
import { NgClass } from '@angular/common';
import {
  MatCard,
  MatCardContent,
  MatCardHeader,
  MatCardTitle,
} from '@angular/material/card';
import { MatButton, MatIconButton } from '@angular/material/button';
import { MatIcon } from '@angular/material/icon';
import {
  MatFormField,
  MatLabel,
  MatSuffix,
} from '@angular/material/form-field';
import { MatInput } from '@angular/material/input';
import { MatOption, MatSelect } from '@angular/material/select';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatChip } from '@angular/material/chips';
import { RouterLink } from '@angular/router';
import { ForumEntity } from '../entity/forum.entity';
import { ForumListCardComponent } from '../forum-list-card/forum-list-card.component';
import { ForumUserEntity } from '../entity/fourm-user.entity';

@Component({
  selector: 'app-forum-list',
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
    ForumListCardComponent,
  ],
  templateUrl: './forum-list.component.html',
  styleUrl: './forum-list.component.scss',
})
export class ForumListComponent {
  @Input({ required: true }) forumList!: ForumEntity[];
  @Input() showFilter = true;
  @Input() filterOptions: Array<string> = [];
  @Input() forumUsersOfUser!: ForumUserEntity[];
  @Input() userId = -1;

  @Output() forumUserLeft = new EventEmitter<number>();

  filteredForumList: ForumEntity[] = [];
  searchControl = new FormControl('');
  filterControl = new FormControl('all');

  constructor(private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.searchControl.valueChanges.subscribe(() => {
      this.updateFilteredForumList();
    });

    this.filterControl.valueChanges.subscribe(() => {
      this.updateFilteredForumList();
    });

    this.updateFilteredForumList();

    console.log('Forum Users:', this.forumUsersOfUser);
    console.log('Forum List:', this.forumList);
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['forumList'] || changes['forumUsersOfUser']) {
      console.log('Data changed:', this.forumList, this.forumUsersOfUser);
      this.updateFilteredForumList();
      this.cdr.detectChanges(); // ✅ Ensure UI updates
    }
  }

  clearSearchFilter() {
    this.searchControl.setValue('');
  }

  handleForumUserLeft(forumId: number) {
    this.forumUserLeft.emit(forumId);
  }

  updateFilteredForumList() {
    if (!this.forumList) return; // Ensure forums are loaded

    const searchValue = this.searchControl.value?.toLowerCase() || '';
    const filterValue = this.filterControl.value;

    // Start with the full forum list
    let filteredList = [...this.forumList];

    // Apply Filter
    switch (filterValue) {
      case 'owned':
        filteredList = filteredList.filter((forum) =>
          this.forumUsersOfUser.some(
            (user) => user.forum_id === forum.id && user.is_owner
          )
        );
        break;
      case 'member':
        filteredList = filteredList.filter((forum) =>
          this.forumUsersOfUser.some(
            (user) => user.forum_id === forum.id && !user.is_owner
          )
        );
        break;
    }

    // Apply Search (by name or other attributes)
    if (searchValue) {
      filteredList = filteredList.filter(
        (forum) =>
          forum.name?.toLowerCase().includes(searchValue) || // Search in name
          forum.description?.toLowerCase().includes(searchValue) // Search in description (optional)
      );
    }

    this.filteredForumList = filteredList;
    this.cdr.detectChanges(); // ✅ Ensure UI updates
  }
}
