CREATE TABLE logs_template (
    id INTEGER PRIMARY KEY SERIAL,
    clock DATE NOT NULL,
    category TEXT NOT NULL,
    message TEXT
);
