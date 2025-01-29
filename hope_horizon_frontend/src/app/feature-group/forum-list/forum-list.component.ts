import {Component, EventEmitter, Input, Output} from '@angular/core';
import {NgClass} from '@angular/common';
import {MatCard, MatCardContent, MatCardHeader, MatCardTitle,} from '@angular/material/card';
import {MatButton, MatIconButton} from '@angular/material/button';
import {MatIcon} from '@angular/material/icon';
import {MatFormField, MatLabel, MatSuffix,} from '@angular/material/form-field';
import {MatInput} from '@angular/material/input';
import {MatOption, MatSelect} from '@angular/material/select';
import {FormControl, ReactiveFormsModule} from '@angular/forms';
import {MatChip} from '@angular/material/chips';
import {RouterLink} from '@angular/router';
import {ForumEntity} from '../entity/forum.entity';
import {ForumListCardComponent} from '../forum-list-card/forum-list-card.component';
import {ForumUserEntity} from '../entity/fourm-user.entity';

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
  @Input({required: true}) forumList!: ForumEntity[];
  @Input() showFilter = true;
  @Input() filterOptions: Array<string> = [];
  @Input() forumUsersOfUser!: ForumUserEntity[];

  @Output() forumUserLeft = new EventEmitter<number>();

  filteredForumList: ForumEntity[] = [];
  searchControl = new FormControl('');
  filterControl = new FormControl('all');

  //TODO: Implement search functionality

  ngOnInit() {
    this.filterControl.valueChanges.subscribe(() => {
      this.updateFilteredForumList();
    });
    this.updateFilteredForumList();
  }

  clearSearchFilter() {
    this.searchControl.setValue('');
  }

  handleForumUserLeft(forumId: number) {
    this.forumUserLeft.emit(forumId);
  }

  updateFilteredForumList() {
    const filterValue = this.filterControl.value;

    switch (filterValue) {
      case 'all':
        this.filteredForumList = this.forumList;
        break;
      case 'owned':
        this.filteredForumList = this.forumList.filter((forum) =>
          this.forumUsersOfUser.some(
            (user) => user.forum_id === forum.id && user.is_owner
          )
        );
        break;
      case 'member':
        this.filteredForumList = this.forumList.filter((forum) =>
          this.forumUsersOfUser.some(
            (user) => user.forum_id === forum.id && !user.is_owner
          )
        );
        break;
      default:
        this.filteredForumList = this.forumList;
        break;
    }
  }
}
