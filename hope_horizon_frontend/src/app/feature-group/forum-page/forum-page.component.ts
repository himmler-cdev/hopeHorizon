import {Component, OnInit} from '@angular/core';
import { ForumListComponent } from '../forum-list/forum-list.component';
import { ForumEntity } from '../entity/forum.entity';
import { ForumService } from '../service/forum.service';


@Component({
  selector: 'app-forum-page',
  standalone: true,
  imports: [
    ForumListComponent
  ],
  templateUrl: './forum-page.component.html'
})
export class ForumPageComponent implements OnInit {
  forumList: ForumEntity[] = [];
  filterOptions = ['owned', 'member', 'all'];

  constructor(private _forumService: ForumService) {
  }

  ngOnInit() {
    this._forumService.getForums().subscribe((response) => {
      response.forums.map((forum) => {
        this.forumList.push(ForumEntity.fromDto(forum));
      });
    });
  }
}
