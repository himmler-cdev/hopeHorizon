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


export class ForumUserPostDto {
  forum_id?: number;
  users?: number[];

  constructor(forum_id?: number, users?: number[]) {
    this.forum_id = forum_id;
    this.users = users ?? [];  // Keep users as an array of numbers
  }
}