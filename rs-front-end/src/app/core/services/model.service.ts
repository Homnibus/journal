import {Model} from '../../app.models';
import {Observable} from 'rxjs';
import {map, tap} from 'rxjs/operators';
import {ModelSerializer} from '../../app.serializers';
import {ModificationRequestStatusService} from './modification-request-status.service';
import {AuthService} from './auth.service';


export class ModelService<T extends Model> {

  constructor(
    private userService: AuthService,
    private model: typeof Model,
    private serializer: ModelSerializer<T>,
    private modificationRequestStatusService: ModificationRequestStatusService,
  ) {
  }

  list(): Observable<T[]> {
    return this.userService.http.get(
      `${this.userService.API_URL}/${this.model.modelPlural}/`
    ).pipe(map((data: Array<object>) => this.convertData(data)));
  }

  filteredList(filter: string): Observable<T[]> {
    return this.userService.http.get(
      `${this.userService.API_URL}/${this.model.modelPlural}/?${filter}`
    ).pipe(map((data: Array<object>) => this.convertData(data)));
  }

  get(id: number | string): Observable<T> {
    return this.userService.http.get(
      `${this.userService.API_URL}/${this.model.modelName}/${id}/`
    ).pipe(map(data => this.serializer.fromJson(data)));
  }


  create(item: T): Observable<T> {
    this.modificationRequestStatusService.requestStart();
    return this.userService.http.post(
      `${this.userService.API_URL}/${this.model.modelPlural}/`,
      this.serializer.toCreateJson(item)
    ).pipe(
      tap(() => this.modificationRequestStatusService.requestEnd()),
      map(data => this.serializer.fromJson(data))
    );
  }

  update(item: T): Observable<T> {
    this.modificationRequestStatusService.requestStart();
    return this.userService.http.put(
      `${this.userService.API_URL}/${this.model.modelPlural}/${item[this.model.lookupField]}/`,
      this.serializer.toUpdateJson(item)
    ).pipe(
      tap(() => this.modificationRequestStatusService.requestEnd()),
      map(data => this.serializer.fromJson(data))
    );
  }

  delete(item: T) {
    this.modificationRequestStatusService.requestStart();
    return this.userService.http.delete(
      `${this.userService.API_URL}/${this.model.modelName}/${item[this.model.lookupField]}/`
    ).pipe(
      tap(() => this.modificationRequestStatusService.requestEnd())
    );
  }

  private convertData(data: any): T[] {
    return data.map(item => this.serializer.fromJson(item));
  }
}
