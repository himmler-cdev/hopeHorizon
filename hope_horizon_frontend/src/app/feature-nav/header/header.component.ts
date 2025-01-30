import {Component} from '@angular/core';
import {MatToolbar} from '@angular/material/toolbar';
import {MatIcon} from '@angular/material/icon';
import {MatAnchor, MatButton, MatIconButton} from '@angular/material/button';
import {NgOptimizedImage} from '@angular/common';
import {RouterLink} from '@angular/router';
import {MatMenu, MatMenuModule} from '@angular/material/menu';
import {UserService} from '../../feature-user/user.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    MatToolbar,
    MatIcon,
    MatIconButton,
    NgOptimizedImage,
    MatButton,
    MatAnchor,
    RouterLink,
    MatAnchor,
    MatMenu,
    MatMenuModule
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {

  constructor(private userService: UserService) {
  }

  onLogout() {
    this.userService.logout();
  }
}
