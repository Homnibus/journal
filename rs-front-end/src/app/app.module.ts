import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {AppRoutingModule} from './app-routing.module';
import {CoreModule} from './core/core.module';
import {CodexModule} from './codex/codex.module';
import {AuthInterceptor} from './core/interceptor/auth.interceptor';
import {HTTP_INTERCEPTORS} from '@angular/common/http';
import {MarkdownModule} from 'ngx-markdown';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {ErrorInterceptor} from './core/interceptor/error.interceptor';
import {ErrorRoutingModule} from './core/error/error-routing.module';

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    CoreModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MarkdownModule.forRoot(),
    CodexModule,
    ErrorRoutingModule,
  ],
  providers: [
    {provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true},
    {provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true},
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
