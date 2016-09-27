-- add_order
CREATE TABLE fc_order (
    id           BIGSERIAL PRIMARY KEY,
    order_id     varchar not null,
    uid          bigint NOT NULL,
    name         varchar not null,
    money        integer not null default 0,
    balance      integer not null default 0,
    coupon       integer not null default 0,
    item_id      integer not null default 0,
    type         smallint not null default 0,
    state        smallint not null default 0,
    extra        varchar,
    create_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
create unique index fc_order_order_id on fc_order(order_id);