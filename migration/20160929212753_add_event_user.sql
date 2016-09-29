-- add_event_user
CREATE TABLE fc_user_event (
    id            BIGSERIAL PRIMARY KEY,
    uid           integer NOT NULL,
    event_id      integer NOT NULL,
    state        smallint  not null default 0,
    create_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_at   TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

create unique index fc_user_event_uid_evid on fc_user_event(uid, event_id)