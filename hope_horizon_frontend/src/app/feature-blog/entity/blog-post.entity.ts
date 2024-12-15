import {BlogPostDto} from '../dto/blog-post.dto';

export class BlogPostEntity {
  id?: number;
  title?: string;
  date?: Date;
  content?: string;
  blogPostTypeId?: number;

  toDto(): BlogPostDto {
    return {
      id: this.id,
      title: this.title,
      date: this.date?.toISOString(),
      content: this.content,
      blog_post_type_id: this.blogPostTypeId
    };
  }

  static fromDto(dto: BlogPostDto) {
    const entity = new BlogPostEntity();
    entity.id = dto.id;
    entity.title = dto.title;
    entity.date = dto.date ? new Date(dto.date) : undefined
    entity.content = dto.content;
    entity.blogPostTypeId = dto.blog_post_type_id;

    return entity;
  }
}
