import {Codex, Information, Model, ModelState, Note, Page, Task} from './app.models';

export abstract class ModelSerializer<T extends Model> {
  abstract fromJson(json: any, state: ModelState): T;

  abstract toCreateJson(instance: T): any;

  abstract toUpdateJson(instance: T): any;
}

export class CodexSerializer implements ModelSerializer<Codex> {
  fromJson(json: any, state: ModelState): Codex {
    const codex = new Codex();
    codex.id = parseInt(json.id, 10);
    codex.title = json.title;
    codex.slug = json.slug;
    codex.description = json.description;
    codex.todoTasks = parseInt(json.todo_tasks, 10);
    codex.creationDate = new Date(json.creation_date);
    codex.nestedUpdateDate = new Date(json.nested_update_date);
    codex.updateDate = new Date(json.update_date);
    codex.state = state;

    return codex;
  }

  toJson(codex: Codex): any {
    return {
      title: codex.title,
      description: codex.description
    };
  }

  toCreateJson(codex: Codex): any {
    return this.toJson(codex);
  }

  toUpdateJson(codex: Codex): any {
    return this.toJson(codex);
  }
}

export class NoteSerializer implements ModelSerializer<Note> {
  fromJson(json: any, state: ModelState): Note {
    const note = new Note();
    note.id = parseInt(json.id, 10);
    note.page = parseInt(json.page, 10);
    note.text = json.text;
    note.initialHash = json.initial_hash;
    note.creationDate = new Date(json.creation_date);
    note.updateDate = new Date(json.update_date);
    note.state = state;

    return note;
  }

  toCreateJson(note: Note): any {
    return {
      text: note.text,
      codex: note.codex,
    };
  }

  toUpdateJson(note: Note): any {
    return {
      text: note.text,
      modification_hash: note.initialHash
    };
  }
}

export class TaskSerializer implements ModelSerializer<Task> {
  fromJson(json: any, state: ModelState): Task {
    const task = new Task();
    task.id = parseInt(json.id, 10);
    task.page = parseInt(json.page, 10);
    task.text = json.text;
    task.isAchieved = json.is_achieved;
    task.initialHash = json.initial_hash;
    task.achievedDate = json.achieved_date ? new Date(json.achieved_date) : null;
    task.creationDate = new Date(json.creation_date);
    task.updateDate = new Date(json.update_date);
    task.state = state;

    return task;
  }

  toCreateJson(task: Task): any {
    return {
      text: task.text,
      is_achieved: task.isAchieved,
      codex: task.codex
    };
  }

  toUpdateJson(task: Task): any {
    return {
      text: task.text,
      is_achieved: task.isAchieved,
      modification_hash: task.initialHash
    };
  }
}

export class PageSerializer implements ModelSerializer<Page> {
  fromJson(json: any, state: ModelState): Page {
    const page = new Page();

    page.id = parseInt(json.id, 10);
    page.codex = parseInt(json.codex, 10);
    page.date = new Date(json.date);
    page.creationDate = new Date(json.creation_date);
    page.nestedUpdateDate = new Date(json.nested_update_date);
    const noteSerializer = new NoteSerializer();
    page.note = json.note ? noteSerializer.fromJson(json.note, state) : null;
    const taskSerializer = new TaskSerializer();
    page.tasks = Array.from(json.tasks, x => taskSerializer.fromJson(x, state));
    page.state = state;

    return page;
  }

  toCreateJson(instance: Page): any {
    return;
  }

  toUpdateJson(instance: Page): any {
    return;
  }

}


export class InformationSerializer implements ModelSerializer<Information> {
  fromJson(json: any, state: ModelState): Information {
    const information = new Information();
    information.id = parseInt(json.id, 10);
    information.codex = parseInt(json.codex, 10);
    information.text = json.text;
    information.initialHash = json.initial_hash;
    information.creationDate = new Date(json.creation_date);
    information.updateDate = new Date(json.update_date);
    information.state = state;

    return information;
  }

  toCreateJson(information: Task): any {
    return {
      codex: information.codex,
      text: information.text
    };
  }

  toUpdateJson(information: Task): any {
    return {
      text: information.text,
      modification_hash: information.initialHash
    };
  }
}
