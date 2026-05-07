INSERT INTO places (name_en, name_pl, category, description, opening_hours, duration, price_range, image_url, latitude, longitude) VALUES
-- landmark
('Old Market Square',    'Stary Rynek',                        'landmark', 'Central historic square with colorful buildings and Renaissance town hall.',             '24/7',                                                          '1h',      'free', '/images/old-market-square.jpg',  52.4082, 16.9335),
('Poznan Town Hall',     'Ratusz Poznanski',                   'landmark', 'Renaissance building famous for its mechanical goats appearing at noon.',                '10:00-17:00',                                                   '45 min',  '€',    '/images/poznan-town-hall.jpg',   52.4083, 16.9336),
('Imperial Castle',      'Zamek Cesarski',                     'landmark', 'Late 19th-century imperial residence now used as a cultural and concert center.',       '10:00-18:00',                                                   '1h',      'free', '/images/imperial-castle.jpg',    52.4094, 16.9219),
('Poznan Cathedral',     'Katedra Poznanska',                  'landmark', 'One of Poland''s oldest churches, located on Cathedral Island (Ostrów Tumski).',        '09:00-17:00',                                                   '45 min',  'free', '/images/poznan-cathedral.jpg',   52.4092, 16.9478),

-- sport
('INEA Stadium',         'INEA Stadion',                       'sport',    'Major football stadium, home of Lech Poznań. Guided tours available.',                  'Match days / tours Sat-Sun 10:00-14:00',                        '1h 30min','€',    '/images/inea-stadium.jpg',       52.3900, 16.8433),
(NULL,                   'Termy Maltanskie',                   'sport',    'Large aqua park with indoor pools, saunas, water slides, and fitness facilities.',      'Mon-Fri 06:00-22:00, Sat-Sun 08:00-22:00',                      '2h',      '€€',   '/images/termy-maltanskie.jpg',   52.4026, 16.9806),
('Malta Ski',            NULL,                                 'sport',    'Year-round ski and snowboard slope with equipment rental, next to Malta Lake.',         'Mon-Fri 10:00-21:00, Sat-Sun 09:00-21:00',                      '2h',      '€€',   '/images/malta-ski.jpg',          52.3971, 16.9782),

-- culture
('Poznan Gate',          'Brama Poznania',                     'culture',  'Award-winning interactive heritage center explaining the origins of the Polish state.', 'Tue-Fri 09:00-18:00, Sat-Sun 10:00-19:00',                      '1h 30min','€€',   '/images/brama-poznania.jpg',     52.4085, 16.9471),
(NULL,                   'Rezerwat Archeologiczny Genius Loci','culture',  'Archaeological reserve on Ostrów Tumski showing 10th-century Piast fortifications.',   'Tue-Thu 10:00-16:00, Fri-Sat 10:00-18:00, Sun 10:00-15:00',     '1h',      '€',    '/images/genius-loci.jpg',        52.4083, 16.9468),
('Enigma Cipher Center', NULL,                                 'culture',  'Interactive museum dedicated to WWII Polish codebreakers and the Enigma machine.',      'Tue-Sun 10:00-18:00',                                           '1h 30min','€€',   '/images/enigma-center.jpg',      52.4070, 16.9310),

-- art
('National Museum',      'Muzeum Narodowe',                    'art',      'Major museum housing Polish and European paintings, sculptures, and decorative arts.',  'Tue-Wed 10:00-16:00, Thu 10:00-18:00, Fri 10:00-20:00, Sat-Sun 10:00-17:00', '2h', '€€', '/images/national-museum.jpg',   52.4077, 16.9264),
('Museum of Applied Arts','Muzeum Sztuk Uzytkowych',           'art',      'Located in the Royal Castle, showcasing furniture, glassware, and decorative arts.',   'Tue-Wed 10:00-16:00, Thu 10:00-18:00, Fri 10:00-20:00, Sat-Sun 10:00-17:00', '1h 30min', '€€', '/images/museum-applied-arts.jpg', 52.4077, 16.9265),
('Arsenal Gallery',      'Galeria Arsenal',                    'art',      'Contemporary art gallery housed in a former arsenal building on the Old Market Square.','Tue-Sun 11:00-18:00',                                           '1h',      'free', '/images/arsenal-gallery.jpg',    52.4084, 16.9339),
('Srodka Mural',         NULL,                                 'art',      'Iconic 3D trompe-l''oeil mural in the Śródka district depicting historic Poznań.',     '24/7',                                                          '20 min',  'free', '/images/srodka-mural.jpg',       52.4078, 16.9472),

-- outdoor
('Citadel Park',         'Park Cytadela',                      'outdoor',  'Largest park in Poznań, built on a 19th-century fortress with monuments and trails.',  '24/7',                                                          '1h 30min','free', '/images/citadel-park.jpg',       52.4212, 16.9320),
('Malta Lake',           'Jezioro Maltanskie',                 'outdoor',  'Artificial recreational lake with a regatta course, cycle paths, and beaches.',        '24/7',                                                          '2h',      'free', '/images/malta-lake.jpg',         52.3990, 16.9820),
(NULL,                   'Park Solacki',                       'outdoor',  'Scenic 19th-century English-style park with ponds, bridges, and shaded walkways.',     '24/7',                                                          '1h',      'free', '/images/park-solacki.jpg',       52.4216, 16.8937),
('Warta River Boulevards',NULL,                                'outdoor',  'Renovated riverside promenades ideal for walks, cycling, and relaxing by the water.',  '24/7',                                                          '1h',      'free', '/images/warta-boulevards.jpg',   52.4115, 16.9400),

-- family
('Poznan Palm House',    'Palmiarnia Poznanska',               'family',   'One of Europe''s largest palm houses with tropical plants, butterflies, and aquarium.', 'Tue-Fri 09:00-17:00, Sat-Sun 10:00-18:00',                      '1h 30min','€',    '/images/palmiarnia.jpg',         52.4007, 16.9849),
('New Zoo',              'Nowe Zoo',                           'family',   'Large modern zoo with over 200 species set in a forested area on the edge of the city.','Apr-Sep 09:00-18:00, Oct-Mar 09:00-16:00',                     '3h',      '€€',   '/images/new-zoo.jpg',            52.3862, 16.9038),
('Old Zoo',              'Stare Zoo',                          'family',   'Historic zoo and green park in the city center, popular with families and joggers.',   '09:00-19:00',                                                   '1h 30min','€',    '/images/old-zoo.jpg',            52.4007, 16.9217),

-- hotel
('Sheraton Poznan Hotel', NULL,                                'hotel',    'Four-star hotel adjacent to the Poznań International Fair and close to the city center.','24/7',                                                       NULL,      '€€€',  '/images/sheraton-poznan.jpg',    52.3905, 16.8599),
('Hotel Blow Up Hall 5050',NULL,                               'hotel',    'Boutique design hotel inside a historic 19th-century building with curated artworks.',  '24/7',                                                          NULL,      '€€€',  '/images/blow-up-hall.jpg',       52.4042, 16.9265),

-- food
('Pyra Bar',             NULL,                                 'food',     'Casual restaurant celebrating Poznań''s pyra (potato) tradition with hearty local dishes.','Mon-Sat 11:00-21:00, Sun 12:00-20:00',                     '1h',      '€',    '/images/pyra-bar.jpg',           52.4075, 16.9316),
('Ratuszova Restaurant', NULL,                                 'food',     'Traditional Polish cuisine served in a historic building steps from the town hall.',    'Mon-Sun 12:00-22:00',                                           '1h 30min','€€',   '/images/ratuszova.jpg',          52.4081, 16.9337);
