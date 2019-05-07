CREATE TABLE users(
    id INTEGER PRIMARY KEY ASC,
    name varchar(256) UNIQUE ,
    born_date date,
    weight float,
    height int,
    activity_level int
    );
CREATE TABLE sports(
    id INTEGER PRIMARY KEY ASC,
    name varchar(128) UNIQUE NOT NULL ,
    moving BOOLEAN NOT NULL CHECK (moving IN (0,1))
    );
CREATE TABLE activities(
    id INTEGER PRIMARY KEY ASC,
    sport_id INTEGER,
    user_id INTEGER,
    time integer,
    distance integer,
    foreign key(sport_id) references sports(id),
    foreign key(user_id) references users(id)
    );