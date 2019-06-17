import {Component, Input} from '@angular/core';
import {AuthService} from '../../core/services/auth.service';

@Component({
  selector: 'app-nav-codex-detail',
  templateUrl: './nav-codex-detail.component.html',
  styleUrls: ['./nav-codex-detail.component.scss']
})
export class NavCodexDetailComponent {

  @Input()
  codexSlug: string;

  constructor(private authService: AuthService) {
  }
}
