import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { MatSnackBar } from "@angular/material/snack-bar";
import { Router } from '@angular/router';
import { Observable, EMPTY } from "rxjs";
import { map, catchError } from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = 'http://127.0.0.1:8000/api/';
  
  private registerUrl = this.apiUrl + 'user/';
  private loginUrl = this.apiUrl + 'user/token/';

  constructor(
    private snackBar: MatSnackBar,
    private http: HttpClient,
    private router: Router
    ) { }

  registerUser(user){
    return this.http.post<any>(this.registerUrl, user, {headers:{skip:"true"}}).pipe(
      map((res) => this.createHandler(res)),
      catchError((e) => this.errorHandler(e))
    );
  }

  loginUser(user){
    return this.http.post<any>(this.loginUrl, user).pipe(
      map(res => res),
      catchError((e) => this.errorHandler(e))
    )
  }

  logoutUser(){
    localStorage.removeItem('token_access')
    localStorage.removeItem('token_refresh')
    this.router.navigate(['/login'])
  }



  // get token localStorafe {browser/application} / inject token in auth-interceptor
  getToken(){
    return localStorage.getItem('token_access')
  }

  showMessage(msg: string, isError: boolean = false): void {
    this.snackBar.open(msg, "X", {
      duration: 3000,
      horizontalPosition: "right",
      verticalPosition: "top",
      panelClass: isError ? ["msg-error"] : ["msg-success"],
    });
  }

  errorHandler(e: any): Observable<any> {
    console.log(e)
    if (e.error.username){
      this.showMessage(`Usuário: ${e.error.username}`, true);
    }
    if (e.error.email){
      this.showMessage(`Email: ${e.error.email}`, true);
    }
    if (e.error.password){
      this.showMessage(`Senha: ${e.error.password}`, true);
    }
    return EMPTY;
  }

  createHandler(res: any): Observable<any> {
    this.showMessage(`Usuário registrado com sucesso.`, false);
    return EMPTY;
  }

}
