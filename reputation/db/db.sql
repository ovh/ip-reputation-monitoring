DROP TABLE IF EXISTS spamhaus;

CREATE TABLE spamhaus (
    active BOOLEAN NOT NULL DEFAULT TRUE,
    sbl_number INTEGER PRIMARY KEY,
    first_seen TIMESTAMP NOT NULL DEFAULT statement_timestamp(),
    last_seen TIMESTAMP NOT NULL DEFAULT statement_timestamp(),
    cidr CIDR NOT NULL
);
CREATE INDEX index_active ON spamhaus (active);