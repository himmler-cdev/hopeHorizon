import {Routes} from '@angular/router';
import {BlogFeedComponent} from './feature-blog/blog-feed/blog-feed.component';
import {BlogJournalComponent} from './feature-blog/blog-journal/blog-journal.component';
import {BlogFormComponent} from './feature-blog/blog-form/blog-form.component';

export const routes: Routes = [
  {path: 'feed', component: BlogFeedComponent},
  {path: 'journal', component: BlogJournalComponent},
  {path: 'blog/create', component: BlogFormComponent},
  {path: 'blog/edit/:id', component: BlogFormComponent}
];
