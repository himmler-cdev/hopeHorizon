export interface UserDto {
  id?: number;
  username?: string;
  password?: string;
  email?: string;
  birthdate?: string;
  user_role?: string;
}

export interface UsersDto {
  users: UserDto[];
}
