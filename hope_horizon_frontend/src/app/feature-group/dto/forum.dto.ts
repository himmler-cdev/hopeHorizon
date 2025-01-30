export interface ForumDto {
  id?: number;
  name?: string;
  description?: string;
}

export interface ForumsDto {
  custom_forums: ForumDto[];
}
