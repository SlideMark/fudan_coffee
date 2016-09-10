-- add_payment_item
CREATE TABLE fc_payment_item (
    id            BIGSERIAL PRIMARY KEY,
    name        varchar not null,
    description  varchar,
    money       integer NOT NULL,
    charge      integer NOT NULL default 0,
    create_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
