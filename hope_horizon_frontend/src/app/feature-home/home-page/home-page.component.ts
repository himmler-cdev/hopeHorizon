import {Component, OnInit} from '@angular/core';
import {MatDivider} from '@angular/material/divider';
import {QuoteService} from '../service/quote.service';
import {QuoteEntity} from '../entity/quote.entity';
import {MatButton} from '@angular/material/button';
import {RouterLink} from '@angular/router';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [
    MatDivider,
    MatButton,
    RouterLink
  ],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.scss'
})
export class HomePageComponent implements OnInit {
  quote?: QuoteEntity;

  constructor(private quoteService: QuoteService) {
  }

  ngOnInit() {
    this.quoteService.getRandomQuote().subscribe((quote) => {
      this.quote = QuoteEntity.fromDto(quote);
    });
  }
}
