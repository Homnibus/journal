import {animate, style, transition, trigger} from '@angular/animations';

export const slideTopTransition = trigger('slideTopTransition', [
  transition('void => CREATED', [
    style({height: 0, opacity: 0, transform: 'scale(0.5)'}),
    animate('0.5s ease-in-out', style({height: '*', opacity: 1, transform: 'scale(1)'}))
  ]),
  transition('* => void', [
    style({height: '*', opacity: 1, transform: 'scale(1)'}),
    animate('0.5s ease-in-out', style({height: 0, opacity: 0, transform: 'scale(0.5)'}))
  ]),
]);
