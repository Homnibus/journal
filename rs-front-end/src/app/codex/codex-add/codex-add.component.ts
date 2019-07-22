import {Component} from '@angular/core';
import {FormBuilder, Validators} from '@angular/forms';
import {CodexService} from '../services/codex.service';
import {Codex} from '../../app.models';
import {Router} from '@angular/router';
import {webPageSize} from '../../web-page/web-page/web-page.component';

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
  webPageSize = webPageSize;

  constructor(private fb: FormBuilder, private codexService: CodexService, private router: Router) {
  }

  onSubmit(): void {
    if (this.codexForm.valid) {
      const newCodex = new Codex();
      newCodex.title = this.codexForm.get('title').value;
      newCodex.description = this.codexForm.get('description').value;
      this.codexService.create(newCodex).subscribe(
        codex => {
          const codexDetailsUrl = this.router.createUrlTree(['/codex/details', codex.slug]);
          this.router.navigateByUrl(codexDetailsUrl);
        }
      );
    }
  }

}
