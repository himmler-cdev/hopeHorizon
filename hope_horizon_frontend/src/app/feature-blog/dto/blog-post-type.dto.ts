export interface BlogPostTypeDto {
  id?: number;
  type?: string;
}

export interface BlogPostTypesDto {
  blog_post_types: BlogPostTypeDto[];
}
