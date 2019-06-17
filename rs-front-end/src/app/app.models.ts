// List of models used by the application
export abstract class Model {
  public static modelName: string;
  public static modelPlural: string;

  public static lookupField: string;
}

export class DefaultLookupField {
  public static lookupField = 'id';
}

export class Codex implements Model {
  public static modelName = 'codex';
  public static modelPlural = 'codex';

  public static lookupField = 'slug';
  public id: number;
  public title: string;
  public slug: string;
  public description: string;
  public creationDate: Date;
  public nestedUpdateDate: Date;
  public updateDate: Date;
}

export class Page extends DefaultLookupField implements Model {
  public static modelName = 'page';
  public static modelPlural = 'pages';

  public id: number;
  public codex: number;
  public date: Date;
  public creationDate: Date;
  public nestedUpdateDate: Date;
  public note: Note;
  public tasks: Task[];
}

export class Note extends DefaultLookupField implements Model {
  public static modelName = 'note';
  public static modelPlural = 'notes';

  public id: number;
  public page: number;
  public text: string;
  public initialHash: string;
  public creationDate: Date;
  public updateDate: Date;

  public codex: number;

}

export class Task extends DefaultLookupField implements Model {
  public static modelName = 'task';
  public static modelPlural = 'tasks';

  public id: number;
  public page: number;
  public text: string;
  public isAchieved: boolean;
  public initialHash: string;
  public achievedDate: Date;
  public creationDate: Date;
  public updateDate: Date;

  public codex: number;
}

export class User {
  public name: string;
  public token: string;

  constructor(name: string, token: string) {
    this.token = token;
    this.name = name;
  }
}
