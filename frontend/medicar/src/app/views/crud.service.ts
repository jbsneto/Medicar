import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Observable } from 'rxjs';

// injetavel em componentes
@Injectable({
  providedIn: 'root'
})
export class CrudService {

  private apiUrl = 'http://127.0.0.1:8000/api/';

  private consultaUrl = `${this.apiUrl}consulta/`;
  private especialidadeUrl = `${this.apiUrl}especialidade/`;

  constructor(private http: HttpClient) { }

  getConsultaEvent(): Observable<any> {
    return this.http.get<any>(this.consultaUrl)
  }

  getEspecialidadeEvent(): Observable<any> {
    return this.http.get<any>(this.especialidadeUrl)
  }

  deleteConsultaEvent(id: string): Observable<any> {
    const url = `${this.consultaUrl}/${id}`;
    return this.http.delete<any>(url);
  }
}
