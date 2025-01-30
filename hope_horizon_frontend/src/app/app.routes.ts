import {Routes} from '@angular/router';
import {BlogListComponent} from './feature-blog/blog-list/blog-list.component';
import {UserLoginComponent} from './feature-user/user-login/user-login.component';
import {UserRegisterComponent} from './feature-user/user-register/user-register.component';
import {authGuard} from './auth.guard';
import {BlogFeedComponent} from './feature-blog/blog-feed/blog-feed.component';
import {BlogJournalComponent} from './feature-blog/blog-journal/blog-journal.component';
import {BlogFormComponent} from './feature-blog/blog-form/blog-form.component';
import {BlogDetailComponent} from './feature-blog/blog-detail/blog-detail.component';
import { CommentSectionComponent } from './feature-comment/comment-section/comment-section.component';

export const routes: Routes = [
  /**
   * Blog routes
   */
  //{ path: '**', redirectTo: '/blog-list' }, // TODO: 404 page
  {path: '', redirectTo: '/blog-list', pathMatch: 'full'}, // TODO: home page
  {path: 'login', component: UserLoginComponent},
  {path: 'register', component: UserRegisterComponent},
  {path: 'blog-list', component: BlogListComponent, canActivate: [authGuard]},
  {path: 'feed', component: BlogFeedComponent, canActivate: [authGuard]},
  {path: 'journal', component: BlogJournalComponent, canActivate: [authGuard]},
  {path: 'blog/create', component: BlogFormComponent, canActivate: [authGuard]},
  {path: 'blog/edit/:id', component: BlogFormComponent, canActivate: [authGuard]},
  {path: 'blog/:id', component: BlogDetailComponent, canActivate: [authGuard]},

  /**
   * TODO: YOUR ROUTES @Kamilo, @David
   */
  {path: 'comment', component: CommentSectionComponent, canActivate: [authGuard]}
];
