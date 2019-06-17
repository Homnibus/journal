import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {BehaviorSubject, Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {User} from '../../app.models';

class TokenData {
  token: string;
}

@Injectable()
export class AuthService {
  public currentUser$: Observable<User>;
  // API URL
  public API_URL = 'http://localhost:8000/api';
  private AUTH_URL = 'http://localhost:8000/api-auth/';
  private currentUserSubject: BehaviorSubject<User>;

  constructor(public http: HttpClient) {
    this.currentUserSubject = new BehaviorSubject<User>(JSON.parse(localStorage.getItem('currentUser')));
    this.currentUser$ = this.currentUserSubject.asObservable();
  }

  public get currentUser(): User {
    return this.currentUserSubject.value;
  }

  public login(username: string, password: string): Observable<User> {
    return this.http.post<TokenData>(this.AUTH_URL, {username, password})
      .pipe(map(
        data => {
          const user = new User(username, data.token);
          localStorage.setItem('currentUser', JSON.stringify(user));
          this.currentUserSubject.next(user);
          return user;
        })
      );
  }

  public logout(): void {
    localStorage.removeItem('currentUser');
    this.currentUserSubject.next(undefined);
  }
}
