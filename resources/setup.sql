CREATE TABLE web (
	url_id integer PRIMARY KEY AUTOINCREMENT,
	url varchar NOT NULL UNIQUE
);

CREATE TABLE user (
	telegram_id integer PRIMARY KEY NOT NULL,
	username varchar NOT NULL,
	firstname varchar NOT NULL,
	lastname varchar NOT NULL,
	language varchar,
	is_bot integer
);

CREATE TABLE web_user (
	url_id integer NOT NULL,
	telegram_id integer NOT NULL,
	alias varchar NOT NULL,
	PRIMARY KEY ( url_id, telegram_id)
);

CREATE INDEX index_web_url ON web (url);
