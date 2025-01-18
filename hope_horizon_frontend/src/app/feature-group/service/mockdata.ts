import { ForumUsersDto } from '../dto/forum-user.dto';
import { ForumsDto } from '../dto/forum.dto';

export class MockData {
  loggedInUser = { id: 1, username: 'testuser' };
  forumList: ForumsDto = {
    forums: [
      {
        id: 1,
        name: 'Forum 1',
        description: 'Description for Forum 1',
      },
      {
        id: 2,
        name: 'Forum 2',
        description: 'Description for Forum 2',
      },
      {
        id: 3,
        name: 'Forum 3',
        description: 'Description for Forum 3',
      },
    ],
  };

  forumUserList: ForumUsersDto = {
      forum_users: [
        {
          id: 1,
          is_owner: true,
          forum_id: 1,
          user_id: this.loggedInUser.id,
          username: this.loggedInUser.username,
        },
        {
          id: 2,
          is_owner: false,
          forum_id: 1,
          user_id: 2,
          username: 'fish2',
        },
        {
          id: 3,
          is_owner: true,
          forum_id: 2,
          user_id: 3,
          username: 'fish3',
        },
        {
          id: 4,
          is_owner: false,
          forum_id: 2,
          user_id: 4,
          username: 'fish4',
        },
        {
            id: 5,
            is_owner: false,
            forum_id: 3,
            user_id: this.loggedInUser.id,
            username: this.loggedInUser.username,
          }
      ],
    }

}
