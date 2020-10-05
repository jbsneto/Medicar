import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CrudService } from '../crud.service';

@Component({
  selector: 'app-consulta',
  templateUrl: './consulta.component.html',
  styleUrls: ['./consulta.component.css']
})
export class ConsultaComponent implements OnInit {

  especialidades = []
  especialidadeId = 0
  medicos = []

  constructor(
    private crudEvent: CrudService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.crudEvent.getEspecialidadeEvent()
      .subscribe(
        res => this.especialidades = res,
        err => console.log(err)
      )
  }


}
