update django_content_type set app_label = 'rs_back_end' where app_label = 'projets';

alter table projets_codex rename to rs_back_end_codex;
alter table projets_information rename to rs_back_end_information;
alter table projets_note rename to rs_back_end_note;
alter table projets_page rename to rs_back_end_page;
alter table projets_task rename to rs_back_end_task;

UPDATE django_migrations SET app='rs_back_end' WHERE app='projets';
