CREATE TABLE users(
    id INTEGER PRIMARY KEY ASC,
    name varchar(256),
    born_date date,
    weight int,
    height int,
    activity_level int
    );
CREATE TABLE sports(
    id INTEGER PRIMARY KEY ASC,
    name varchar(128),
    moving BOOLEAN NOT NULL CHECK (moving IN (0,1))
    );
CREATE TABLE activities(
    id INTEGER PRIMARY KEY ASC,
    sport_id INTEGER,
    user_id INTEGER,
    foreign key(sport_id) references sports(id),
    foreign key(user_id) references users(id)
    );