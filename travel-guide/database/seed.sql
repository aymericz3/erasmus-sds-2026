INSERT INTO places (name_en, name_pl, category, description, opening_hours) VALUES
-- landmark
('Old Market Square',    'Stary Rynek',             'landmark', 'Central historic square with colorful buildings and Renaissance town hall.', '24/7'),
('Poznan Town Hall',     'Ratusz Poznanski',        'landmark', 'Renaissance building famous for mechanical goats at noon.', '10:00-17:00'),
('Imperial Castle',      'Zamek Cesarski',          'landmark', 'Historic imperial residence now used as a cultural center.', '10:00-18:00'),
('Poznan Cathedral',     'Katedra Poznanska',       'landmark', 'One of Poland oldest churches, located on Cathedral Island.', '10:00-17:00'),

-- sport
('INEA Stadium',         'INEA Stadion',            'sport', 'Major football stadium, home of Lech Poznan.', 'Event-based / daytime tours'),
(NULL,                   'Termy Maltanskie',        'sport', 'Large aqua park with pools, saunas, and sports facilities.', '06:00-22:00'),
('Malta Ski',            NULL,                      'sport', 'Year-round ski slope and sports complex near Malta Lake.', '10:00-22:00'),

-- culture
('Poznan Gate',          'Brama Poznania',          'culture', 'Interactive heritage center explaining the origins of Poland.', 'Tue-Fri 09:00-18:00, Sat-Sun 10:00-19:00'),
(NULL,                   'Rezerwat Archeologiczny Genius Loci', 'culture', 'Archaeological reserve showing 10th-century Piast fortifications.', 'Tue-Thu 10:00-16:00, Fri-Sat 10:00-18:00, Sun 10:00-15:00'),
('Enigma Cipher Center', NULL,                      'culture', 'Museum about WWII codebreakers and cryptography.', '10:00-18:00'),

-- art
('National Museum',      'Muzeum Narodowe',         'art', 'Major museum with Polish and international art collections.', 'Tue-Wed 10:00-16:00, Thu 10:00-18:00, Fri 10:00-20:00, Sat-Sun 10:00-17:00'),
('Museum of Applied Arts', 'Muzeum Sztuk Uzytkowych', 'art', 'Located in the Royal Castle, showcasing decorative arts.', 'Tue-Wed 10:00-16:00, Thu 10:00-18:00, Fri 10:00-20:00, Sat-Sun 10:00-17:00'),
('Arsenal Gallery',      'Galeria Arsenal',         'art', 'Contemporary art gallery in the Old Market Square.', '11:00-18:00'),
('Srodka Mural',         NULL,                      'art', 'Famous 3D mural representing historical Poznan life.', '24/7'),

-- outdoor
('Citadel Park',         'Park Cytadela',           'outdoor', 'Largest park in Poznan with monuments and walking paths.', '24/7'),
('Malta Lake',           'Jezioro Maltanskie',      'outdoor', 'Recreational lake with walking, cycling, and sports activities.', '24/7'),
(NULL,                   'Park Solacki',            'outdoor', 'Scenic park with ponds and historic surroundings.', '24/7'),
('Warta River Boulevards', NULL,                    'outdoor', 'Riverside walking and leisure area.', '24/7'),

-- family
('Poznan Palm House',    'Palmiarnia Poznanska',    'family', 'Large greenhouse with exotic plants and aquarium.', '09:00-17:00'),
('New Zoo',              'Nowe Zoo',                'family', 'Large zoo with many animal species and green areas.', '09:00-18:00'),
('Old Zoo',              'Stare Zoo',               'family', 'Smaller zoo and park in the city center.', '09:00-19:00'),

-- hotel
('Sheraton Poznan Hotel', NULL,                     'hotel', 'Modern hotel near the city center and trade fair.', '24/7'),
('Hotel Blow Up Hall 5050', NULL,                   'hotel', 'Boutique luxury hotel with artistic concept.', '24/7'),

-- food
('Pyra Bar',             NULL,                      'food', 'Traditional restaurant specializing in potato dishes.', '11:00-21:00'),
('Ratuszova Restaurant', NULL,                      'food', 'Traditional Polish cuisine in a historic building.', '12:00-22:00');
