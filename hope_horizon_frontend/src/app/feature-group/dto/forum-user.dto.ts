export interface ForumUserDto {
  id?: number;
  is_owner?: boolean;
  is_active?: boolean;
  group_id?: number;
  user_id?: number;
  username?: string;
}

export interface ForumUsersDto {
  forum_users: ForumUserDto[];
}

export interface UserIdDto {
  user_id: number;
}

export interface ForumUserPostDto {
  forum_id?: number;
  users?: UserIdDto[];
}

