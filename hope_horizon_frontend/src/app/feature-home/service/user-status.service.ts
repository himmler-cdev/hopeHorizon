import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {UserStatusDto, UserStatusesDto} from '../dto/user-status.dto';

@Injectable({
    providedIn: 'root',
})
export class UserStatusService {

    constructor(private _http: HttpClient) {
    }

    getUserStatus(fromDate: Date, toDate?: Date) {
        let fromDateStr = fromDate.toISOString().split('T')[0];
        let toDateStr = toDate ? toDate.toISOString().split('T')[0] : '';
        if (toDateStr === '') {
            return this._http.get<UserStatusesDto>(`/api/user-status?from=${fromDateStr}`);
        } else {
            return this._http.get<UserStatusesDto>(`/api/user-status?from=${fromDateStr}&to=${toDateStr}`);
        }
    }

    createUserStatus(userStatus: UserStatusDto) {
        return this._http.post<UserStatusDto>('/api/user-status/', userStatus);
    }
}
