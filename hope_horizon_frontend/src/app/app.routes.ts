import { Routes } from '@angular/router';
import { BlogListComponent } from './feature-blog/blog-list/blog-list.component';
import { UserLoginComponent } from './feature-user/user-login/user-login.component';
import { UserRegisterComponent } from './feature-user/user-register/user-register.component';
import { authGuard } from './auth.guard';

export const routes: Routes = [
  //{ path: '**', redirectTo: '/blog-list' }, // TODO: 404 page
  { path: '', redirectTo: '/blog-list', pathMatch: 'full' }, // TODO: home page
  { path: 'login', component: UserLoginComponent },
  { path: 'register', component: UserRegisterComponent },
  { path: 'blog-list', component: BlogListComponent, canActivate: [authGuard] },
];
