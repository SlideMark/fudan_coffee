-- add_item_id
alter table fc_payment add column item_id integer not null default 0;
