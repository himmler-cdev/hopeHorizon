import {Component, inject} from '@angular/core';
import {RouterOutlet} from '@angular/router';
import {MatButton} from '@angular/material/button';
import {HeaderComponent} from './feature-nav/header/header.component';
import {FooterComponent} from './feature-nav/footer/footer.component';
import {UserService} from './feature-user/user.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, MatButton, HeaderComponent, FooterComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'hope_horizon_frontend';
  userService = inject(UserService);
}
