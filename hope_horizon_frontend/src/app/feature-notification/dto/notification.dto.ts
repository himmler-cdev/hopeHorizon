export interface NotificationDto {
    id?: number;
    is_read?: boolean;
    date?: string;
    content?: string;
    user_id?: number;
    comment_id?: number;
    forum_id?: number;
}