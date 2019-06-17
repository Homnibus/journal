import {Component} from '@angular/core';
import {FormBuilder, Validators} from '@angular/forms';
import {CodexService} from '../codex.service';
import {Codex} from '../../app.models';
import {Router} from '@angular/router';

@Component({
  selector: 'app-codex-add',
  templateUrl: './codex-add.component.html',
  styleUrls: ['./codex-add.component.scss']
})
export class CodexAddComponent {

  codexForm = this.fb.group({
    title: ['', Validators.required],
    description: ['']
  });

  constructor(private fb: FormBuilder, private codexService: CodexService, private router: Router) {
  }

  onSubmit(): void {
    const newCodex = new Codex();
    newCodex.title = this.codexForm.get('title').value;
    newCodex.description = this.codexForm.get('description').value;
    this.codexService.create(newCodex).subscribe(
      codex => {
        const codexDetailsUrl = this.router.createUrlTree(['/codex', codex.slug]);
        this.router.navigateByUrl(codexDetailsUrl);
      }
    );
  }

}
