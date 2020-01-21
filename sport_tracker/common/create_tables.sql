CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY ASC,
    name varchar(256) UNIQUE ,
    born_date date,
    weight float,
    height int,
    gender INT NOT NULL CHECK (gender in (0,1)),
    activity_level int
    );
CREATE TABLE IF NOT EXISTS sports(
    id INTEGER PRIMARY KEY ASC,
    name varchar(128) UNIQUE NOT NULL ,
    moving BOOLEAN NOT NULL CHECK (moving IN (0,1))
    );
CREATE TABLE IF NOT EXISTS activities(
    id INTEGER PRIMARY KEY ASC,
    sport_id INTEGER,
    user_id INTEGER,
    time integer,
    distance integer,
    foreign key(sport_id) references sports(id),
    foreign key(user_id) references users(id)
    );
CREATE TABLE IF NOT EXISTS sports_extra_columns(
    id INTEGER PRIMARY KEY ASC,
    sport_id INTEGER,
    name varchar(128),
    value varchar(128),
    type varchar(128),
    foreign key(sport_id) references sports(id)
);