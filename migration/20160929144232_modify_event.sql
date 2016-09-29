-- modify_event.=
alter table fc_event add column shop_id smallint not null default 0;
alter table fc_event add column title varchar not null;


