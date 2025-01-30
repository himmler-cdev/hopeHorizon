import { TrackerDto } from "../dto/tracker.dto";


export class TrackerEntity {
    id?: number;
    is_enabled?: boolean;
    track_mood?: boolean;
    track_energy_level?: boolean;
    track_sleep_quality?: boolean;
    track_anxiety_level?: boolean;
    track_appetite?: boolean;
    track_content?: boolean;

    toDto(): TrackerDto {
        return {
            id: this.id,
            is_enabled: this.is_enabled,
            track_mood: this.track_mood,
            track_energy_level: this.track_energy_level,
            track_sleep_quality: this.track_sleep_quality,
            track_anxiety_level: this.track_anxiety_level,
            track_appetite: this.track_appetite,
            track_content: this.track_content,
        };
    }

    fromDto(dto: TrackerDto): TrackerEntity {
        const entity = new TrackerEntity();
        entity.id = dto.id;
        entity.is_enabled = dto.is_enabled;
        entity.track_mood = dto.track_mood;
        entity.track_energy_level = dto.track_energy_level;
        entity.track_sleep_quality = dto.track_sleep_quality;
        entity.track_anxiety_level = dto.track_anxiety_level;
        entity.track_appetite = dto.track_appetite;
        entity.track_content = dto.track_content;
        return entity;
    }
}