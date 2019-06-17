import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {CheckBoxComponent} from './check-box/check-box.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatButtonModule, MatCheckboxModule} from '@angular/material';

@NgModule({
  declarations: [CheckBoxComponent],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatButtonModule,
    MatCheckboxModule,
  ],
  exports: [
    CheckBoxComponent,
  ]
})
export class SharedModule {
}
