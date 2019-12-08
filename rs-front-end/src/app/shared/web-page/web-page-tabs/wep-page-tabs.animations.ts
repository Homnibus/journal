import {animate, query, style, transition, trigger} from '@angular/animations';

export const routerTransition = trigger('routerTransition', [
        transition( '* => *', [
          query(':enter',
            [
              style({ opacity: 0 })
            ],
            { optional: true }
          ),

          query(':leave',
            [
              style({ opacity: 1,
                position: 'absolute',
                top: 0,
                left: '1em',
                right: '1em',
              }),
              animate('0.2s', style({ opacity: 0 }))
            ],
            { optional: true }
          ),

          query(':enter',
            [
              style({ opacity: 0 }),
              animate('0.2s', style({ opacity: 1 }))
            ],
            { optional: true }
          )

        ])
  ]);
