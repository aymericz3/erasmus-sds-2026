CREATE TABLE IF NOT EXISTS places (
    id            SERIAL PRIMARY KEY,
    name_en       TEXT,
    name_pl       TEXT,
    category      TEXT NOT NULL,
    description   TEXT,
    opening_hours TEXT,
    duration      TEXT,
    price_range   TEXT,
    image_url     TEXT,
    latitude      FLOAT,
    longitude     FLOAT,
    -- Enrichment fields (OpenStreetMap + Wikipedia)
    address           TEXT,
    website           TEXT,
    osm_id            TEXT,
    wikipedia_title   TEXT,
    image_attribution TEXT,
    source            TEXT
);

-- Idempotent columns for databases created before enrichment was added.
ALTER TABLE places ADD COLUMN IF NOT EXISTS address           TEXT;
ALTER TABLE places ADD COLUMN IF NOT EXISTS website           TEXT;
ALTER TABLE places ADD COLUMN IF NOT EXISTS osm_id            TEXT;
ALTER TABLE places ADD COLUMN IF NOT EXISTS wikipedia_title   TEXT;
ALTER TABLE places ADD COLUMN IF NOT EXISTS image_attribution TEXT;
ALTER TABLE places ADD COLUMN IF NOT EXISTS source            TEXT;
