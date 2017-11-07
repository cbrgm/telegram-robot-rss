CREATE TABLE web (
	url varchar PRIMARY KEY NOT NULL UNIQUE,
	last_updated timestamp
);

CREATE TABLE user (
	telegram_id integer PRIMARY KEY NOT NULL,
	username varchar NOT NULL,
	firstname varchar NOT NULL,
	lastname varchar NOT NULL,
	language varchar,
	is_bot integer,
	is_active
);

CREATE TABLE web_user (
	url varchar NOT NULL,
	telegram_id integer NOT NULL,
	alias varchar NOT NULL,
	PRIMARY KEY (url, telegram_id),
	FOREIGN KEY(url) REFERENCES web(url),
	FOREIGN KEY(telegram_id) REFERENCES user(telegram_id)
);
