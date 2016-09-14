-- add_payment
-- COLUMNS = ['id', 'uid', 'item_id', 'num', 'money', 'description', 'create_at', 'update_at']

CREATE TABLE fc_payment (
    id            BIGSERIAL PRIMARY KEY,
    uid           bigint NOT NULL,
    num         smallint not null default 1,
    money       integer not null default 0,
    description varchar,
    create_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
