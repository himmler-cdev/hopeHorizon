export interface ForumDto {
  id?: number;
  name?: string;
  description?: string;
}

export interface ForumsDto {
  forums: ForumDto[];
}
