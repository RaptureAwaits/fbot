CREATE TABLE pins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL,
    pinned_by_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    score INTEGER NOT NULL
);
