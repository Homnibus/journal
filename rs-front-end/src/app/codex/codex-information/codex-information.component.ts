import {Component, OnInit} from '@angular/core';
import {Codex, Information} from '../../app.models';
import {InformationService} from '../../information/information.service';
import {CodexDetailsService} from '../services/codex-details.service';
import {switchMap} from 'rxjs/operators';
import {Observable} from 'rxjs';

@Component({
  selector: 'app-codex-information',
  templateUrl: './codex-information.component.html',
  styleUrls: ['./codex-information.component.scss']
})
export class CodexInformationComponent implements OnInit {

  private informationEditable = false;
  codex$: Observable<Codex>;
  private information$: Observable<Information[]>;

  constructor(private informationService: InformationService, private codexDetailsService: CodexDetailsService) {
  }

  ngOnInit() {
    this.codex$ = this.codexDetailsService.activeCodex$;
    this.information$ = this.codex$.pipe(
      switchMap(codex => this.informationService.getCodexInformation(codex.slug)),
    );
  }

  switchEditMode(): void {
    this.informationEditable = !this.informationEditable;
  }

}
