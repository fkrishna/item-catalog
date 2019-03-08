CREATE TABLE categories (
	id serial PRIMARY KEY NOT NULL,
 	title varchar(255) NOT NULL
);

CREATE TABLE items (
	id serial PRIMARY KEY NOT NULL,
 	name varchar(255) NOT NULL,
 	description text,
 	post_date timestamp NOT NULL,
 	category_id integer NOT NULL REFERENCES categories(id)
);

CREATE TABLE users (
	id serial PRIMARY KEY NOT NULL,
 	username varchar(255) NOT NULL,
 	email text
);