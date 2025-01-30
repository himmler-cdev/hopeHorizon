import {ForumDto} from '../dto/forum.dto';

export class ForumEntity {
  id?: number;
  name?: string;
  description?: string;

  toDto(): ForumDto {
    return {
      id: this.id,
      name: this.name,
      description: this.description,
    };
  }

  static fromDto(dto: ForumDto) {
    const entity = new ForumEntity();
    entity.id = dto.id;
    entity.name = dto.name;
    entity.description = dto.description;

    return entity;
  }
}

