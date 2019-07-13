import {Injectable} from "@angular/core";
import {Codex} from "../app.models";
import {CodexService} from "./codex.service";
import {BehaviorSubject, Observable} from "rxjs";
import {map} from "rxjs/operators";


@Injectable({
  providedIn: 'root',
})
export class CodexDetailsService {

  private activeCodexSubject = new BehaviorSubject<Codex>(undefined);
  public activeCodex$ = this.activeCodexSubject.asObservable();

  constructor(private codexService: CodexService) {
  }

  setActiveCodex(slug: string): Observable<Codex> {
    return this.codexService.get(slug).pipe(
      map(
        codex => {
          this.activeCodexSubject.next(codex);
          return codex;
        }
      )
    );
  }

  removeActiveCodex(): void {
    this.activeCodexSubject.next(undefined);
  }

}
