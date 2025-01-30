import {NotificationDto} from '../dto/notification.dto';

export class NotificationEntity {
  id?: number;
  is_read?: boolean;
  date?: Date;
  content?: string;
  userId?: number;
  commentId?: number;
  forumId?: number;


  constructor(dto: NotificationDto) {
    this.id = dto.id;
    this.is_read = dto.is_read;
    this.date = dto.date ? new Date(dto.date) : undefined;
    this.content = dto.content;
    this.userId = dto.user_id;
    this.commentId = dto.comment_id;
    this.forumId = dto.forum_id;
  }

  static fromDto(dto: NotificationDto): NotificationEntity {
    return new NotificationEntity(dto);
  }

  toDto(): NotificationDto {
    return {
      id: this.id,
      is_read: this.is_read,
      date: this.date?.toISOString(),
      content: this.content,
      user_id: this.userId,
      comment_id: this.commentId,
      forum_id: this.forumId
    };
  }
}
