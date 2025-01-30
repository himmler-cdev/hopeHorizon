import {ApplicationConfig, importProvidersFrom, provideZoneChangeDetection} from '@angular/core';
import { JwtModule } from '@auth0/angular-jwt';
import {provideRouter} from '@angular/router';

import {routes} from './app.routes';
import {provideHttpClient, withInterceptorsFromDi} from '@angular/common/http';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';

export function tokenGetter(request?: any) {
  // Check if the request is a POST to /api/user/
  if (request && request.method === 'POST' && request.url.includes('/api/user/')) {
    return null;
  }

  return localStorage.getItem('access_token');
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({eventCoalescing: true}),
    provideRouter(routes),
    importProvidersFrom(
      JwtModule.forRoot({
        config: {
          tokenGetter: tokenGetter,
          allowedDomains: ['localhost:4200'],
        },
      }),
    ),
    provideHttpClient(withInterceptorsFromDi()),
    provideAnimationsAsync()]
};
