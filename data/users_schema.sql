CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    credit INTEGER NOT NULL,
    coins INTEGER NOT NULL,
    prob INTEGER NOT NULL,
    muted BOOL NOT NULL,
    admin BOOL NOT NULL
);
