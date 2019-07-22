import {HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {Observable} from 'rxjs';
import {AuthService} from '../services/auth.service';
import {Injectable} from "@angular/core";

@Injectable({providedIn: 'root'})
export class AuthInterceptor implements HttpInterceptor {

  constructor(private authService: AuthService) {
  }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    let newHeaders = req.headers;
    if (this.authService.currentUser) {
      newHeaders = req.headers.append('Authorization', `Token ${this.authService.currentUser.token}`);
    }
    const newRequest = req.clone({headers: newHeaders});
    return next.handle(newRequest);
  }
}
