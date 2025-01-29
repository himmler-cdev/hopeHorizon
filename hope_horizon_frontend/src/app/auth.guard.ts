import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { UserService } from './feature-user/user.service';
import { map } from 'rxjs';

export const authGuard: CanActivateFn = (route, state) => {
  const userService = inject(UserService);
  const router = inject(Router);
  const isLoggedIn = userService.isLoggedInSignal();
  if (!isLoggedIn) {
    router.navigate(['login']);
  }
  return isLoggedIn;
};
