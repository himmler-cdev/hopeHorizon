import {Routes} from '@angular/router';
import {BlogListComponent} from './feature-blog/blog-list/blog-list.component';
import {BlogListEditComponent} from './feature-blog/blog-list-edit/blog-list-edit.component';

export const routes: Routes = [
  {path: 'blog-list', component: BlogListComponent},
  {path: 'blog-list-edit', component: BlogListEditComponent}
];
