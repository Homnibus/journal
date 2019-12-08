import {BaseModel, Model, ModelState} from '../../app.models';
import {Observable} from 'rxjs';
import {map, tap} from 'rxjs/operators';
import {ModelSerializer} from '../../app.serializers';
import {ModificationRequestStatusService} from './modification-request-status.service';
import {AuthService} from './auth.service';
import {environment} from '../../../environments/environment';


export abstract class BaseModelService<T extends BaseModel> {

  constructor(
    protected userService: AuthService,
    protected model: typeof Model,
    protected serializer: ModelSerializer<T>,
    protected modificationRequestStatusService: ModificationRequestStatusService,
  ) {
  }

  updateList(toUpdateModelList: T[], updatedModel: T): T[] {
    const modelListCopy = Object.assign([], toUpdateModelList);
    const modelCopy = Object.assign({}, updatedModel);

    const toUpdateModel = modelListCopy.find(function(currentModel: T) {
      // @ts-ignore
      return currentModel.id === this;
    }, modelCopy.id);
    const toUpdateModelIndex = modelListCopy.indexOf(toUpdateModel);
    modelListCopy[toUpdateModelIndex] = modelCopy;
    return modelListCopy;
  }

  deleteFromList(toUpdateModelList: T[], deletedModel: T): T[] {
    return toUpdateModelList.filter(function(currentModel: T) {
      return currentModel.id !== this;
    }, deletedModel.id);
  }

  get(id: number | string): Observable<T[]> {
    return this.userService.http.get(
      `${environment.apiUrl}${this.model.modelName}/${id}/`
    ).pipe(map(data => [this.serializer.fromJson(data, ModelState.Retrieved)]));
  }


  create(item: T): Observable<T> {
    this.modificationRequestStatusService.startSaveRequest();
    return this.userService.http.post(
      `${environment.apiUrl}${this.model.modelPlural}/`,
      this.serializer.toCreateJson(item)
    ).pipe(
      tap(() => this.modificationRequestStatusService.endSaveRequest()),
      map(data => this.serializer.fromJson(data, ModelState.Created))
    );
  }

  update(item: T): Observable<T> {
    this.modificationRequestStatusService.startSaveRequest();
    return this.userService.http.put(
      `${environment.apiUrl}${this.model.modelPlural}/${item[this.model.lookupField]}/`,
      this.serializer.toUpdateJson(item)
    ).pipe(
      tap(() => this.modificationRequestStatusService.endSaveRequest()),
      map(data => this.serializer.fromJson(data, ModelState.Modified))
    );
  }

  delete(item: T): Observable<T> {
    this.modificationRequestStatusService.startSaveRequest();
    return this.userService.http.delete(
      `${environment.apiUrl}${this.model.modelPlural}/${item[this.model.lookupField]}/`
    ).pipe(
      tap(() => this.modificationRequestStatusService.endSaveRequest()),
      map(() => undefined)
    );
  }
}
