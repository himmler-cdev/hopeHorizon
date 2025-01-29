export interface ForumUserDto {
  id?: number;
  is_owner?: boolean;
  forum_id?: number;
  user_id?: number;
  username?: string;
}

export interface ForumUsersDto {
  forum_users: ForumUserDto[];
}

export class UserIdDto {
  user_id: number;

  constructor(user_id: number) {
    this.user_id = user_id;
  }
}

export class ForumUserPostDto {
  forum_id?: number;
  users?: UserIdDto[];

  constructor(forum_id?: number, users?: number[]) {
    this.forum_id = forum_id;
    this.users = users ? users.map((id) => new UserIdDto(id)) : [];
  }
}
