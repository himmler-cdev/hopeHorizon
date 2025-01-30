import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {QuoteDto} from '../dto/quote.dto';

@Injectable({
  providedIn: 'root',
})
export class QuoteService {

  constructor(private _http: HttpClient) {
  }

  getRandomQuote() {
    return this._http.get<QuoteDto>('/api/quote/');
  }
}
