export interface BlogPostDto {
  id?: number;
  title?: string;
  date?: string;
  content?: string;
  blog_post_type_id?: number;
}

export interface BlogPostsDto {
  blog_posts: BlogPostDto[];
}
