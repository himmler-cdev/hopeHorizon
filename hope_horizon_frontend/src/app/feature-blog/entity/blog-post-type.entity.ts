import {BlogPostTypeDto} from '../dto/blog-post-type.dto';

export class BlogPostTypeEntity {
  id?: number;
  type?: string;

  toDto(): BlogPostTypeDto {
    return {
      id: this.id,
      type: this.type
    };
  }

  static fromDto(dto: BlogPostTypeDto) {
    const entity = new BlogPostTypeEntity();
    entity.id = dto.id;
    entity.type = dto.type;

    return entity;
  }
}
