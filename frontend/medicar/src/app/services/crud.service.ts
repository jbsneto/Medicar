import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'

@Injectable({
  providedIn: 'root'
})
export class CrudService {

  private apiUrl = 'http://127.0.0.1:8000/api/';
  
  private consultaUrl = this.apiUrl + 'consulta/';

  constructor(private http: HttpClient) { }

  getConsultaEvent(){
    return this.http.get<any>(this.consultaUrl)
  }
}
