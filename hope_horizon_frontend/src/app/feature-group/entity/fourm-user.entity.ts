import { ForumUserDto } from '../dto/forum-user.dto';

export class ForumUserEntity {
  id?: number;
  user_id?: number;
  username?: string;

  toDto(): ForumUserDto {
    return {
      id: this.id,
      user_id: this.user_id,
      username: this.username,
    };
  }

  static fromDto(dto: ForumUserDto) {
    const entity = new ForumUserEntity();
    entity.id = dto.id;
    entity.user_id = dto.user_id;
    entity.username = dto.username;

    return entity;
  }
}
