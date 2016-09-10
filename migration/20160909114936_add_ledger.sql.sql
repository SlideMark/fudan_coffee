-- add_ledger.sql
CREATE TABLE fc_ledger (
    id            BIGSERIAL PRIMARY KEY,
    uid           bigint NOT NULL,
    name          varchar not null,
    money         integer not null,
    type        integer not null default 0,
    item_id     integer not null default 0,
    create_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
