import {ChangeDetectorRef, Component, Input, OnInit} from '@angular/core';
import {CommentListComponent} from '../comment-list/comment-list.component';
import {CommentFormComponent} from '../comment-form/comment-form.component';
import {CommentService} from '../service/comment.service';
import {MatCard} from '@angular/material/card';
import {MatButton} from '@angular/material/button';
import {MatDivider} from '@angular/material/divider';
import {CommentEntity} from '../entity/comment.entity';

@Component({
    selector: 'app-comment-section',
    standalone: true,
    imports: [CommentListComponent, CommentFormComponent, MatCard, MatButton, MatDivider],
    templateUrl: './comment-section.component.html',
    styleUrl: './comment-section.component.scss'
})
export class CommentSectionComponent implements OnInit {
    comments: CommentEntity[] = [];
    page = 0; // Backend pagination starts at 0
    showLoadMore = false; // Determines whether the "Load More" button is visible
    totalComments!: number; // Initialize as undefined to avoid overwriting
    pageSize = 10; // Define the page size

    @Input({required: true}) blogId!: number;

    constructor(private commentService: CommentService, private cdr: ChangeDetectorRef) {
    }

    ngOnInit(): void {
        this.loadComments();
    }

    loadComments(): void {
        this.commentService.getComments({page: this.page, blog: this.blogId}) //
            .subscribe(response => {
                const newComments = response.comments.map(CommentEntity.fromDto);

                if (newComments.length > 0) {
                    // Append only new comments (avoid duplicates)
                    this.comments = [...this.comments, ...newComments.filter(comment =>
                        !this.comments.some(existingComment => existingComment.id === comment.id)
                    )];
                    this.page++; // Increment page
                }

                // Update total comments only if it's undefined (first load)
                if (this.totalComments === undefined) {
                    this.totalComments = response.pageInformation.actual_size;
                }

                this.updateShowLoadMore();
            });
    }

    onCommentAdded(comment: CommentEntity): void {
        this.comments = [comment, ...this.comments];
        this.totalComments = (this.totalComments ?? 0) + 1; // Ensure it's never undefined

        this.comments = [...this.comments]; // Reassigning forces Angular to detect changes
        this.cdr.detectChanges();

        // Check if the number of comments exceeds the page size
        if (this.comments.length > this.pageSize) {
            this.comments = this.comments.slice(0, this.pageSize); // Keep only the first pageSize comments
        }

        this.updateShowLoadMore();
    }

    onCommentDeleted(commentId: number): void {
        this.comments = this.comments.filter(comment => comment.id !== commentId);
        this.totalComments = (this.totalComments ?? 0) - 1; // Ensure it's never undefined
        this.cdr.detectChanges();
        this.updateShowLoadMore();
    }

    private updateShowLoadMore(): void {
        const previousShowLoadMore = this.showLoadMore;
        this.showLoadMore = this.comments.length < (this.totalComments ?? 0);

        if (this.showLoadMore !== previousShowLoadMore) {
            this.cdr.detectChanges(); // Force UI update if necessary
        }
    }
}
