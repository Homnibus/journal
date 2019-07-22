import {HttpErrorResponse, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {Observable, throwError} from 'rxjs';
import {catchError} from "rxjs/operators";
import {Router} from "@angular/router";
import {Injectable} from "@angular/core";

@Injectable({providedIn: 'root'})
export class ErrorInterceptor implements HttpInterceptor {

  constructor(private router: Router) {
  }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(req).pipe(
      catchError((error: HttpErrorResponse) => {
        let errorUrl: string;
        switch (error.status) {
          case 400: {
            return throwError(error);
          }
          case 404: {
            errorUrl = '/error/not-found';
            break;
          }
          case 403: {
            errorUrl = '/error/forbidden';
            break;
          }
          default: {
            errorUrl = '/error/unexpected';
            break;
          }
        }
        this.router.navigateByUrl(errorUrl);
        return throwError(error);
      })
    );
  }
}
