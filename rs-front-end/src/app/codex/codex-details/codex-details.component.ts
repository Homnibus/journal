import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, ParamMap, Router} from '@angular/router';
import {Codex} from '../../app.models';
import {switchMap} from 'rxjs/operators';
import {Observable} from 'rxjs';
import {CodexService} from '../codex.service';

@Component({
  selector: 'app-codex-details',
  templateUrl: './codex-details.component.html',
  styleUrls: ['./codex-details.component.scss']
})
export class CodexDetailsComponent implements OnInit {

  codex$: Observable<Codex>;

  constructor(
    private codexService: CodexService,
    private route: ActivatedRoute,
    private router: Router,
  ) {

  }

  ngOnInit() {
    this.codex$ =
      this.route.paramMap.pipe(
        switchMap((params: ParamMap) =>
          this.codexService.get(params.get('slug')))
      );
  }

  updateCodex(codex: Codex): void {
    console.log('update');
    this.codexService.update(codex).subscribe(
      updatedCodex => console.log(updatedCodex)
    );
  }

  deleteCodex(codex: Codex): void {
    console.log('delete');
    this.codexService.delete(codex).subscribe();
    this.router.navigate(['/codex']);
  }
}
