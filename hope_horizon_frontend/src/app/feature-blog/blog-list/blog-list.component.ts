import {Component, EventEmitter, Input, Output} from '@angular/core';
import {BlogPostEntity} from '../entity/blog-post.entity';
import {DatePipe, NgClass} from '@angular/common';
import {MatCard, MatCardContent, MatCardHeader, MatCardTitle} from '@angular/material/card';
import {MatButton, MatIconButton} from '@angular/material/button';
import {MatIcon} from '@angular/material/icon';
import {BlogListCardComponent} from '../blog-list-card/blog-list-card.component';
import {MatFormField, MatLabel, MatSuffix} from '@angular/material/form-field';
import {MatInput} from '@angular/material/input';
import {MatOption, MatSelect} from '@angular/material/select';
import {FormControl, ReactiveFormsModule} from '@angular/forms';
import {MatChip} from '@angular/material/chips';
import {BlogPostTypeEntity} from '../entity/blog-post-type.entity';
import {RouterLink} from '@angular/router';

@Component({
  selector: 'app-blog-list',
  standalone: true,
  imports: [
    DatePipe,
    MatCard,
    MatCardTitle,
    MatCardHeader,
    MatCardContent,
    MatIconButton,
    MatIcon,
    BlogListCardComponent,
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
  templateUrl: './blog-list.component.html',
  styleUrl: './blog-list.component.scss'
})
export class BlogListComponent {
  @Input({required: true}) blogPostList!: BlogPostEntity[];
  @Input() showFilter = true;
  @Input() filterOptions: BlogPostTypeEntity[] = [];

  @Output() searchChange = new EventEmitter<string | null>();
  @Output() filterChange = new EventEmitter<number | null>();

  searchControl = new FormControl('');
  filterControl = new FormControl(null);

  constructor() {
    this.searchControl.valueChanges.subscribe(value => {
      this.searchChange.emit(value);
    });

    this.filterControl.valueChanges.subscribe(value => {
      this.filterChange.emit(value);
    });
  }

  clearSearchFilter() {
    this.searchControl.setValue('');
  }
}
