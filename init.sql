create table if not exists blog_user
(
	id serial
		constraint blog_user_pk
			primary key,
	login varchar not null,
	password varchar not null
);

create unique index blog_user_login_uindex
	on blog_user (login);

create table if not exists post
(
	id serial
		constraint post_pk
			primary key,
	content text not null,
	post_date date not null,
	is_presented bool not null,
	author int not null
		constraint post_blog_user_id_fk
			references blog_user (id)
				on delete cascade
);
