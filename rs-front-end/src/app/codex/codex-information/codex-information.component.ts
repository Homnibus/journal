import {Component, OnInit} from '@angular/core';
import {Codex, Information} from '../../app.models';
import {InformationService} from '../../information/information.service';
import {CodexDetailsService} from '../services/codex-details.service';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-codex-information',
  templateUrl: './codex-information.component.html',
  styleUrls: ['./codex-information.component.scss']
})
export class CodexInformationComponent implements OnInit {

  private informationEditable = false;
  codex: Codex;
  private information: Information[];

  constructor(private informationService: InformationService,
              private codexDetailsService: CodexDetailsService,
              private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.route.parent.data.subscribe(data => {
      this.codex = data.codex;
    });
    this.route.data.subscribe(data => {
      this.information = data.information;
    });
  }

  switchEditMode(): void {
    this.informationEditable = !this.informationEditable;
  }

}
