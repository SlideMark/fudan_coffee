-- add_user
CREATE TABLE fc_user (
    id            BIGSERIAL PRIMARY KEY,
    name          varchar,
    gender        smallint not null default 0,
    province      varchar,
    city          varchar,
    avatar        varchar,
    openid    varchar NOT NULL,
    unionid    varchar,
    access_token varchar,
    session_data  varchar not null,
    phone       varchar,
    state      smallint not null default 0,
    create_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
