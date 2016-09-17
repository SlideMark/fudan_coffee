-- add_extra_to_tr
alter table fc_payment_transaction add column balance integer not null default 0;
alter table fc_payment_transaction add column coupon integer not null default 0;
