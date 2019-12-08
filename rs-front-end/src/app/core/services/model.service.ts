import {BaseModel, Model, ModelState} from '../../app.models';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {ModelSerializer} from '../../app.serializers';
import {ModificationRequestStatusService} from './modification-request-status.service';
import {AuthService} from './auth.service';
import {environment} from '../../../environments/environment';
import {BaseModelService} from './base-model.service';


export class ModelService<T extends BaseModel> extends BaseModelService<T> {

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

  list(): Observable<T[]> {
    return this.userService.http.get(
      `${environment.apiUrl}${this.model.modelPlural}/`
    ).pipe(map((data: any) => this.convertData(data)));
  }

  filteredList(filter: string): Observable<T[]> {
    return this.userService.http.get(
      `${environment.apiUrl}${this.model.modelPlural}/?${filter}`
    ).pipe(map((data: any) => this.convertData(data)));
  }

  private convertData(data: any): T[] {
    return data.map(item => this.serializer.fromJson(item, ModelState.Retrieved));
  }

}
