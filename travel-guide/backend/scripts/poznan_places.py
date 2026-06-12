"""
Seed data: places to visit in Poznań, Poland.

Each entry has:
    - name:        display name (English + Polish where useful)
    - category:    one of CATEGORIES
    - description: one-line blurb for the planner UI

Notes on freshness:
    - landmark / culture / art / outdoor / family / sport entries are stable.
    - food and hotel entries change the most (rebrands, closures); these were
      checked against 2025-2026 listings but verify against a live source before
      shipping. Some entries can plausibly fit more than one category — a single
      best-fit category was chosen to match your flat schema, re-tag as needed.
"""

CATEGORIES = ["landmark", "sport", "culture", "art", "outdoor", "family", "hotel", "food"]

PLACES = [
    # ---------------------------- LANDMARK ----------------------------
    {"name": "Old Market Square (Stary Rynek)", "category": "landmark",
     "description": "The colourful Renaissance heart of the city, ringed by merchant houses and cafes."},
    {"name": "Poznań Town Hall (Ratusz)", "category": "landmark",
     "description": "Renaissance town hall; the mechanical billy goats butt heads daily at noon."},
    {"name": "Royal Castle (Zamek Królewski / Przemysł Castle)", "category": "landmark",
     "description": "Reconstructed castle on Przemysł Hill housing the Museum of Applied Arts."},
    {"name": "Imperial Castle (Zamek Cesarski)", "category": "landmark",
     "description": "Monumental early-20th-c. residence built for Kaiser Wilhelm II, now a culture centre."},
    {"name": "Archcathedral Basilica of St. Peter and St. Paul", "category": "landmark",
     "description": "Poland's oldest cathedral, on Cathedral Island, with the Golden Chapel of the first kings."},
    {"name": "Ostrów Tumski (Cathedral Island)", "category": "landmark",
     "description": "The cradle of the Polish state, a quiet island of churches and red brick."},
    {"name": "Poznań Parish Church (Fara)", "category": "landmark",
     "description": "Exuberant pink-and-cream Baroque church with regular free organ recitals."},
    {"name": "Działyński Palace", "category": "landmark",
     "description": "Late-Baroque palace on the square hosting concerts and exhibitions."},
    {"name": "Górka Palace", "category": "landmark",
     "description": "Renaissance magnate residence, now home to the Archaeological Museum."},
    {"name": "Merchant Houses (Domki Budnicze)", "category": "landmark",
     "description": "Row of slim, brightly painted former stallholders' houses on the square."},
    {"name": "Bamberka Fountain", "category": "landmark",
     "description": "Beloved statue of a Bamberg settler woman, a popular meeting point."},
    {"name": "Church of St. Adalbert (Kościół św. Wojciecha)", "category": "landmark",
     "description": "Hilltop Gothic church with a crypt of notable Poles in its 'Skałka'."},
    {"name": "Collegium Minus (Adam Mickiewicz University)", "category": "landmark",
     "description": "Neo-Renaissance university building anchoring the Imperial District."},
    {"name": "Okrąglak", "category": "landmark",
     "description": "Iconic cylindrical modernist department store by Marek Leykam."},
    {"name": "Monument to the Victims of June 1956", "category": "landmark",
     "description": "Two towering bound crosses commemorating the Poznań June uprising."},
    {"name": "Adam Mickiewicz Monument", "category": "landmark",
     "description": "Statue of the national poet on the square that bears his name."},
    {"name": "Imperial District (Dzielnica Cesarska) / Św. Marcin", "category": "landmark",
     "description": "Grand boulevard of early-1900s German imperial architecture."},
    {"name": "Stary Marych Monument", "category": "landmark",
     "description": "Bronze of the folkloric Poznań everyman with his bicycle."},

    # ---------------------------- CULTURE ----------------------------
    {"name": "Croissant Museum (Rogalowe Muzeum Poznania)", "category": "culture",
     "description": "Hands-on, comedic show about the city's St. Martin's croissant."},
    {"name": "Enigma Cipher Centre (Centrum Szyfrów Enigma)", "category": "culture",
     "description": "Interactive museum honouring the Poznań mathematicians who cracked Enigma."},
    {"name": "Porta Posnania / Brama Poznania (ICHOT)", "category": "culture",
     "description": "Modern interactive heritage centre telling the story of Ostrów Tumski."},
    {"name": "Archaeological Museum (Muzeum Archeologiczne)", "category": "culture",
     "description": "Regional prehistory plus a strong ancient-Egypt collection in Górka Palace."},
    {"name": "Museum of Musical Instruments", "category": "culture",
     "description": "One of Europe's richest instrument collections, on the Old Market Square."},
    {"name": "Greater Poland Military Museum", "category": "culture",
     "description": "Arms, armour and uniforms spanning centuries of regional history."},
    {"name": "Greater Poland Uprising Museum (1918-1919)", "category": "culture",
     "description": "Devoted to the only fully successful Polish uprising."},
    {"name": "Bambrzy Museum (Muzeum Bambrów Poznańskich)", "category": "culture",
     "description": "Story of the German Bamberg settlers who shaped local culture."},
    {"name": "Henryk Sienkiewicz Literary Museum", "category": "culture",
     "description": "Memorabilia of the Nobel-winning author in a townhouse setting."},
    {"name": "Grand Theatre / Opera (Teatr Wielki im. Moniuszki)", "category": "culture",
     "description": "Neoclassical opera house topped by a winged Pegasus."},
    {"name": "Teatr Polski", "category": "culture",
     "description": "Historic Polish-language repertory theatre founded in the 19th c."},
    {"name": "Teatr Nowy", "category": "culture",
     "description": "Leading contemporary drama stage with an adventurous programme."},
    {"name": "Animation Theatre (Teatr Animacji)", "category": "culture",
     "description": "Puppet and object theatre for children and adults."},
    {"name": "Poznań Philharmonic (Filharmonia Poznańska)", "category": "culture",
     "description": "Symphonic concerts, often in the university's grand Aula."},
    {"name": "Castle Culture Centre (Centrum Kultury Zamek)", "category": "culture",
     "description": "Sprawling arts venue inside the Imperial Castle: film, exhibitions, festivals."},
    {"name": "Museum of Applied Arts (Muzeum Sztuk Użytkowych)", "category": "culture",
     "description": "Design, craft and decorative arts within the Royal Castle."},

    # ------------------------------ ART ------------------------------
    {"name": "National Museum in Poznań (Muzeum Narodowe)", "category": "art",
     "description": "The city's flagship fine-art gallery: Polish and European masters."},
    {"name": "Stary Browar Art Stations", "category": "art",
     "description": "Contemporary art foundation inside an award-winning former brewery."},
    {"name": "Arsenał Municipal Gallery (Galeria Miejska Arsenał)", "category": "art",
     "description": "Long-running contemporary gallery on the Old Market Square."},
    {"name": "'Unrecognized' (Nierozpoznani) by Abakanowicz", "category": "art",
     "description": "112 headless cast-iron figures striding across Cytadela Park."},
    {"name": "Śródka Mural", "category": "art",
     "description": "Vast 3D trompe-l'œil mural reviving the old Śródka quarter."},
    {"name": "Galeria Ego", "category": "art",
     "description": "Commercial gallery showcasing modern Polish painting."},
    {"name": "PIX.HOUSE", "category": "art",
     "description": "Photography gallery and bookshop in the Łazarz district."},
    {"name": "Concordia Design", "category": "art",
     "description": "Design hub with exhibitions, studios and a cafe in a restored printworks."},
    {"name": "Galeria u Jezuitów", "category": "art",
     "description": "Intimate gallery in a former Jesuit college near the parish church."},
    {"name": "Rozbrat", "category": "art",
     "description": "Long-standing alternative/squat space for grassroots art and events."},

    # ---------------------------- OUTDOOR ----------------------------
    {"name": "Lake Malta (Jezioro Maltańskie)", "category": "outdoor",
     "description": "Artificial lake with promenades, a regatta course and year-round activity."},
    {"name": "Cytadela Park (Park Cytadela)", "category": "outdoor",
     "description": "The city's largest park on a former fortress, with sculptures and museums."},
    {"name": "Wilson Park (Park Wilsona)", "category": "outdoor",
     "description": "Elegant landscaped park surrounding the Palm House."},
    {"name": "Sołacki Park", "category": "outdoor",
     "description": "Romantic Art Nouveau-era park with ponds in leafy Sołacz."},
    {"name": "Lake Rusałka (Jezioro Rusałka)", "category": "outdoor",
     "description": "Forest-fringed lake with a beach and walking trails."},
    {"name": "Lake Strzeszyńskie (Jezioro Strzeszyńskie)", "category": "outdoor",
     "description": "Clean swimming lake popular for summer bathing and cycling."},
    {"name": "Lake Kierskie (Jezioro Kierskie)", "category": "outdoor",
     "description": "Large lake on the city edge for sailing, windsurfing and swimming."},
    {"name": "Botanical Garden (Ogród Botaniczny UAM)", "category": "outdoor",
     "description": "University garden with themed collections and an alpine section."},
    {"name": "Wartostrada", "category": "outdoor",
     "description": "Riverside walking and cycling route along both banks of the Warta."},
    {"name": "Morasko Meteorite Reserve", "category": "outdoor",
     "description": "Forest reserve dotted with craters from a prehistoric meteorite fall."},
    {"name": "Dębina / Łęgi Dębińskie", "category": "outdoor",
     "description": "Riverside floodplain forest for walks and birdwatching south of centre."},
    {"name": "Kórnik Arboretum & Castle", "category": "outdoor",
     "description": "Day trip: neo-Gothic island castle and Poland's oldest arboretum."},
    {"name": "Rogalin Palace & Oaks", "category": "outdoor",
     "description": "Day trip: Baroque palace, gallery and a grove of ancient oaks."},

    # ---------------------------- FAMILY ----------------------------
    {"name": "New Zoo (Nowe Zoo)", "category": "family",
     "description": "Spacious woodland zoo by Lake Malta, reachable by the Maltanka train."},
    {"name": "Old Zoo (Stare Zoo)", "category": "family",
     "description": "Charming 19th-c. zoo-park in the city centre, free to enter."},
    {"name": "Maltanka Park Railway", "category": "family",
     "description": "Narrow-gauge heritage train running along the lake to the New Zoo."},
    {"name": "Malta Thermal Baths (Termy Maltańskie)", "category": "family",
     "description": "Big indoor/outdoor water park with thermal pools and slides."},
    {"name": "Palm House (Palmiarnia Poznańska)", "category": "family",
     "description": "Historic glasshouse with tropical plants, fish and a butterfly section."},
    {"name": "Malta Ski", "category": "family",
     "description": "Year-round dry ski slope, summer toboggan run and alpine coaster."},
    {"name": "Genius Loci Archaeological Reserve", "category": "family",
     "description": "Underground glimpse of Poznań's earliest medieval ramparts."},
    {"name": "Pyrland Trampoline Park", "category": "family",
     "description": "Indoor trampoline and adventure park for rainy-day energy."},
    {"name": "Fort VII Museum", "category": "family",
     "description": "Sobering WWII memorial site in a Prussian fort (older children/teens)."},
    {"name": "Adventure Rope Park (Park Linowy Malta)", "category": "family",
     "description": "Treetop rope courses beside Lake Malta."},

    # ----------------------------- SPORT -----------------------------
    {"name": "Enea Stadion (Stadion Poznań)", "category": "sport",
     "description": "Home of football club Lech Poznań; stadium tours available."},
    {"name": "Malta Regatta Course (Tor Regatowy Malta)", "category": "sport",
     "description": "World-class rowing and canoeing course hosting international events."},
    {"name": "Malta Ski Slope", "category": "sport",
     "description": "Skiing, snowboarding and tubing on an artificial slope by the lake."},
    {"name": "Arena Poznań", "category": "sport",
     "description": "Indoor sports and events hall for handball, volleyball and concerts."},
    {"name": "Tor Poznań", "category": "sport",
     "description": "Motorsport racing circuit hosting car and motorcycle events."},
    {"name": "Poznań Golf Club", "category": "sport",
     "description": "18-hole course on the outskirts for a relaxed round."},
    {"name": "Wola Hippodrome (Hipodrom Wola)", "category": "sport",
     "description": "Historic racecourse for horse racing and equestrian events."},
    {"name": "Chwiałka Swimming Pool", "category": "sport",
     "description": "Central municipal pool complex for lap swimming."},

    # ----------------------------- HOTEL -----------------------------
    {"name": "PURO Hotel Poznań Stare Miasto", "category": "hotel",
     "description": "Design-led 4-star a short walk from the Old Market Square."},
    {"name": "Sheraton Poznań Hotel", "category": "hotel",
     "description": "Upscale international chain near the Old Brewery and trade fairs."},
    {"name": "Andersia Hotel & Spa (Radisson Individuals)", "category": "hotel",
     "description": "Modern 4-star with spa on Andersia Square in the business district."},
    {"name": "Brovaria Hotel", "category": "hotel",
     "description": "Boutique rooms above a brewery-restaurant right on the square."},
    {"name": "Blow Up Hall 5050", "category": "hotel",
     "description": "Avant-garde art-hotel inside the Stary Browar complex."},
    {"name": "Mercure Poznań Centrum", "category": "hotel",
     "description": "Reliable central high-rise, home of a popular St. Martin's croissant cafe."},
    {"name": "City Park Hotel & Residence", "category": "hotel",
     "description": "Elegant 5-star in the leafy City Park complex west of centre."},
    {"name": "Don Prestige Residence", "category": "hotel",
     "description": "Apartment-style suites near the Old Town, good for longer stays."},
    {"name": "Hotel Kolegiacki", "category": "hotel",
     "description": "Quiet boutique hotel steps from the parish church and square."},
    {"name": "City Solei Boutique Hotel", "category": "hotel",
     "description": "Individually themed rooms in the riverside Chwaliszewo quarter."},
    {"name": "Hampton by Hilton Poznań Old Town", "category": "hotel",
     "description": "Comfortable mid-range option with free breakfast near the square."},
    {"name": "Hotel Bazar (historic)", "category": "hotel",
     "description": "Landmark 19th-c. hotel and meeting place of Polish patriots."},

    # ------------------------------ FOOD ------------------------------
    {"name": "MUGA", "category": "food",
     "description": "Poznań's Michelin-starred restaurant; creative tasting menus."},
    {"name": "Brovaria", "category": "food",
     "description": "Brewpub-restaurant on the square serving house lagers and Polish fare."},
    {"name": "Hyćka", "category": "food",
     "description": "Showcase of regional Wielkopolska cooking and the local dialect."},
    {"name": "Bamberka", "category": "food",
     "description": "Regional Greater Poland dishes on the Old Market Square."},
    {"name": "Ratuszova", "category": "food",
     "description": "Polish classics with cellar dining beneath the town hall."},
    {"name": "Wiejskie Jadło", "category": "food",
     "description": "Hearty traditional Polish food in a rustic setting off the square."},
    {"name": "Pyra Bar", "category": "food",
     "description": "Fun, affordable spot built entirely around the potato (pyra)."},
    {"name": "Concordia Taste", "category": "food",
     "description": "Modern Polish fine dining in the Concordia Design building."},
    {"name": "Marino Bistro", "category": "food",
     "description": "Polish-Italian family bistro in Jeżyce, Michelin-recommended."},
    {"name": "Weranda Caffe", "category": "food",
     "description": "Stylish brunch and breakfast favourite near the centre."},
    {"name": "MOMO", "category": "food",
     "description": "Fresh seafood and international plates brought from the coast."},
    {"name": "Food Fyrtel", "category": "food",
     "description": "Indoor food hall with many vendors, ideal for indecisive groups."},
    {"name": "Whisky in the Jar", "category": "food",
     "description": "American-style smoked BBQ and ribs, a local crowd-pleaser."},
    {"name": "Ed Red Poznań", "category": "food",
     "description": "Steakhouse focused on dry-aged Polish beef."},
]


def by_category(category):
    """Return all places in a given category."""
    return [p for p in PLACES if p["category"] == category]


def category_counts():
    """Return a dict of category -> number of places."""
    return {c: len(by_category(c)) for c in CATEGORIES}


if __name__ == "__main__":
    print(f"Total places: {len(PLACES)}")
    for cat, n in category_counts().items():
        print(f"  {cat:<10} {n}")
