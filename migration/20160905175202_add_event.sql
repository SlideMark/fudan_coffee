-- add_event
CREATE TABLE fc_event (
    id            BIGSERIAL PRIMARY KEY,
    creator       bigint not null,
    state         smallint not null default 0,
    fee          integer not null default 0,
    user_limit   integer not null default 0,
    poster_url   varchar,
    description  varchar not null,
    open_at      TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    close_at     TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    memo         varchar,
    create_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
