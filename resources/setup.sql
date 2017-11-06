CREATE TABLE web (
	url_id integer,
	url varchar
);

CREATE TABLE user (
	telegram_id integer,
	username varchar,
	firstname varchar,
	lastname varchar,
	language varchar,
	is_bot integer
);

CREATE TABLE web_user (
	url_id integer,
	telegram_id integer,
	last_updated datetime,
	alias varchar
);

CREATE INDEX index_web_url ON web (url);
