CREATE TABLE IF NOT EXISTS "known" (
    "name" VARCHAR(64) NOT NULL,
    "iid" VARCHAR(128) NOT NULL,
    "source" VARCHAR(32),
    PRIMARY KEY ("name","iid")
);