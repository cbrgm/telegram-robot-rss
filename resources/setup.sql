CREATE TABLE web (
	url varchar PRIMARY KEY NOT NULL UNIQUE,
	last_updated timestamp
);

CREATE TABLE user (
	telegram_id integer PRIMARY KEY NOT NULL UNIQUE,
	username varchar,
	firstname varchar NOT NULL,
	lastname varchar,
	language varchar,
	is_bot integer NOT NULL,
	is_active integer NOT NULL
);

CREATE TABLE web_user (
	url varchar NOT NULL,
	telegram_id integer NOT NULL,
	alias varchar NOT NULL,
	FOREIGN KEY(url) REFERENCES web(url),
	FOREIGN KEY(telegram_id) REFERENCES user(telegram_id)
);
