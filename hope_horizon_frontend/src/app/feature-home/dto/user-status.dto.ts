export interface UserStatusDto {
  id?: number;
  user_id?: number;
  date?: string;
  mood?: number;
  energy_level?: number;
  sleep_quality?: number;
  anxiety_level?: number;
  appetite?: number;
  content?: string;
}

export class UserStatusesDto {
  user_statuses?: UserStatusDto[];
}
