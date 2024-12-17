import {BlogPostTypeDto} from './blog-post-type.dto';

export interface BlogPostDto {
  id?: number;
  title?: string;
  date?: string;
  content?: string;
  blog_post_type_id?: number;
  user_id?: number;
  forum_id?: number;
}

export interface BlogPostsDto {
  blog_posts: BlogPostDto[];
  page_information: {
    page: number;
    page_size: number;
    total_size: number;
  }
}

export interface BlogPostsDto {
  blog_posts: BlogPostDto[];
}
