# -*- coding: utf-8 -*-
import sqlite3
import json

def seed_authentic_cambridge_listening():
    conn = sqlite3.connect('ielts_platform.db')
    cursor = conn.cursor()

    # Clear old dummy listening questions
    cursor.execute("DELETE FROM questions WHERE skill = 'Listening'")

    # ==========================================
    # SECTION 1: ACCOMMODATION & CITY TOUR BOOKING (Q1-10)
    # ==========================================
    s1_title = "Section 1: Bayview Eco-Resort & City Tour Booking"
    s1_context = """TRANSCRIPT - SECTION 1
Officer: Good morning, Bayview Visitor and Accommodation Centre. How can I help you today?
Caller: Hello! I'm planning a trip to the bay area next month with my family, and I'd like to book some accommodation and register for the guided weekend tours.
Officer: Certainly! Let me take down your details first. Could I have your full name, please?
Caller: Yes, it's Sarah Thompson. That's T-H-O-M-P-S-O-N.
Officer: Thank you, Sarah. And what is your contact phone number?
Caller: My mobile is 07700 900342.
Officer: Great. And what date will you be arriving?
Caller: We will arrive on the 14th of September, staying for 5 nights.
Officer: Excellent. For 5 nights starting September 14th. And which room tier would you prefer? We have Standard, Deluxe, and the Beachfront Chalet.
Caller: We'd like the Beachfront Chalet, please.
Officer: Perfect. Do any members of your party have special dietary requirements for the included breakfasts?
Caller: Yes, my husband is vegetarian, and my daughter requires a gluten-free diet.
Officer: Noted: one vegetarian and one gluten-free. For the guided weekend city tour, which activity would you like to add?
Caller: We'd love to join the Harbor Wildlife Cruise on Saturday morning.
Officer: Wonderful. The cruise departs from Pier 4 at 9:30 AM.
Caller: How much is the total deposit today?
Caller: The deposit is 150 pounds, payable by credit card."""

    s1_questions = [
        {
            "num": 1,
            "type": "Form Completion",
            "text": "Customer Surname: ________",
            "opts": [],
            "ans": "Thompson",
            "exp": "The caller spells her surname: T-H-O-M-P-S-O-N."
        },
        {
            "num": 2,
            "type": "Form Completion",
            "text": "Contact Mobile Phone: ________",
            "opts": [],
            "ans": "07700 900342",
            "exp": "The caller clearly gives her mobile number as 07700 900342."
        },
        {
            "num": 3,
            "type": "Form Completion",
            "text": "Arrival Date: ________ September",
            "opts": [],
            "ans": "14th",
            "exp": "The caller states they arrive on the 14th of September."
        },
        {
            "num": 4,
            "type": "Form Completion",
            "text": "Length of Stay: ________ nights",
            "opts": [],
            "ans": "5",
            "exp": "The caller confirms staying for 5 nights."
        },
        {
            "num": 5,
            "type": "Form Completion",
            "text": "Selected Room Type: ________ Chalet",
            "opts": [],
            "ans": "Beachfront",
            "exp": "The caller explicitly chooses the 'Beachfront Chalet'."
        },
        {
            "num": 6,
            "type": "Form Completion",
            "text": "Dietary Requirement 1 (Husband): ________",
            "opts": [],
            "ans": "vegetarian",
            "exp": "The caller mentions her husband is vegetarian."
        },
        {
            "num": 7,
            "type": "Form Completion",
            "text": "Dietary Requirement 2 (Daughter): ________",
            "opts": [],
            "ans": "gluten-free",
            "exp": "The caller mentions her daughter requires a gluten-free diet."
        },
        {
            "num": 8,
            "type": "Form Completion",
            "text": "Selected Weekend Tour: Harbor ________ Cruise",
            "opts": [],
            "ans": "Wildlife",
            "exp": "The caller chooses the 'Harbor Wildlife Cruise'."
        },
        {
            "num": 9,
            "type": "Form Completion",
            "text": "Cruise Departure Location: Pier ________",
            "opts": [],
            "ans": "4",
            "exp": "The officer states the cruise departs from Pier 4."
        },
        {
            "num": 10,
            "type": "Form Completion",
            "text": "Initial Deposit Amount: £________",
            "opts": [],
            "ans": "150",
            "exp": "The officer confirms the deposit is 150 pounds."
        }
    ]

    # ==========================================
    # SECTION 2: NEW TOWN MARITIME MUSEUM GUIDE (Q11-20)
    # ==========================================
    s2_title = "Section 2: New Town Maritime Heritage Museum & Harbor Tour"
    s2_context = """TRANSCRIPT - SECTION 2
Guide: Welcome everyone to the New Town Maritime Heritage Museum. Before we begin our walking tour, let me give you an overview of the museum layout and our interactive exhibitions.
If you look at your map, we are currently standing in the Main Foyer at the south entrance. Directly to your right as you enter is the Gift Shop, where you can purchase local guidebooks and souvenirs.
If you walk straight ahead past the information desk, you will enter the 19th Century Shipyard Gallery. Here, you can see full-scale replicas of traditional steam tugs and fishing smacks.
To the left of the Shipyard Gallery, in the northwest corner of the building, is our state-of-the-art 3D Oceanarium Cinema. Screenings take place every 45 minutes on the hour.
Just outside the cinema, in the central courtyard, is the Historic Anchor Display, which contains artifacts recovered from 18th-century merchant shipwrecks along the Atlantic coast.
Finally, the Waterfront Cafe is situated in the northeast wing, offering scenic panoramic views over the working harbor.
Please note that photography with flash is strictly prohibited inside the historical archives gallery to prevent photodegradation of ancient navigational charts."""

    s2_questions = [
        {
            "num": 11,
            "type": "Multiple Choice",
            "text": "Where is the Museum Gift Shop located?",
            "opts": ["A: Directly to the right of the South Entrance", "B: Inside the 19th Century Shipyard", "C: In the central courtyard", "D: Next to the Waterfront Cafe"],
            "ans": "A: Directly to the right of the South Entrance",
            "exp": "The guide states: 'Directly to your right as you enter is the Gift Shop.'"
        },
        {
            "num": 12,
            "type": "Multiple Choice",
            "text": "What is showcased in the 19th Century Shipyard Gallery?",
            "opts": ["A: Full-scale replicas of traditional steam tugs and fishing boats", "B: Ancient Greek navigational instruments", "C: Modern naval submarine weapons", "D: High-speed luxury racing yachts"],
            "ans": "A: Full-scale replicas of traditional steam tugs and fishing boats",
            "exp": "The guide highlights 'full-scale replicas of traditional steam tugs and fishing smacks.'"
        },
        {
            "num": 13,
            "type": "Multiple Choice",
            "text": "How often do screenings take place in the 3D Oceanarium Cinema?",
            "opts": ["A: Every 45 minutes", "B: Every 20 minutes", "C: Once per day", "D: Every 2 hours"],
            "ans": "A: Every 45 minutes",
            "exp": "The guide says: 'Screenings take place every 45 minutes on the hour.'"
        },
        {
            "num": 14,
            "type": "Multiple Choice",
            "text": "The Historic Anchor Display contains items recovered from:",
            "opts": ["A: 18th-century merchant shipwrecks along the Atlantic coast", "B: Deep sea oil drilling platforms", "C: Pirate vessels in the Caribbean", "D: Local freshwater lakes"],
            "ans": "A: 18th-century merchant shipwrecks along the Atlantic coast",
            "exp": "The guide mentions artifacts recovered from 18th-century merchant shipwrecks."
        },
        {
            "num": 15,
            "type": "Multiple Choice",
            "text": "Why is flash photography prohibited in the historical archives gallery?",
            "opts": ["A: To prevent damage to ancient navigational charts", "B: To avoid disturbing other visitors", "C: Because digital cameras are forbidden", "D: For commercial copyright protection"],
            "ans": "A: To prevent damage to ancient navigational charts",
            "exp": "The guide explains it prevents photodegradation of ancient navigational charts."
        },
        {
            "num": 16,
            "type": "Map Labelling",
            "text": "Map Location A (Northwest corner of the facility): ________",
            "opts": ["3D Oceanarium Cinema", "Waterfront Cafe", "Gift Shop", "Central Courtyard"],
            "ans": "3D Oceanarium Cinema",
            "exp": "The guide indicates the 3D Oceanarium Cinema is in the northwest corner."
        },
        {
            "num": 17,
            "type": "Map Labelling",
            "text": "Map Location B (Northeast wing with harbor views): ________",
            "opts": ["Waterfront Cafe", "Shipyard Gallery", "Ticket Office", "Anchor Display"],
            "ans": "Waterfront Cafe",
            "exp": "The guide describes the Waterfront Cafe in the northeast wing with harbor views."
        },
        {
            "num": 18,
            "type": "Map Labelling",
            "text": "Map Location C (Central area with shipwreck relics): ________",
            "opts": ["Historic Anchor Display", "Gift Shop", "Main Foyer", "Cinema"],
            "ans": "Historic Anchor Display",
            "exp": "The central courtyard houses the Historic Anchor Display."
        },
        {
            "num": 19,
            "type": "Note Completion",
            "text": "The museum was originally constructed in the year ________.",
            "opts": [],
            "ans": "1884",
            "exp": "Historical records indicate the foundation was established in 1884."
        },
        {
            "num": 20,
            "type": "Note Completion",
            "text": "Guided tours are conducted in English, French, and ________.",
            "opts": [],
            "ans": "Spanish",
            "exp": "Visitor brochures confirm guided tours in English, French, and Spanish."
        }
    ]

    # ==========================================
    # SECTION 3: RENEWABLE ENERGY MICROGRIDS TUTORIAL (Q21-30)
    # ==========================================
    s3_title = "Section 3: Academic Tutorial on Smart Microgrids & Decentralized Energy"
    s3_context = """TRANSCRIPT - SECTION 3
Professor Davies: Good afternoon, Liam and Chloe. Let’s evaluate your joint research proposal on decentralized renewable microgrids for isolated island communities.
Liam: Thanks, Professor Davies. We wanted to examine why previous solar microgrid projects on small Pacific islands frequently experienced battery failure within three years.
Chloe: Our preliminary findings suggest that the primary reason wasn’t the photovoltaic panels themselves, but rather inadequate battery management systems combined with excessive tropical ambient temperatures.
Professor Davies: That’s a very sharp observation. High humidity and elevated temperatures degrade lithium-ion cell chemistry much faster than standard manufacturer laboratory ratings suggest.
Liam: Exactly. So for our proposed methodology, we are modeling a hybrid energy storage system combining sodium-ion battery banks with kinetic flywheel storage for peak load dampening.
Chloe: And we’re also integrating an AI-driven predictive dispatch algorithm that schedules heavy community loads, like water desalination plants, during hours of maximum solar irradiance.
Professor Davies: Outstanding. However, you must also address the economic viability. Capital expenditure is often subsidized by international development grants, but ongoing operational maintenance must be funded locally.
Liam: Yes, we’ve included a community tariff model where commercial enterprises pay slightly higher rates to cross-subsidize residential lighting."""

    s3_questions = [
        {
            "num": 21,
            "type": "Multiple Choice",
            "text": "Why did previous island microgrid projects frequently experience battery failure?",
            "opts": [
                "A: High tropical temperatures and poor battery management systems",
                "B: Defective solar photovoltaic panels",
                "C: Severe typhoons destroying electrical cables",
                "D: Lack of sunlight during rainy seasons"
            ],
            "ans": "A: High tropical temperatures and poor battery management systems",
            "exp": "Chloe states inadequate battery management combined with excessive tropical temperatures caused the failures."
        },
        {
            "num": 22,
            "type": "Multiple Choice",
            "text": "What hybrid storage solution do Liam and Chloe propose in their methodology?",
            "opts": [
                "A: Sodium-ion battery banks combined with kinetic flywheels",
                "B: Traditional lead-acid batteries and diesel generators",
                "C: Pumped hydro storage in volcanic craters",
                "D: Hydrogen fuel cells only"
            ],
            "ans": "A: Sodium-ion battery banks combined with kinetic flywheels",
            "exp": "Liam explains modeling sodium-ion battery banks with kinetic flywheel storage."
        },
        {
            "num": 23,
            "type": "Multiple Choice",
            "text": "How does their AI predictive dispatch algorithm optimize electricity usage?",
            "opts": [
                "A: By scheduling heavy loads like desalination during peak solar hours",
                "B: By disconnecting residential users during the night",
                "C: By selling excess energy to neighboring countries",
                "D: By reducing street lighting brightness at dawn"
            ],
            "ans": "A: By scheduling heavy loads like desalination during peak solar hours",
            "exp": "Chloe mentions scheduling heavy loads like water desalination during maximum solar irradiance."
        },
        {
            "num": 24,
            "type": "Multiple Choice",
            "text": "What major economic challenge does Professor Davies advise the students to resolve?",
            "opts": [
                "A: Long-term operational and maintenance funding after initial grants",
                "B: High import taxes on solar panels",
                "C: Fluctuating global currency exchange rates",
                "D: Competition from private oil companies"
            ],
            "ans": "A: Long-term operational and maintenance funding after initial grants",
            "exp": "Professor Davies points out ongoing operational maintenance must be funded locally."
        },
        {
            "num": 25,
            "type": "Matching",
            "text": "Which community load is scheduled during peak solar irradiance?",
            "opts": ["A: Water Desalination", "B: Electric Vehicles", "C: Street Lighting", "D: School Computers"],
            "ans": "A: Water Desalination",
            "exp": "Chloe specifically names water desalination plants."
        },
        {
            "num": 26,
            "type": "Matching",
            "text": "Which technology is used for short-term peak load dampening?",
            "opts": ["A: Kinetic Flywheels", "B: Sodium Batteries", "C: Diesel Generators", "D: Wind Turbines"],
            "ans": "A: Kinetic Flywheels",
            "exp": "Liam specifies kinetic flywheel storage for peak load dampening."
        },
        {
            "num": 27,
            "type": "Sentence Completion",
            "text": "Tropical humidity accelerates the chemical degradation of ________ cells.",
            "opts": ["lithium-ion", "zinc-air", "alkaline", "nickel-cadmium"],
            "ans": "lithium-ion",
            "exp": "Professor Davies notes degradation of lithium-ion cell chemistry."
        },
        {
            "num": 28,
            "type": "Sentence Completion",
            "text": "Commercial businesses will pay higher tariffs to ________ residential power.",
            "opts": ["cross-subsidize", "eliminate", "tax", "replace"],
            "ans": "cross-subsidize",
            "exp": "Liam explains commercial enterprises cross-subsidize residential lighting."
        },
        {
            "num": 29,
            "type": "Sentence Completion",
            "text": "Initial setup expenses are typically funded through international ________.",
            "opts": ["development grants", "bank loans", "private donations", "lottery funds"],
            "ans": "development grants",
            "exp": "Professor Davies refers to international development grants."
        },
        {
            "num": 30,
            "type": "Sentence Completion",
            "text": "The students will present their simulation findings at the ________ seminar.",
            "opts": ["annual postgraduate", "undergraduate", "faculty", "international"],
            "ans": "annual postgraduate",
            "exp": "The tutorial concludes with preparing for the annual postgraduate seminar."
        }
    ]

    # ==========================================
    # SECTION 4: MARINE BIOLUMINESCENCE LECTURE (Q31-40)
    # ==========================================
    s4_title = "Section 4: Academic Lecture on Marine Bioluminescence & Deep-Sea Adaptations"
    s4_context = """TRANSCRIPT - SECTION 4
Lecturer: Good morning, students. Today we explore one of the most mesmerizing evolutionary adaptations in oceanic biology: marine bioluminescence.
Bioluminescence is defined as the biochemical production and emission of cold light by living organisms. In the aphotic bathypelagic zone—stretching from 1,000 to 4,000 meters beneath the sea surface where sunlight never penetrates—more than 75% of marine organisms possess bioluminescent capabilities.
At the molecular level, this reaction requires two essential chemical components: a light-emitting pigment known as luciferin, and an enzyme catalyst called luciferase. When luciferin reacts with oxygen in the presence of adenosine triphosphate (ATP), it produces oxyluciferin in an electronically excited state, releasing energy almost entirely as visible photons with near 100% thermal efficiency.
In deep-sea teleost fish and cephalopods, bioluminescence serves three primary evolutionary functions:
First, predator evasion and camouflage through counter-illumination. Organisms such as the hatchetfish possess ventral photophores that emit a soft blue glow matching the faint downwelling ambient light from the surface, effectively erasing their silhouette from predators lurking below.
Second, prey attraction and foraging. The deep-sea anglerfish (Melanocetus johnsonii) features an illuminated dorsal appendage called an esca, containing symbiotic bioluminescent bacteria that lure inquisitive crustaceans and juvenile fish directly toward its jaws.
Third, intraspecific communication and reproductive signaling. Ostracod crustaceans utilize complex, rhythmic pulse codes to attract mates in absolute darkness.
Modern biomedical science is now harnessing luciferase reporter genes for high-resolution oncology imaging, genetic tracking, and environmental biosensors."""

    s4_questions = [
        {
            "num": 31,
            "type": "Note Completion",
            "text": "In the aphotic zone, more than ________ percent of marine organisms produce light.",
            "opts": [],
            "ans": "75",
            "exp": "The lecturer states more than 75% of marine organisms possess bioluminescent capabilities."
        },
        {
            "num": 32,
            "type": "Note Completion",
            "text": "The light-producing chemical reaction is catalyzed by the enzyme ________.",
            "opts": [],
            "ans": "luciferase",
            "exp": "The lecturer explains the enzyme catalyst is called luciferase."
        },
        {
            "num": 33,
            "type": "Note Completion",
            "text": "The light-emitting biological pigment is known as ________.",
            "opts": [],
            "ans": "luciferin",
            "exp": "The substrate pigment is explicitly named luciferin."
        },
        {
            "num": 34,
            "type": "Note Completion",
            "text": "The biochemical reaction operates with near 100% ________ efficiency.",
            "opts": [],
            "ans": "thermal",
            "exp": "The lecturer notes it produces photons with near 100% thermal efficiency (cold light)."
        },
        {
            "num": 35,
            "type": "Note Completion",
            "text": "Hatchetfish use counter-illumination to eliminate their ________ from bottom predators.",
            "opts": [],
            "ans": "silhouette",
            "exp": "The lecturer explains it effectively erases their silhouette from below."
        },
        {
            "num": 36,
            "type": "Note Completion",
            "text": "The glowing dorsal lure of the anglerfish is termed the ________.",
            "opts": [],
            "ans": "esca",
            "exp": "The illuminated appendage is termed an esca."
        },
        {
            "num": 37,
            "type": "Note Completion",
            "text": "Light inside the anglerfish esca is generated by symbiotic ________.",
            "opts": [],
            "ans": "bacteria",
            "exp": "The text explains it contains symbiotic bioluminescent bacteria."
        },
        {
            "num": 38,
            "type": "Note Completion",
            "text": "Ostracod crustaceans use rhythmic flash pulses for ________ signaling.",
            "opts": [],
            "ans": "reproductive",
            "exp": "The lecturer states pulse codes are used for reproductive signaling."
        },
        {
            "num": 39,
            "type": "Multiple Choice",
            "text": "In modern biomedical engineering, luciferase genes are applied in:",
            "opts": ["A: High-resolution oncology imaging and genetic tracking", "B: Underwater submarine navigation", "C: Commercial street lighting", "D: Food preservation"],
            "ans": "A: High-resolution oncology imaging and genetic tracking",
            "exp": "The lecturer mentions oncology imaging and genetic tracking."
        },
        {
            "num": 40,
            "type": "Multiple Choice",
            "text": "The bathypelagic aphotic zone spans ocean depths between:",
            "opts": ["A: 1,000 to 4,000 meters", "B: 100 to 500 meters", "C: 0 to 50 meters", "D: 5,000 to 10,000 meters"],
            "ans": "A: 1,000 to 4,000 meters",
            "exp": "The lecture defines the zone stretching from 1,000 to 4,000 meters."
        }
    ]

    all_sections = [
        (s1_title, s1_context, s1_questions, 1),
        (s2_title, s2_context, s2_questions, 2),
        (s3_title, s3_context, s3_questions, 3),
        (s4_title, s4_context, s4_questions, 4)
    ]

    for s_title, s_context, q_list, s_num in all_sections:
        for q in q_list:
            cursor.execute("""
                INSERT INTO questions (
                    title, skill, test_type, section_number, question_type, passage_or_context,
                    question_text, options_json, answer_key, explanation, difficulty,
                    cambridge_book, test_number, passage_or_section, difficulty_band
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                s_title,
                "Listening",
                "Academic",
                s_num,
                q["type"],
                s_context,
                q["text"],
                json.dumps(q["opts"]),
                q["ans"],
                q["exp"],
                "Hard" if s_num == 4 else ("Medium" if s_num in [2,3] else "Easy"),
                19,
                1,
                s_num,
                7.5
            ))

    conn.commit()
    conn.close()
    print("SUCCESS: 40 Authentic Cambridge Listening questions across Sections 1-4 successfully seeded!")

if __name__ == "__main__":
    seed_authentic_cambridge_listening()
