import { Component, OnInit } from '@angular/core';
import { ForumListComponent } from '../forum-list/forum-list.component';
import { ForumEntity } from '../entity/forum.entity';
import { ForumService } from '../service/forum.service';
import { ForumUserService } from '../service/forum-user.service';
import { ForumUserEntity } from '../entity/fourm-user.entity';
import { UserService } from '../../feature-user/user.service';

@Component({
  selector: 'app-forum-page',
  standalone: true,
  imports: [ForumListComponent],
  templateUrl: './forum-page.component.html',
})
export class ForumPageComponent implements OnInit {
  forumList: ForumEntity[] = [];
  forumUsersOfUser: ForumUserEntity[] = [];
  filterOptions = ['owned', 'member', 'all'];
  userId = -1;
  
  

  constructor(
    private _forumService: ForumService,
    private _forumUserService: ForumUserService,
    private _userSerivce: UserService
  ) {}

  ngOnInit() {
    this.userId = this._userSerivce.getUserId();
    this.loadForums();
    console.log('UserID:', this.userId);

  }

  loadForums() {
    
    this._forumService.getForums(true).subscribe((response) => {
      this.forumList = response.custom_forums.map((forum) =>
        ForumEntity.fromDto(forum)
      );

      // Load forum users for each forum
      this.forumList.forEach((forum) => {
        this.loadForumUser(forum.id!);
      });
    });
    //console.log('Forums:', this.forumList);

    this._forumService.getForums(false).subscribe((response) => {
      const additionalForums = response.custom_forums.map((forum) =>
        ForumEntity.fromDto(forum)
      );

      //console.log('Additional Forums:', additionalForums);

      // Append these forums to the existing list
      this.forumList = [...this.forumList, ...additionalForums];

      // Load forum users for each additional forum
      additionalForums.forEach((forum) => {
        this.loadForumUser(forum.id!);
      });

      //console.log('Final Forum List:', this.forumList);
    });
  }

  loadForumUser(forumId: number) {
    this._forumUserService.getForumUsers(forumId).subscribe(
      (response) => {
        // Filter users whose user_id matches this.userId
        const users = response.forum_users
          .map(ForumUserEntity.fromDto)
          .filter(user => user.user_id === this.userId);
  
        // Append only the filtered users
        this.forumUsersOfUser = [...this.forumUsersOfUser, ...users];
  
        //console.log(`Filtered Forum Users for forum ${forumId}:`, users);
        //console.log('Updated Forum Users list:', this.forumUsersOfUser);
      },
      (error) => {
        console.error(`Error fetching forum users for forum ${forumId}:`, error);
      }
    );
  }
  

  handleForumUserLeft(forumId: number) {
    this.forumUsersOfUser = this.forumUsersOfUser.filter(
      (user) => user.forum_id !== forumId
    );
  }
}
