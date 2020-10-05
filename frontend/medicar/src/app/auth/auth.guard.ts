import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { AuthService } from '../auth/auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(
    private authService: AuthService,
    private router: Router
    ) { }

  // guard get token service
  canActivate(): boolean{
    if (this.authService.getToken()){
      return true
    } else {
      this.router.navigate(['/login'])
      return false
    }
  }
}
