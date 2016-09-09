-- add_product.sql
CREATE TABLE fc_product (
    id            BIGSERIAL PRIMARY KEY,
    name          varchar not null,
    description   varchar,
    icon          varchar not null,
    creator       bigint NOT NULL,
    shop_id      smallint not null default 0,
    price        integer not null default 0,
    create_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
