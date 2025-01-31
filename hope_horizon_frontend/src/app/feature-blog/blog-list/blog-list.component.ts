import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {BlogPostEntity} from '../entity/blog-post.entity';
import {MatButton, MatIconButton} from '@angular/material/button';
import {MatIcon} from '@angular/material/icon';
import {BlogListCardComponent} from '../blog-list-card/blog-list-card.component';
import {MatFormField, MatLabel, MatSuffix} from '@angular/material/form-field';
import {MatInput} from '@angular/material/input';
import {MatOption, MatSelect} from '@angular/material/select';
import {FormControl, ReactiveFormsModule} from '@angular/forms';
import {BlogPostTypeEntity} from '../entity/blog-post-type.entity';
import {RouterLink} from '@angular/router';
import {BlogPostTypeService} from '../service/blog-post-type.service';
import {ForumService} from '../../feature-group/service/forum.service';
import {ForumEntity} from '../../feature-group/entity/forum.entity';

@Component({
  selector: 'app-blog-list',
  standalone: true,
  imports: [
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
    MatButton,
    RouterLink
  ],
  templateUrl: './blog-list.component.html',
  styleUrl: './blog-list.component.scss'
})
export class BlogListComponent implements OnInit {
  @Input({required: true}) blogPostList!: BlogPostEntity[];
  @Input() showFilter = true;
  @Input() filterForum: boolean = false;

  @Output() searchChange = new EventEmitter<string | null>();
  @Output() filterChange = new EventEmitter<number | null>();

  searchControl = new FormControl('');
  filterControl = new FormControl(0);
  blogPostTypes: BlogPostTypeEntity[] = [];
  forums: ForumEntity[] = [];
  forumId: number | undefined;

  constructor(private _blogPostTypeService: BlogPostTypeService, private _forumService: ForumService) {
  }

  ngOnInit() {
    this.searchControl.valueChanges.subscribe(value => {
      this.searchChange.emit(value);
    });

    this.filterControl.valueChanges.subscribe(value => {
      this.filterChange.emit(value);
    });

    this._blogPostTypeService.getBlogPostTypes().subscribe((response) => {
      response.blog_post_types.map((blogPostType) => {
        this.blogPostTypes.push(BlogPostTypeEntity.fromDto(blogPostType));
        this.forumId = this.blogPostTypes.find(type => type.type === 'Forum')?.id;

        if (this.filterForum && this.forumId) {
          this.filterControl.setValue(this.forumId);
        }
      });
    });

    this._forumService.getForums(true).subscribe((response) => {
      response.custom_forums.forEach((forum) => {
        this.forums.push(ForumEntity.fromDto(forum));
      });
    });

    this._forumService.getForums(false).subscribe((response) => {
      response.custom_forums.forEach((forum) => {
        this.forums.push(ForumEntity.fromDto(forum));
      });
    });
  }

  clearSearchFilter() {
    this.searchControl.setValue('');
  }

  getBlogPostTypeById(id: number | undefined): string {
    return this.blogPostTypes.find(type => type.id === id)?.type || '';
  }

  getForumNameByBlogPostId(id: number | undefined): string {
    return this.forums.find(forum => forum.id === id)?.name || '';
  }
}
