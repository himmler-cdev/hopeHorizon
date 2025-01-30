import {TrackerDto} from "../dto/tracker.dto";


export class TrackerEntity {
  id?: number;
  isEnabled?: boolean;
  trackMood?: boolean;
  trackEnergyLevel?: boolean;
  trackSleepQuality?: boolean;
  trackAnxietyLevel?: boolean;
  trackAppetite?: boolean;
  trackContent?: boolean;

  toDto(): TrackerDto {
    return {
      id: this.id,
      is_enabled: this.isEnabled,
      track_mood: this.trackMood,
      track_energy_level: this.trackEnergyLevel,
      track_sleep_quality: this.trackSleepQuality,
      track_anxiety_level: this.trackAnxietyLevel,
      track_appetite: this.trackAppetite,
      track_content: this.trackContent,
    };
  }

  static fromDto(dto: TrackerDto): TrackerEntity {
    const entity = new TrackerEntity();
    entity.id = dto.id;
    entity.isEnabled = dto.is_enabled;
    entity.trackMood = dto.track_mood;
    entity.trackEnergyLevel = dto.track_energy_level;
    entity.trackSleepQuality = dto.track_sleep_quality;
    entity.trackAnxietyLevel = dto.track_anxiety_level;
    entity.trackAppetite = dto.track_appetite;
    entity.trackContent = dto.track_content;
    return entity;
  }
}
