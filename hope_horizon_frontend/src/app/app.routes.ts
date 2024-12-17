import {Routes} from '@angular/router';
import {BlogFeedComponent} from './feature-blog/blog-feed/blog-feed.component';
import {BlogJournalComponent} from './feature-blog/blog-journal/blog-journal.component';
import {BlogFormComponent} from './feature-blog/blog-form/blog-form.component';
import {BlogDetailComponent} from './feature-blog/blog-detail/blog-detail.component';

export const routes: Routes = [
  /**
   * Blog routes
   */
  {path: 'feed', component: BlogFeedComponent},
  {path: 'journal', component: BlogJournalComponent},
  {path: 'blog/create', component: BlogFormComponent},
  {path: 'blog/edit/:id', component: BlogFormComponent},
  {path: 'blog/:id', component: BlogDetailComponent}

  /**
   * TODO: YOUR ROUTES @Kamilo, @David
   */
];
