import { UserStatusDto } from "../dto/user-status.dto";


export class UserStatusEntity {
  id?: number;
  user_id?: number;
  date?: Date;
  mood?: number;
  energyLevel?: number;
  sleepQuality?: number;
  anxietyLevel?: number;
  appetite?: number;
  content?: string;

  toDto(): UserStatusDto {
    return {
      id: this.id,
      user_id: this.user_id,
      date: this.date ? this.date.toISOString().split('T')[0] : undefined,
      mood: this.mood,
      energy_level: this.energyLevel,
      sleep_quality: this.sleepQuality,
      anxiety_level: this.anxietyLevel,
      appetite: this.appetite,
      content: this.content,
    };
  }

  static fromDto(dto: UserStatusDto) {
    const entity = new UserStatusEntity();
    entity.id = dto.id;
    entity.user_id = dto.user_id;
    entity.date = dto.date ? new Date(dto.date) : undefined;
    entity.mood = dto.mood;
    entity.energyLevel = dto.energy_level;
    entity.sleepQuality = dto.sleep_quality;
    entity.anxietyLevel = dto.anxiety_level;
    entity.appetite = dto.appetite;
    entity.content = dto.content;
    return entity;
  }
}
