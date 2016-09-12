-- add_column_password
alter table fc_user add column password varchar;
create unique index fc_user_phone on fc_user(phone);
