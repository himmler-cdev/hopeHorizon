import {Component, OnInit} from '@angular/core';
import {ForumListComponent} from '../forum-list/forum-list.component';
import {ForumEntity} from '../entity/forum.entity';
import {ForumService} from '../service/forum.service';
import {ForumUserService} from '../service/forum-user.service';
import {ForumUserEntity} from '../entity/fourm-user.entity';
import {UserService} from '../../feature-user/user.service';
import {UserEntity} from '../../feature-user/entity/user.entity';

@Component({
    selector: 'app-forum-page',
    standalone: true,
    imports: [ForumListComponent],
    templateUrl: './forum-page.component.html',
})
export class ForumPageComponent implements OnInit {
    forumList: ForumEntity[] = [];
    forumUsersOfUser: ForumUserEntity[] = [];
    filterOptions = ['all', 'owned', 'member'];
    loggedInUser = new UserEntity();

    constructor(
        private _forumService: ForumService,
        private _forumUserService: ForumUserService,
        private _userService: UserService
    ) {
    }

    ngOnInit() {
        const userData = this._userService.getUserDataImmediate();
        if (userData) {
            this.loggedInUser = userData;
        } else {
            console.error('User data is null');
        }
        this.loadForums();
    }

    loadForums() {
        this._forumService.getForums(true).subscribe((response) => {
            response.custom_forums.forEach((forum) => {
                this.forumList.push(ForumEntity.fromDto(forum));
            });

            this.forumList.forEach((forum) => {
                this.loadForumUser(forum.id);
            });
        });

        this._forumService.getForums(false).subscribe((response) => {
            response.custom_forums.forEach((forum) => {
                if (!this.forumList.find((f) => f.id === forum.id)) {
                    this.forumList.push(ForumEntity.fromDto(forum));
                }

                this.forumList.forEach((forum) => {
                    this.loadForumUser(forum.id);
                });
            });
        });
    }

    loadForumUser(forumId: number | undefined) {
        if (!forumId) {
            return;
        }

        this._forumUserService.getForumUsers(forumId).subscribe(
            (response) => {
                // Filter users whose user_id matches this.userId
                const users = response.forum_users
                    .map(ForumUserEntity.fromDto)
                    .filter((user) => user.user_id === this.loggedInUser.id);

                // Append only the filtered users
                if (!this.forumUsersOfUser.find((formUser) => formUser.forum_id === forumId)) {
                    this.forumUsersOfUser = [...this.forumUsersOfUser, ...users];
                }
            },
            (error) => {
                console.error(
                    `Error fetching forum users for forum ${forumId}:`,
                    error
                );
            }
        );
    }

    handleForumUserLeft(forumId: number) {
        this.forumUsersOfUser = this.forumUsersOfUser.filter(
            (user) => user.forum_id !== forumId
        );
    }
}
