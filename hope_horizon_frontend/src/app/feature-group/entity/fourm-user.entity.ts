import { ForumUserDto } from '../dto/forum-user.dto';

export class ForumUserEntity {
  id?: number;
  is_owner?: boolean;
  forum_id?: number;
  user_id?: number;
  username?: string;

  toDto(): ForumUserDto {
    return {
      id: this.id,
      is_owner: this.is_owner,
      forum_id: this.forum_id,
      user_id: this.user_id,
      username: this.username,
    };
  }

  static fromDto(dto: ForumUserDto) {
    const entity = new ForumUserEntity();
    entity.id = dto.id;
    entity.is_owner = dto.is_owner;
    entity.forum_id = dto.forum_id;
    entity.user_id = dto.user_id;
    entity.username = dto.username;

    return entity;
  }
}
