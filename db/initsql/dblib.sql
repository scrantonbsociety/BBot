CREATE TABLE IF NOT EXISTS "users" (
	"id" VARCHAR(32) NOT NULL,
	"iid" VARCHAR(64) NULL DEFAULT NULL,
	PRIMARY KEY ("id")
);