import {Component, OnInit} from '@angular/core';
import {Codex} from '../../app.models';
import {Observable} from 'rxjs';
import {CodexDetailsService} from "../codex-details.service";

@Component({
  selector: 'app-codex-details',
  templateUrl: './codex-details.component.html',
  styleUrls: ['./codex-details.component.scss']
})
export class CodexDetailsComponent implements OnInit {

  codex$: Observable<Codex>;

  constructor(private codexDetailsService: CodexDetailsService) {
  }

  ngOnInit() {
    this.codex$ = this.codexDetailsService.activeCodex$;
  }
}
