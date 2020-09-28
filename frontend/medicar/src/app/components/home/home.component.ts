import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';
import { CrudService } from 'src/app/services/crud.service';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  consultas = []

  constructor(
    private crudEvent: CrudService,
    public auth: AuthService
    ) { }

  ngOnInit(): void {
    this.crudEvent.getConsultaEvent()
      .subscribe(
        res => this.consultas = res,
        err => console.log(err)
      )
  }
  
}
