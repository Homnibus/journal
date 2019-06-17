import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {AppRoutingModule} from './app-routing.module';
import {CoreModule} from './core/core.module';
import {CodexModule} from './codex/codex.module';
import {NoteModule} from './note/note.module';
import {TaskModule} from './task/task.module';
import {AuthInterceptor} from './core/auth.interceptor';
import {HTTP_INTERCEPTORS} from '@angular/common/http';
import {SharedModule} from './shared/shared.module';
import {MarkdownModule} from 'ngx-markdown';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';


@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    CoreModule,
    SharedModule,
    CodexModule,
    NoteModule,
    TaskModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MarkdownModule.forRoot(),
  ],
  providers: [
    {provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true},
  ],
  exports: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
