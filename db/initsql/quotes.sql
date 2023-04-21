CREATE TABLE IF NOT EXISTS "quotes" (
    "quote_id" SERIAL PRIMARY KEY,
    "name" VARCHAR(128) NOT NULL,
    "quote" VARCHAR(1024) NOT NULL,
    "user_id" VARCHAR(32) NOT NULL
);