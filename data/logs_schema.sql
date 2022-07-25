CREATE TABLE logs_template (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clock DATE NOT NULL,
    severity TEXT NOT NULL,
    category TEXT NOT NULL,
    message TEXT
);
