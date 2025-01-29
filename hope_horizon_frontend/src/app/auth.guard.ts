import {inject} from '@angular/core';
import {CanActivateFn, Router} from '@angular/router';
import {UserService} from './feature-user/user.service';

export const authGuard: CanActivateFn = (route, state) => {
  const userService = inject(UserService);
  const router = inject(Router);
  const isLoggedIn = userService.isLoggedInSignal();
  if (!isLoggedIn) {
    router.navigate(['login']);
  }
  return isLoggedIn;
};
