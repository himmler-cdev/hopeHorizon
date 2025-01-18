import {Component, OnInit} from '@angular/core';
import { ForumListComponent } from '../forum-list/forum-list.component';
import { ForumEntity } from '../entity/forum.entity';
import { ForumService } from '../service/forum.service';
import { ForumUserService } from '../service/forum-user.service';
import { MockData } from '../service/mockdata';
import { ForumUserEntity } from '../entity/fourm-user.entity';


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
  forumUsersOfUser: ForumUserEntity[] = [];
  filterOptions = ['owned', 'member', 'all'];

  private mockData = new MockData(); //TODO: Mock recode after API is ready
  loggedInUser = this.mockData.loggedInUser;


  constructor(private _forumService: ForumService, private _forumUserService: ForumUserService) {
  }

  ngOnInit() {
    this.loadForums();
  }

  loadForums() {
    this._forumService.getForums().subscribe((response) => {
      this.forumList = response.forums.map((forum) => ForumEntity.fromDto(forum));
      this.loadForumUsers();
    });
  }

  loadForumUsers() {
    this.forumUsersOfUser = [];
    this.forumList.forEach((forum) => {
      this.getForumUserOfLoggedInUser(forum.id!);
    });
  }

  getForumUserOfLoggedInUser(forumId: number) {
    this._forumUserService.getForumUsers(forumId).subscribe((response) => {
      const userForumUsers = response.forum_users.filter(forumUser => forumUser.user_id === this.mockData.loggedInUser.id);
      this.forumUsersOfUser.push(...userForumUsers.map(ForumUserEntity.fromDto));
    });
  }

  handleForumUserLeft(forumId: number) {
    this.forumUsersOfUser = this.forumUsersOfUser.filter(user => user.forum_id !== forumId);
    this.loadForumUsers();
  }
}