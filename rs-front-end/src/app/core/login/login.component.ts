import {Component} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {AuthService} from '../services/auth.service';
import {FormBuilder, Validators} from "@angular/forms";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {

  loginForm = this.fb.group({
    userName: ['', Validators.required],
    password: ['', Validators.required]
  });
  hide = true;

  constructor(private authService: AuthService, private router: Router, private route: ActivatedRoute, private fb: FormBuilder) {
  }

  get userName() {
    return this.loginForm.get('userName');
  }

  get password() {
    return this.loginForm.get('password');
  }

  tryLogin(): void {
    if (this.loginForm.valid) {
      this.authService.login(this.loginForm.get('userName').value, this.loginForm.get('password').value).subscribe(
        user => {
          const nextUrl = this.route.snapshot.queryParamMap.get('next');
          this.router.navigateByUrl(nextUrl);
        },
        err => {
          if (err.status == 400) {
            this.loginForm.setErrors({invalidUserOrPassword: true});
          } else {
            throw err;
          }
        }
      );
    }
  }
}
