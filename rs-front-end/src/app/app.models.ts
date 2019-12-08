// List of models used by the application

export enum ModelState {
  Retrieved = 'RETRIEVED',
  Created = 'CREATED',
  Modified = 'MODIFIED',
  Deleted = 'DELETED',
}

export abstract class Model {
  public static modelName: string;
  public static modelPlural: string;

  public static lookupField: string;
  public state: ModelState;
  public id: number;
}


export class BaseModel {
  public static lookupField = 'id';
  public state: ModelState;
  public id: number;
}

export class Codex extends BaseModel implements Model {
  public static modelName = 'codex';
  public static modelPlural = 'codex';

  public static lookupField = 'slug';
  public title: string;
  public slug: string;
  public description: string;
  public todoTasks: number;
  public creationDate: Date;
  public nestedUpdateDate: Date;
  public updateDate: Date;
}

export class Page extends BaseModel implements Model {
  public static modelName = 'page';
  public static modelPlural = 'pages';

  public codex: number;
  public date: Date;
  public creationDate: Date;
  public nestedUpdateDate: Date;
  public note: Note;
  public tasks: Task[] = [];
}

export class Note extends BaseModel implements Model {
  public static modelName = 'note';
  public static modelPlural = 'notes';

  public page: number;
  public text: string;
  public initialHash: string;
  public creationDate: Date;
  public updateDate: Date;

  public codex: number;

}

export class Task extends BaseModel implements Model {
  public static modelName = 'task';
  public static modelPlural = 'tasks';

  public page: number;
  public text: string;
  public isAchieved: boolean;
  public initialHash: string;
  public achievedDate: Date;
  public creationDate: Date;
  public updateDate: Date;

  public codex: number;
}

export class Information extends BaseModel implements Model {
  public static modelName = 'information';
  public static modelPlural = 'information';

  public codex: number;
  public text: string;
  public initialHash: string;
  public creationDate: Date;
  public updateDate: Date;
}

export class User {
  public name: string;
  public token: string;

  constructor(name: string, token: string) {
    this.token = token;
    this.name = name;
  }
}
