import { HttpInterceptor } from '@angular/common/http';
import { Injectable, Injector } from '@angular/core';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class TokenInterceptorService implements HttpInterceptor{

  constructor(
    private injector: Injector
  ) { }

  // coloca o token no head da solucitação da página
  intercept(req, next) {
    let authService = this.injector.get(AuthService)
    let tokenizesRed = req.clone({
      setHeaders: {
        // insert token in headers page {browser/network}
        Authorization: `Token ${authService.getToken()}` 
      }
    })
    return next.handle(tokenizesRed)
  }
}
