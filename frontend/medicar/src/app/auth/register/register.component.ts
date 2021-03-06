import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  registerUserData = {
    username: '',
    email: '',
    password: '',
  }

  error = {
    username: '',
    email: '',
    password: '',
  }

  constructor(
    private auth: AuthService,
    private router: Router
    ) { }

  ngOnInit(): void {
  }
  
  registerUser(){
    this.auth.registerUser(this.registerUserData)
    .subscribe(
      res => console.log(res),
      err => this.error = err
    )
  }

}