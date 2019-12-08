import {BaseModel, Model, ModelState} from '../../app.models';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {ModelSerializer} from '../../app.serializers';
import {ModificationRequestStatusService} from './modification-request-status.service';
import {AuthService} from './auth.service';
import {environment} from '../../../environments/environment';
import {BaseModelService} from './base-model.service';


export class PaginationContainer<T extends BaseModel> {
  count: number;
  next: string;
  previous: string;
  results: T[];
}

export class ModelPaginationService<T extends BaseModel> extends BaseModelService<T> {

  constructor(
    userService: AuthService,
    model: typeof Model,
    serializer: ModelSerializer<T>,
    modificationRequestStatusService: ModificationRequestStatusService,
  ) {
    super(
      userService,
      model,
      serializer,
      modificationRequestStatusService,
    );
  }

  list(pageNumber: number): Observable<PaginationContainer<T>> {
    const sanitizePageNumber = pageNumber > 0 ? pageNumber : 0;
    return this.userService.http.get(
      `${environment.apiUrl}${this.model.modelPlural}/?page=${sanitizePageNumber}`
    ).pipe(map((data: any) => this.convertData(data)));
  }

  filteredList(filter: string, pageNumber: number): Observable<PaginationContainer<T>> {
    const sanitizePageNumber = pageNumber > 0 ? pageNumber : 0;
    return this.userService.http.get(
      `${environment.apiUrl}${this.model.modelPlural}/?${filter}&page=${sanitizePageNumber}`
    ).pipe(map((data: any) => this.convertData(data)));
  }

  protected convertData(data: any): PaginationContainer<T> {
    const paginationContainer = new PaginationContainer<T>();
    paginationContainer.count = data.count;
    paginationContainer.next = data.next;
    paginationContainer.previous = data.previous;
    paginationContainer.results = data.results.map(item => this.serializer.fromJson(item, ModelState.Retrieved));
    return paginationContainer;
  }

}
