import {Routes} from '@angular/router';
import {BlogListComponent} from './feature-blog/blog-list/blog-list.component';
import { UserLoginComponent } from './feature-user/user-login/user-login.component';
import { UserRegisterComponent } from './feature-user/user-register/user-register.component';

export const routes: Routes = [
  {path: 'blog-list', component: BlogListComponent},
  {path: 'login', component: UserLoginComponent},
  {path: 'register', component: UserRegisterComponent},
];
