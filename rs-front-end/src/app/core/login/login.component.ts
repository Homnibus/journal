import {Component} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {AuthService} from '../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {

  userName = 'homnibus';
  password = 'gata585674';

  constructor(private authService: AuthService, private router: Router, private route: ActivatedRoute) {
  }

  tryLogin(): void {
    this.authService.login(this.userName, this.password).subscribe(
      user => {
        const nextUrl = this.route.snapshot.queryParamMap.get('next');
        this.router.navigateByUrl(nextUrl);
      }
    );
  }
}
