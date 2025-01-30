export interface CommentDto {
    id?: number;
    content: string;
    date?: string;
    blog_post_id: number;
    user_id?: number;
    username?: string;
  }

  export interface CommentsDto {
    pageInformation: {
      page: number;
      page_size: number;
      actual_size: number;
    };
    comments: CommentDto[];
  }
