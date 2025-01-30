import {Routes} from '@angular/router';
import {BlogListComponent} from './feature-blog/blog-list/blog-list.component';
import {UserLoginComponent} from './feature-user/user-login/user-login.component';
import {UserRegisterComponent} from './feature-user/user-register/user-register.component';
import {authGuard} from './auth.guard';
import {BlogFeedComponent} from './feature-blog/blog-feed/blog-feed.component';
import {BlogJournalComponent} from './feature-blog/blog-journal/blog-journal.component';
import {BlogFormComponent} from './feature-blog/blog-form/blog-form.component';
import {BlogDetailComponent} from './feature-blog/blog-detail/blog-detail.component';
import {NotFoundComponent} from './feature-not-found/not-found/not-found.component';
import {HomePageComponent} from './feature-home/home-page/home-page.component';
import {ForumPageComponent} from './feature-group/forum-page/forum-page.component';
import {ForumFormComponent} from './feature-group/forum-form/forum-form.component';

export const routes: Routes = [
  /**
   * User routes
   */
  {path: 'login', component: UserLoginComponent},
  {path: 'register', component: UserRegisterComponent},

  /**
   * Home route
   */
  {path: '', redirectTo: '/home', pathMatch: 'full'}, // Redirect to home
  {path: 'home', component: HomePageComponent, canActivate: [authGuard]},

  /**
   * Blog routes
   */
  {path: 'blog-list', component: BlogListComponent, canActivate: [authGuard]},
  {path: 'feed', component: BlogFeedComponent, canActivate: [authGuard]},
  {path: 'journal', component: BlogJournalComponent, canActivate: [authGuard]},
  {path: 'blog/create', component: BlogFormComponent, canActivate: [authGuard]},
  {path: 'blog/edit/:id', component: BlogFormComponent, canActivate: [authGuard]},
  {path: 'blog/:id', component: BlogDetailComponent, canActivate: [authGuard]},
  {path: 'blog/:id', component: BlogDetailComponent, canActivate: [authGuard]},

  /**
   * Forum routes
   */
  {path: 'forum', component: ForumPageComponent, canActivate: [authGuard]},
  {path: 'forum/:id', component: ForumFormComponent, canActivate: [authGuard]},
  {path: 'forum/create', component: ForumFormComponent, canActivate: [authGuard]},
  {path: 'forum/edit/:id', component: ForumFormComponent, canActivate: [authGuard]},

  /**
   * TODO: YOUR ROUTES @Kamilo, @David
   */


  /**
   * Default route - 404 Not Found - Must be the last route
   */
  {path: '**', component: NotFoundComponent}
];
