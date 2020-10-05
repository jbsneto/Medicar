import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Observable } from 'rxjs';

// injetavel em componentes
@Injectable({
  providedIn: 'root'
})
export class CrudService {

  private apiUrl = 'http://127.0.0.1:8000/api/consulta/';

  constructor(private http: HttpClient) { }

  getConsultaEvent(){
    return this.http.get<any>(this.apiUrl)
  }

  deleteConsultaEvent(id: string){
    const url = `${this.apiUrl}/${id}`;
    return this.http.delete<any>(url);
  }
}
