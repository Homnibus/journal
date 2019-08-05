import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {InformationDetailsComponent} from './information-details/information-details.component';
import {MarkdownModule} from 'ngx-markdown';
import {ReactiveFormsModule} from '@angular/forms';
import {SharedModule} from '../shared/shared.module';

@NgModule({
  declarations: [
    InformationDetailsComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    MarkdownModule,
    ReactiveFormsModule,
  ],
  exports: [
    InformationDetailsComponent,
  ],
})
export class InformationModule {
}
