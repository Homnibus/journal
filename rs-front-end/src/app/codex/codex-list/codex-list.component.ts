import {Component, OnDestroy, OnInit} from '@angular/core';
import {Codex} from '../../app.models';
import {CodexService} from '../codex.service';
import {FormControl} from '@angular/forms';
import {Subscription} from 'rxjs';
import {debounceTime} from 'rxjs/operators';
import * as seedrandom from 'seedrandom';


@Component({
  selector: 'app-codex-list',
  templateUrl: './codex-list.component.html',
  styleUrls: ['./codex-list.component.scss']
})
export class CodexListComponent implements OnInit, OnDestroy {

  codexSearchControl: FormControl;
  codexSearchControlOnChange: Subscription;
  private dataSource: Codex[];
  private filteredCodexList: Codex[];

  constructor(
    private codexService: CodexService,
  ) {
  }

  ngOnInit() {
    this.fetchCodex();

    this.codexSearchControl = new FormControl();
    this.codexSearchControlOnChange = this.codexSearchControl.valueChanges.pipe(
      debounceTime(200),
    )
      .subscribe(value => this.codexSearch(value));
  }

  ngOnDestroy() {
    this.codexSearchControlOnChange.unsubscribe();
  }

  fetchCodex(): void {
    this.codexService.list().subscribe(
      data => {
        this.dataSource = data;
        this.filteredCodexList = Object.assign([], this.dataSource);
      }
    );
  }

  getCodexColor(codex: Codex): string {
    const seededRandomNumberGenerator = seedrandom(codex.id.toString());
    return "hsl(" + Math.floor(seededRandomNumberGenerator() * 360).toString() + ",100%,70%)";
  }

  codexSearch(value: string): void {
    const filter = value.toLowerCase().split(' ');
    this.filteredCodexList = this.dataSource.filter(
      codex => {
        let include = true;
        for (const word of filter) {
          include = Boolean(codex.title.toLowerCase().includes(word) && include);
        }
        return include;
      });
  }
}
