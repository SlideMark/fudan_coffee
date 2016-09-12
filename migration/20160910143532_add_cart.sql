-- add_cart
CREATE TABLE fc_cart (
    id            BIGSERIAL PRIMARY KEY,
    uid           bigint NOT NULL,
    product_id    bigint not null,
    num          smallint not null default 1,
    state        smallint not null default 0,
    create_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
