import { Routes } from '@angular/router';
import { BlogListComponent } from './feature-blog/blog-list/blog-list.component';
import { UserLoginComponent } from './feature-user/user-login/user-login.component';
import { UserRegisterComponent } from './feature-user/user-register/user-register.component';
import { authGuard } from './auth.guard';
import {BlogListEditComponent} from './feature-blog/blog-list-edit/blog-list-edit.component';
import {BlogFeedComponent} from './feature-blog/blog-feed/blog-feed.component';
import {BlogJournalComponent} from './feature-blog/blog-journal/blog-journal.component';
import {BlogFormComponent} from './feature-blog/blog-form/blog-form.component';

export const routes: Routes = [
  //{ path: '**', redirectTo: '/blog-list' }, // TODO: 404 page
  { path: '', redirectTo: '/blog-list', pathMatch: 'full' }, // TODO: home page
  { path: 'login', component: UserLoginComponent },
  { path: 'register', component: UserRegisterComponent },
  { path: 'blog-list', component: BlogListComponent, canActivate: [authGuard] },
  {path: 'blog-list-edit', component: BlogListEditComponent},
  {path: 'feed', component: BlogFeedComponent},
  {path: 'journal', component: BlogJournalComponent},
  {path: 'blog/create', component: BlogFormComponent},
  {path: 'blog/edit/:id', component: BlogFormComponent}
];
