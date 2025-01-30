import {HttpClient} from "@angular/common/http";
import {Injectable} from "@angular/core";
import {map, Observable} from "rxjs";
import {NotificationDto} from "../dto/notification.dto";


@Injectable({
  providedIn: 'root',
})
export class NotificationService {
  private readonly API_URL = '/api/notification/';

  constructor(private _http: HttpClient) {
  }

  getNotifications(): Observable<NotificationDto[]> {
    return this._http.get<{ notifications: NotificationDto[] }>(this.API_URL)
      .pipe(map(response => response.notifications));
  }


  deleteNotification(id: number): Observable<void> {
    return this._http.delete<void>(this.API_URL + id);
  }

}
