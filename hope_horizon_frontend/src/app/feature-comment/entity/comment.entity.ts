import {CommentDto} from '../dto/comment.dto';

export class CommentEntity {
  id?: number;
  content: string;
  date?: Date;
  blogPostId: number;
  userId?: number;
  username?: string;

  constructor(dto: CommentDto) {
    this.id = dto.id;
    this.content = dto.content;
    this.date = dto.date ? new Date(dto.date) : undefined;
    this.blogPostId = dto.blog_post_id;
    this.userId = dto.user_id;
    this.username = dto.username;
  }

  static fromDto(dto: CommentDto): CommentEntity {
    return new CommentEntity(dto);
  }

  toDto(): CommentDto {
    return {
      id: this.id,
      content: this.content,
      date: this.date?.toISOString(),
      blog_post_id: this.blogPostId,
      user_id: this.userId,
      username: this.username
    };
  }
}
