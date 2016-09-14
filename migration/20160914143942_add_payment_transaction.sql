-- add_payment_transaction
-- COLUMNS = ['id', 'uid', 'type', 'out_trade_no', 'state', 'create_at', 'update_at']

CREATE TABLE fc_payment_transaction (
    id            BIGSERIAL PRIMARY KEY,
    uid           bigint NOT NULL,
    type         smallint not null default 0,
    out_trade_no varchar not null,
    state        smallint not null default 0,
    create_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
