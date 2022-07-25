CREATE TABLE servers (
    id INTEGER PRIMARY KEY,
    respects INTEGER NOT NULL,
    main_channel_id INTEGER,
    bot_channel_id INTEGER,
    pin_channel_id INTEGER
);
