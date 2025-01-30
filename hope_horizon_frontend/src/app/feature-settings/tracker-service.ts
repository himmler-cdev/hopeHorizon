import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {TrackerDto} from './dto/tracker.dto';

@Injectable({
  providedIn: 'root',
})
export class TrackerService {

  constructor(private _http: HttpClient) {
  }

  getUserTracker() {
    return this._http.get<TrackerDto>(`/api/user-tracker/`);
  }

  updateUserTracker(tracker: TrackerDto) {
    return this._http.put<TrackerDto>(`/api/user-tracker/${tracker.id}/`, tracker);
  }
}
