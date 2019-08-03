import {animate, style, transition, trigger} from '@angular/animations';

export const saveIconTransition = trigger('saveIconTransition', [
  transition('2 => *', [
    style({ opacity: 1}),
    animate('0.75s ease-in-out', style({opacity: 1})),
    animate('0.25s ease-in-out', style({opacity: 0}))
  ]),
  transition('void => 1', [
    style({ opacity: 0}),
    animate('0.25s ease-in-out', style({opacity: 1}))
  ]),
]);
