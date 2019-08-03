import {Component, Inject, OnDestroy, OnInit} from '@angular/core';
import {webPageSize} from '../../shared/web-page/web-page/web-page.component';
import {FormBuilder, Validators} from '@angular/forms';
import {CodexService} from '../services/codex.service';
import {Observable, Subscription} from 'rxjs';
import {Codex} from '../../app.models';
import {ActivatedRoute, ParamMap, Router} from '@angular/router';
import {map, switchMap} from 'rxjs/operators';
import {MAT_DIALOG_DATA, MatDialog, MatDialogRef, MatSnackBar} from '@angular/material';

@Component({
  selector: 'app-codex-edit',
  templateUrl: './codex-edit.component.html',
  styleUrls: ['./codex-edit.component.scss']
})
export class CodexEditComponent implements OnInit, OnDestroy {

  codex$: Observable<Codex>;
  codex: Codex;
  codexSubscription: Subscription;
  codexForm = this.fb.group({
    title: ['', Validators.required],
    description: ['']
  });
  webPageSize = webPageSize;

  constructor(
    private fb: FormBuilder, private codexService: CodexService, private route: ActivatedRoute,
    private snackBar: MatSnackBar, public dialog: MatDialog, private router: Router
  ) {
  }


  ngOnInit() {
    this.codex$ = this.route.paramMap.pipe(
      switchMap((params: ParamMap) => this.codexService.get(params.get('slug')).pipe(
        map(
          codexList => {
            let codex: Codex;
            if (codexList.length > 0) {
              codex = codexList[0];
            }
            return codex;
          }
        )
      ))
    );
    this.codexSubscription = this.codex$.subscribe(codex => {
      this.codex = codex;
      this.initForm(this.codex);
    });
  }

  ngOnDestroy(): void {
    this.codexSubscription.unsubscribe();
  }

  initForm(codex: Codex): void {
    this.codexForm.reset({title: codex.title, description: codex.description});
  }

  onSubmit(): void {
    if (this.codexForm.valid && this.codexForm.dirty
    ) {
      const updatedCodex = Object.assign({}, this.codex);
      updatedCodex.title = this.codexForm.get('title').value;
      updatedCodex.description = this.codexForm.get('description').value;
      this.codexService.update(updatedCodex).subscribe(codex => {
        this.snackBar.open('Codex Updated !', 'Close', {duration: 2000, });
        this.initForm(codex);
      });
    }
  }

  deleteCodex(): void {
    const dialogRef = this.dialog.open(CodexEditDeleteDialogComponent, {
      width: '250px',
      data: this.codex
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result === 'delete') {
        this.codexService.delete(this.codex).subscribe(next => {
            const codexDetailsUrl = this.router.createUrlTree(['/codex']);
            this.snackBar.open('Codex Deleted !', 'Close', {duration: 2000, });
            this.router.navigateByUrl(codexDetailsUrl);
          }
        );
      }
    });
  }
}


@Component({
  selector: 'app-codex-edit-delete-dialog',
  templateUrl: 'codex-edit-delete-dialog.component.html',
  styleUrls: ['./codex-edit-delete-dialog.scss']
})
export class CodexEditDeleteDialogComponent {

  constructor(
    public dialogRef: MatDialogRef<CodexEditDeleteDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: Codex) {
  }

}
