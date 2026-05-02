CREATE TABLE IF NOT EXISTS places (
    id            SERIAL PRIMARY KEY,
    name_en       TEXT,
    name_pl       TEXT,
    category      TEXT NOT NULL,
    description   TEXT,
    opening_hours TEXT,
);
