import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/auth/auth.service';
import { CrudService } from '../crud.service';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  consultas = []

  consultaId: string

  constructor(
    private crudEvent: CrudService,
    public auth: AuthService,
    public crud: CrudService,
    private router: Router
    ) { }

  ngOnInit(): void {
    this.crudEvent.getConsultaEvent()
      .subscribe(
        res => this.consultas = res,
        err => console.log(err)
      )
  }

  deleteConsulta(){
    this.crud.deleteConsultaEvent(this.consultaId)
      .subscribe(
        res => {
          console.log(res),
          this.router.navigate(['/'])
        },
        err => console.log(err)
      )
  }
  
}
