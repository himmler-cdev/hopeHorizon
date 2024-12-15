import {Injectable} from '@angular/core';
import {BlogPostDto} from './dto/blog-post.dto';
import {Observable, of} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class BlogPostService {
  mockBlogPosts: BlogPostDto[] = [
    {id: 1, title: 'Post 1', date: new Date().toISOString(), content: 'Content 1', blog_post_type_id: 1},
    {
      id: 2,
      title: 'Post 2',
      date: new Date().toISOString(),
      content: 'Flowers are among the most enchanting elements of nature, captivating humans for centuries with their beauty, fragrance, and symbolism. They are far more than just aesthetic pleasures; flowers play a crucial role in ecosystems, cultures, and human emotions. This blog explores the fascinating world of flowers, from their biological significance to their cultural impact, and their role in everyday life.\n' +
        '\n' +
        'The Biology of Flowers\n' +
        '\n' +
        'At their core, flowers are the reproductive structures of angiosperms, or flowering plants. Their primary purpose is reproduction, facilitating the union of male and female gametes to produce seeds. Each part of a flower is meticulously designed for this purpose. The petals, often brightly colored, attract pollinators such as bees, butterflies, and birds. The sepals protect the budding flower, while the stamens and carpels contain the reproductive organs.\n' +
        '\n' +
        'Pollination is a critical process in the life cycle of a flower. Some flowers rely on wind or water for pollination, while others depend on animals. This symbiotic relationship benefits both the plants, which achieve reproduction, and the pollinators, which receive nectar or pollen as a reward.\n' +
        '\n' +
        'Flowers and Ecosystems\n' +
        '\n' +
        'Flowers are essential for maintaining biodiversity and healthy ecosystems. By attracting pollinators, they ensure the reproduction of plants, which serve as food and shelter for countless organisms. The loss of pollinator species due to habitat destruction, climate change, or pesticides directly threatens the balance of ecosystems. Thus, the conservation of flowers and their habitats is vital for sustaining life on Earth.\n' +
        '\n' +
        'Symbolism and Cultural Significance\n' +
        '\n' +
        'Throughout history, flowers have carried deep symbolic meanings. In ancient Greece, the rose was associated with Aphrodite, the goddess of love, symbolizing passion and desire. In Victorian England, the "language of flowers" allowed individuals to convey complex emotions through floral arrangements. A red rose meant love, a white lily signified purity, and a yellow tulip expressed cheerful thoughts.',
      blog_post_type_id: 1
    },
    {id: 3, title: 'Post 3', date: new Date().toISOString(), content: 'Content 3', blog_post_type_id: 1},
    {id: 4, title: 'Post 4', date: new Date().toISOString(), content: 'Content 4', blog_post_type_id: 1},
    {id: 5, title: 'Post 5', date: new Date().toISOString(), content: 'Content 5', blog_post_type_id: 1},
    {id: 6, title: 'Post 6', date: new Date().toISOString(), content: 'Content 6', blog_post_type_id: 1},
    {id: 7, title: 'Post 7', date: new Date().toISOString(), content: 'Content 7', blog_post_type_id: 1},
    {id: 8, title: 'Post 8', date: new Date().toISOString(), content: 'Content 8', blog_post_type_id: 1},
    {id: 9, title: 'Post 9', date: new Date().toISOString(), content: 'Content 9', blog_post_type_id: 1},
    {id: 10, title: 'Post 10', date: new Date().toISOString(), content: 'Content 10', blog_post_type_id: 1}
  ];

  constructor() {
  }

  getBlogPosts(): Observable<Readonly<BlogPostDto[]>> {
    return of(this.mockBlogPosts);
  }

  getBlogPost(id: number): Observable<Readonly<BlogPostDto | undefined>> {
    return of(this.mockBlogPosts.find(post => post.id === id));
  }

  createBlogPost(blogPost: BlogPostDto): Observable<Readonly<BlogPostDto>> {
    this.mockBlogPosts.push(blogPost);
    return of(blogPost);
  }

  updateBlogPost(blogPost: BlogPostDto): Observable<Readonly<BlogPostDto>> {
    const index = this.mockBlogPosts.findIndex(post => post.id === blogPost.id);
    this.mockBlogPosts[index] = blogPost;
    return of(blogPost);
  }

  deleteBlogPost(id: number): Observable<void> {
    this.mockBlogPosts = this.mockBlogPosts.filter(post => post.id !== id);
    return of();
  }
}
