-- 
alter table fc_payment_transaction add column from_cart smallint not null default 0;
