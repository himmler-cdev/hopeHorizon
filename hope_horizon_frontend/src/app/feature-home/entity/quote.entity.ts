import {QuoteDto} from '../dto/quote.dto';

export class QuoteEntity {
  id?: number;
  quote?: string;
  author?: string;

  toDto(): QuoteDto {
    return {
      id: this.id,
      quote: this.quote,
      author: this.author
    };
  }

  static fromDto(dto: QuoteDto) {
    const entity = new QuoteEntity();
    entity.id = dto.id;
    entity.quote = dto.quote;
    entity.author = dto.author;

    return entity;
  }
}
