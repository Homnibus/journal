import {Component, OnDestroy, OnInit} from '@angular/core';
import {Codex} from '../../app.models';
import {CodexService} from '../codex.service';
import {NavigationLink, NavigationService} from '../../core/navigation/navigation.service';
import {FormControl} from '@angular/forms';
import {Subscription} from 'rxjs';
import {debounceTime} from 'rxjs/operators';


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
    private navigationService: NavigationService,
  ) {
  }

  ngOnInit() {
    const links = [new NavigationLink('/codex/13', 'Codex 13')];
    this.navigationService.setLinks(links);
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
