import {animate, group, query, style, transition, trigger} from '@angular/animations';

export const routerTransition = trigger('routerTransition', [
  transition(':decrement', [
    query(':enter, :leave', style({
        position: 'absolute',
        top: '0',
      }),
      {optional: true}),
    group([
      query(':enter', [
        style({
          right: '150%',
          left: '-150%',
        }),
        animate('0.5s ease-in-out', style({
          right: '1em',
          left: '1em',
        }))
      ], {optional: true}),
      query(':leave', [
        style({
          right: '1em',
          left: '1em',
        }),
        animate('0.5s ease-in-out', style({
          right: '-150%',
          left: '150%',
        }))
      ], {optional: true}),
    ])
  ]),
  transition(':increment', [
    group([
      query(':enter, :leave', style({
          position: 'absolute',
          top: '0',
        })
        , {optional: true}),
      query(':enter', [
        style({
          right: '-150%',
          left: '150%',
        }),
        animate('0.5s ease-in-out', style({
          right: '1em',
          left: '1em',
        }))
      ], {optional: true}),
      query(':leave', [
        style({
          right: '1em',
          left: '1em',
        }),
        animate('0.5s ease-in-out', style({
          right: '150%',
          left: '-150%',
        }))
      ], {optional: true}),
    ])
  ])
]);
