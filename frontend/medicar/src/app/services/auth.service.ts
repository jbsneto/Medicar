import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = 'http://127.0.0.1:8000/api/';
  
  private registerUrl = this.apiUrl + 'user/';
  private loginUrl = this.apiUrl + 'user/token/';

  constructor(
    private http: HttpClient,
    private router: Router
    ) { }

  registerUser(user){
    return this.http.post<any>(this.registerUrl, user)
  }

  // post user
  loginUser(user){
    return this.http.post<any>(this.loginUrl, user)
  }

  // get token localStorafe {browser/application} / inject token in auth-interceptor
  getToken(){
    return localStorage.getItem('token_access')
  }

  logoutUser(){
    localStorage.removeItem('token_access')
    localStorage.removeItem('token_refresh')
    this.router.navigate(['/login'])
  }

}
