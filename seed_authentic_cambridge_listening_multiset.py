# -*- coding: utf-8 -*-
import sqlite3
import json
import random

def insert_listening_set(cursor, set_data):
    cursor.execute("DELETE FROM questions WHERE skill = 'Listening'")
    
    for sec_data in set_data["sections"]:
        sec_num = sec_data["section_number"]
        sec_title = sec_data["title"]
        sec_transcript = sec_data["transcript"]
        
        for q in sec_data["questions"]:
            cursor.execute('''
                INSERT INTO questions (
                    title, skill, test_type, section_number, question_type,
                    passage_or_context, question_text, options_json, answer_key,
                    explanation, difficulty, cambridge_book, test_number,
                    passage_or_section, difficulty_band, group_id, group_instructions
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                sec_title,
                'Listening',
                'Academic',
                sec_num,
                q.get('type', 'Form Completion'),
                sec_transcript,
                q.get('text', ''),
                json.dumps(q.get('opts', [])),
                q.get('ans', ''),
                q.get('exp', ''),
                q.get('difficulty', 'Medium'),
                set_data.get('cambridge_book', 19),
                set_data.get('test_number', 1),
                sec_num,
                '7.0',
                f"S{sec_num}_G1",
                sec_data.get('instructions', '')
            ))

def get_set_a():
    return {
        "set_id": "A",
        "name": "Cambridge 19 - Test 1 (Eco-Lodge, Maritime Museum, Microgrids, Bioluminescence)",
        "cambridge_book": 19,
        "test_number": 1,
        "sections": [
            {
                "section_number": 1,
                "title": "Section 1: Bayview Eco-Lodge Customer Registration",
                "instructions": "Complete the form below. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each answer.",
                "transcript": """Officer: Good morning. Bayview Eco-Lodge and Activity Centre. How may I assist you?
Customer: Hello! I would like to book accommodation for my family for next month, and also sign up for some outdoor activity packages.
Officer: Excellent. I can certainly help you with that. Let me take down your contact details first. Could I have your surname, please?
Customer: Yes, it's Henderson. H-E-N-D-E-R-S-O-N.
Officer: Thank you, Mr. Henderson. And your first name?
Customer: It's Mark.
Officer: And a daytime telephone number we can reach you on?
Customer: You can reach me on 07911 802341.
Officer: Wonderful. What date are you planning to check in?
Customer: We will arrive on the 18th of October.
Officer: And how many nights will you be staying?
Customer: For 4 nights, checking out on the 22nd.
Officer: Great. Which accommodation option would you prefer? We have standard family rooms, luxury safari tents, and pine log cabins.
Customer: We would like the Pine Log Cabin, please.
Officer: Perfect choice. How many adults and children in total?
Customer: 2 adults and 2 children.
Officer: Do any of the guests have special dietary needs for our organic farm-to-table breakfast buffet?
Customer: Yes, my son has a severe nut allergy, and my wife is lactose-intolerant.
Officer: Noted: nut allergy and dairy-free breakfast. Regarding activities, which weekend guided excursion would you like to reserve?
Customer: We are keen to do the Forest Canopy Zipline on Saturday morning.
Officer: Excellent. That departs from Base Camp Station B at 10:15 AM.
Customer: How much is the initial holding deposit?
Officer: The required deposit is £120, payable by debit or credit card today.""",
                "questions": [
                    {"num": 1, "type": "Form Completion", "text": "Customer Surname: ________", "opts": [], "ans": "Henderson", "exp": "The customer spells his surname: H-E-N-D-E-R-S-O-N."},
                    {"num": 2, "type": "Form Completion", "text": "Contact Phone: ________", "opts": [], "ans": "07911 802341", "exp": "The customer provides the number 07911 802341."},
                    {"num": 3, "type": "Form Completion", "text": "Check-in Date: ________ October", "opts": [], "ans": "18th", "exp": "Check-in is on the 18th of October."},
                    {"num": 4, "type": "Form Completion", "text": "Duration of Stay: ________ nights", "opts": [], "ans": "4", "exp": "The customer confirms staying 4 nights."},
                    {"num": 5, "type": "Form Completion", "text": "Accommodation Type: Pine Log ________", "opts": [], "ans": "Cabin", "exp": "Selected room is the Pine Log Cabin."},
                    {"num": 6, "type": "Form Completion", "text": "Dietary Requirement 1: Son has severe ________ allergy", "opts": [], "ans": "nut", "exp": "Son has a severe nut allergy."},
                    {"num": 7, "type": "Form Completion", "text": "Dietary Requirement 2: Wife requires ________ meals", "opts": [], "ans": "dairy-free", "exp": "Wife is lactose-intolerant (dairy-free)."},
                    {"num": 8, "type": "Form Completion", "text": "Excursion: Forest Canopy ________", "opts": [], "ans": "Zipline", "exp": "The excursion is the Forest Canopy Zipline."},
                    {"num": 9, "type": "Form Completion", "text": "Departure Station: Base Camp Station ________", "opts": [], "ans": "B", "exp": "The officer confirms Station B."},
                    {"num": 10, "type": "Form Completion", "text": "Required Holding Deposit: £________", "opts": [], "ans": "120", "exp": "The deposit is £120."}
                ]
            },
            {
                "section_number": 2,
                "title": "Section 2: New Town Maritime Heritage Museum Tour",
                "instructions": "Questions 11–15: Choose the correct letter, A, B, C, or D. Questions 16–20: Label the map below.",
                "transcript": """Guide: Good morning, ladies and gentlemen, and welcome to the New Town Maritime Heritage Museum.
Before we start our guided exploration, please look at the orientation plan printed on your visitor badges.
The museum was originally founded in 1894 by Captain Arthur Davies and underwent a full modernization two years ago.
Admission is free for students, and general admission tickets are £8.50.
Let's talk about the facility layout. You are standing right now at the South Entrance facing north towards the harbor docks.
Directly to your left, west of the entrance hall, is Room A, our Audio-Visual Theater, where a 15-minute documentary plays every half hour.
Moving further north along the west corridor, tucked into the far northwest corner, is Room B, our Model Ship Workshop, where artisans restore historic wooden vessels.
Now, if you cross through the Central Atrium where the Great Galleon is displayed, you will find our panoramic Harbor View Cafe in the northeast corner at Room C.
Just south of the cafe along the eastern wall is Room D, the interactive Children's Discovery Zone with hands-on water locks and nautical puzzles.
Finally, right next to the South Entrance on your right-hand side is Room E, our Souvenir & Maritime Book Shop.""",
                "questions": [
                    {"num": 11, "type": "Multiple Choice", "text": "When was the original Maritime Museum founded?", "opts": ["A) 1884", "B) 1894", "C) 1904", "D) 1994"], "ans": "B) 1894", "exp": "The guide states the museum was founded in 1894."},
                    {"num": 12, "type": "Multiple Choice", "text": "How often is the documentary screened in the theater?", "opts": ["A) Every 15 minutes", "B) Every 30 minutes", "C) Every 45 minutes", "D) Once an hour"], "ans": "B) Every 30 minutes", "exp": "The 15-minute documentary plays every half hour."},
                    {"num": 13, "type": "Multiple Choice", "text": "What is the general admission fee for regular visitors?", "opts": ["A) Free", "B) £6.00", "C) £8.50", "D) £12.00"], "ans": "C) £8.50", "exp": "General admission tickets are £8.50."},
                    {"num": 14, "type": "Multiple Choice", "text": "Where is the Great Galleon artifact displayed?", "opts": ["A) West Corridor", "B) Central Atrium", "C) East Wing", "D) North Harbor Dock"], "ans": "B) Central Atrium", "exp": "The galleon is in the Central Atrium."},
                    {"num": 15, "type": "Multiple Choice", "text": "What can children experience in Room D?", "opts": ["A) Ship painting", "B) Water locks and nautical puzzles", "C) Sailing simulator", "D) Diving equipment"], "ans": "B) Water locks and nautical puzzles", "exp": "Room D offers hands-on water locks and nautical puzzles."},
                    {"num": 16, "type": "Map Labelling", "text": "Audio-Visual Theater", "opts": ["A", "B", "C", "D", "E"], "ans": "A", "exp": "Directly to the left of the entrance is Room A."},
                    {"num": 17, "type": "Map Labelling", "text": "Model Ship Workshop", "opts": ["A", "B", "C", "D", "E"], "ans": "B", "exp": "In the northwest corner is Room B."},
                    {"num": 18, "type": "Map Labelling", "text": "Harbor View Cafe", "opts": ["A", "B", "C", "D", "E"], "ans": "C", "exp": "In the northeast corner is Room C."},
                    {"num": 19, "type": "Map Labelling", "text": "Children's Discovery Zone", "opts": ["A", "B", "C", "D", "E"], "ans": "D", "exp": "South of the cafe on the eastern wall is Room D."},
                    {"num": 20, "type": "Map Labelling", "text": "Souvenir & Book Shop", "opts": ["A", "B", "C", "D", "E"], "ans": "E", "exp": "On the right side of the entrance is Room E."}
                ]
            },
            {
                "section_number": 3,
                "title": "Section 3: Smart Microgrids Academic Research Tutorial",
                "instructions": "Questions 21–30: Listen to the academic tutorial and answer questions 21–30.",
                "transcript": """Dr. Evans: Good afternoon, Jack and Maya. Let's discuss your final-year engineering thesis proposal on Decentralized Smart Microgrids. Jack, what is your primary thesis objective?
Jack: Well, Dr. Evans, we are evaluating how localized battery energy storage systems, or BESS, can stabilize grid frequency fluctuations during peak renewable load surges.
Dr. Evans: That is highly relevant. Maya, which methodology did you choose for your simulation models?
Maya: We decided to use dynamic Monte Carlo simulations because they allow us to incorporate volatile wind and solar variability over a 12-month period.
Dr. Evans: Excellent. And what was the biggest constraint you encountered in the pilot test at the university solar farm?
Jack: The main constraint was thermal dissipation during ultra-fast discharge cycles in high ambient summer temperatures.
Maya: Exactly. The battery pack efficiency dropped by nearly 14 percent when cell temperatures exceeded 45 degrees Celsius.
Dr. Evans: How do you plan to mitigate that issue in your revised design?
Jack: We are proposing a hybrid immersion cooling loop using biodegradable dielectric fluid.
Dr. Evans: That is innovative. Make sure you compare the capital installation costs against traditional air cooling before presenting to the board.""",
                "questions": [
                    {"num": 21, "type": "Multiple Choice", "text": "What is the primary focus of Jack and Maya's thesis?", "opts": ["A) Hydroelectric dam construction", "B) Battery storage for grid frequency stabilization", "C) Nuclear reactor efficiency", "D) Wind turbine blade design"], "ans": "B) Battery storage for grid frequency stabilization", "exp": "Jack confirms evaluating battery storage systems to stabilize grid frequency."},
                    {"num": 22, "type": "Multiple Choice", "text": "Why did Maya select Monte Carlo simulation methodology?", "opts": ["A) It is the cheapest software", "B) It handles volatile wind and solar variability", "C) It requires no coding", "D) Dr. Evans mandated it"], "ans": "B) It handles volatile wind and solar variability", "exp": "Maya mentions incorporating wind and solar variability."},
                    {"num": 23, "type": "Multiple Choice", "text": "What was the main physical constraint in the pilot study?", "opts": ["A) Power outage", "B) Thermal dissipation during fast discharge", "C) High electricity costs", "D) Sensor cable breakage"], "ans": "B) Thermal dissipation during fast discharge", "exp": "Jack highlights thermal dissipation during fast discharge."},
                    {"num": 24, "type": "Sentence Completion", "text": "Battery efficiency dropped by ________ percent during extreme heat.", "opts": [], "ans": "14", "exp": "Maya notes battery efficiency dropped by nearly 14 percent."},
                    {"num": 25, "type": "Sentence Completion", "text": "The critical threshold was exceeded when temperatures reached ________ degrees Celsius.", "opts": [], "ans": "45", "exp": "Cell temperatures exceeded 45 degrees Celsius."},
                    {"num": 26, "type": "Sentence Completion", "text": "The proposed solution is a hybrid ________ cooling loop.", "opts": [], "ans": "immersion", "exp": "Jack proposes a hybrid immersion cooling loop."},
                    {"num": 27, "type": "Sentence Completion", "text": "The coolant used will be biodegradable ________ fluid.", "opts": [], "ans": "dielectric", "exp": "They will use biodegradable dielectric fluid."},
                    {"num": 28, "type": "Multiple Choice", "text": "What must Jack and Maya compare before board presentation?", "opts": ["A) Environmental laws", "B) Capital installation costs vs air cooling", "C) Battery patents", "D) Student survey results"], "ans": "B) Capital installation costs vs air cooling", "exp": "Dr. Evans advises comparing capital installation costs."},
                    {"num": 29, "type": "Sentence Completion", "text": "The simulation model covers a duration of ________ months.", "opts": [], "ans": "12", "exp": "The simulation evaluates variability over a 12-month period."},
                    {"num": 30, "type": "Sentence Completion", "text": "The pilot was tested at the university ________ farm.", "opts": [], "ans": "solar", "exp": "Tested at the university solar farm."}
                ]
            },
            {
                "section_number": 4,
                "title": "Section 4: Marine Bioluminescence Academic Lecture",
                "instructions": "Complete the lecture notes below. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each answer.",
                "transcript": """Lecturer: Welcome back to Marine Biology 301. Today we are exploring the phenomenon of bioluminescence in deep-sea pelagic organisms.
Bioluminescence is the biochemical emission of light produced by living organisms.
Unlike incandescence, bioluminescence is cold light, meaning that less than 20 percent of the energy is lost as heat.
The primary biochemical reaction involves two molecules: a substrate called luciferin and an enzyme called luciferase.
When luciferin reacts with molecular oxygen in the presence of luciferase and magnesium ions, oxyluciferin is produced in an excited electronic state, emitting photons as it returns to ground state.
What evolutionary functions does this serve in the aphotic zone?
First is counterillumination camouflage. Organisms like the firefly squid produce downward-facing light that matches the intensity of sunlight penetrating from the surface, effectively eliminating their silhouette against predators below.
Second is defensive startling. Dinoflagellates flash intense blue-green light when mechanically disturbed, which blinds attackers and alerts secondary apex predators—a phenomenon known as the burglar alarm effect.
Third is predatory attraction. The anglerfish utilizes a modified dorsal ray tipped with a bioluminescent photophore containing symbiotic Vibrio bacteria to lure unsuspecting prey directly towards its jaws in total darkness.""",
                "questions": [
                    {"num": 31, "type": "Note Completion", "text": "Bioluminescent light is efficient: less than ________ percent is lost as heat.", "opts": [], "ans": "20", "exp": "Less than 20 percent of energy is lost as heat."},
                    {"num": 32, "type": "Note Completion", "text": "The light-emitting substrate molecule is called ________.", "opts": [], "ans": "luciferin", "exp": "The substrate is luciferin."},
                    {"num": 33, "type": "Note Completion", "text": "The reaction requires molecular ________ to proceed.", "opts": [], "ans": "oxygen", "exp": "Reacts with molecular oxygen."},
                    {"num": 34, "type": "Note Completion", "text": "The catalyst enzyme involved is ________.", "opts": [], "ans": "luciferase", "exp": "The enzyme is luciferase."},
                    {"num": 35, "type": "Note Completion", "text": "The excited end product is called ________.", "opts": [], "ans": "oxyluciferin", "exp": "Oxyluciferin is produced in an excited state."},
                    {"num": 36, "type": "Note Completion", "text": "Firefly squid use downward light for ________ camouflage.", "opts": [], "ans": "counterillumination", "exp": "Used for counterillumination camouflage."},
                    {"num": 37, "type": "Note Completion", "text": "Dinoflagellates emit a ________ light flash when disturbed.", "opts": [], "ans": "blue-green", "exp": "Flash intense blue-green light."},
                    {"num": 38, "type": "Note Completion", "text": "This defense mechanism is termed the ________ alarm effect.", "opts": [], "ans": "burglar", "exp": "Known as the burglar alarm effect."},
                    {"num": 39, "type": "Note Completion", "text": "Anglerfish photophores contain symbiotic ________ bacteria.", "opts": [], "ans": "Vibrio", "exp": "Symbiotic Vibrio bacteria."},
                    {"num": 40, "type": "Note Completion", "text": "The light organ is used primarily for predatory ________.", "opts": [], "ans": "attraction", "exp": "Used for predatory attraction to lure prey."}
                ]
            }
        ]
    }

def get_set_b():
    return {
        "set_id": "B",
        "name": "Cambridge 18 - Test 2 (Aquatic Centre, Wildlife Nature Park Map, Ocean Wave Energy, Language Evolution)",
        "cambridge_book": 18,
        "test_number": 2,
        "sections": [
            {
                "section_number": 1,
                "title": "Section 1: Greenwood Community Aquatic Centre Membership",
                "instructions": "Complete the form below. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each answer.",
                "transcript": """Officer: Good afternoon, Greenwood Community Aquatic Centre. How can I help you today?
Customer: Hello! I've recently moved to the area and would like to register for a family membership.
Officer: Welcome to Greenwood! I'll take your registration details right away. Could you spell your last name for me?
Customer: Yes, it is Sinclair. S-I-N-C-L-A-I-R.
Officer: Thank you. And your first name?
Customer: Fiona.
Officer: And your contact telephone number, Fiona?
Customer: It is 07700 900542.
Officer: And your residential address?
Customer: 24 Elmwood Avenue, Greenwood.
Officer: Which membership tier are you interested in? We have Bronze, Silver, and Gold Family All-Access.
Customer: We would like the Gold Family All-Access tier, please.
Officer: That includes unlimited pool access, fitness gym, and hydrotherapy sauna. What date would you like the membership to commence?
Customer: Starting on the 5th of November.
Officer: And how many family passes will be issued?
Customer: 3 passes in total: two adults and one teenager.
Officer: Do any members require accessible locker storage or private changing cubicles?
Customer: Yes, my husband needs ground-floor locker access due to a knee injury.
Officer: Noted. Ground-floor locker assigned. What is your preferred payment schedule?
Customer: Monthly direct debit.
Officer: The monthly fee is £65, with an initial induction fee of £15.""",
                "questions": [
                    {"num": 1, "type": "Form Completion", "text": "Customer Surname: ________", "opts": [], "ans": "Sinclair", "exp": "The customer spells S-I-N-C-L-A-I-R."},
                    {"num": 2, "type": "Form Completion", "text": "Customer First Name: ________", "opts": [], "ans": "Fiona", "exp": "First name is Fiona."},
                    {"num": 3, "type": "Form Completion", "text": "Contact Phone: ________", "opts": [], "ans": "07700 900542", "exp": "Phone is 07700 900542."},
                    {"num": 4, "type": "Form Completion", "text": "Street Address: 24 ________ Avenue", "opts": [], "ans": "Elmwood", "exp": "Address is 24 Elmwood Avenue."},
                    {"num": 5, "type": "Form Completion", "text": "Membership Tier: Gold Family ________", "opts": [], "ans": "All-Access", "exp": "Selected tier is Gold Family All-Access."},
                    {"num": 6, "type": "Form Completion", "text": "Start Date: ________ November", "opts": [], "ans": "5th", "exp": "Starts on 5th of November."},
                    {"num": 7, "type": "Form Completion", "text": "Total Passes: ________", "opts": [], "ans": "3", "exp": "3 passes in total."},
                    {"num": 8, "type": "Form Completion", "text": "Special Request: ________ locker access", "opts": [], "ans": "ground-floor", "exp": "Requires ground-floor locker access."},
                    {"num": 9, "type": "Form Completion", "text": "Monthly Fee: £________", "opts": [], "ans": "65", "exp": "Monthly fee is £65."},
                    {"num": 10, "type": "Form Completion", "text": "One-time Induction Fee: £________", "opts": [], "ans": "15", "exp": "Induction fee is £15."}
                ]
            },
            {
                "section_number": 2,
                "title": "Section 2: Greenwood Wildlife Nature Park & Trail Tour",
                "instructions": "Questions 11–15: Choose the correct letter, A, B, C, or D. Questions 16–20: Label the map below.",
                "transcript": """Ranger: Hello everyone, and welcome to Greenwood Wildlife Nature Park!
Our sanctuary spans over 200 acres of protected ancient woodland and wetlands.
The park is open daily from 9:00 AM until 6:00 PM, and guided nature safari walks begin at 11:00 AM every morning.
Please hold on to your trail maps while I explain the layout.
You are currently standing at the Main Ticket Plaza at the South Gate.
If you head straight north along the central paved path, the first building immediately on your left is Building A, our Educational Discovery Centre.
Continuing northwest along the canopy boardwalk, you will reach Building B, our Tropical Bird Aviary, housing over 60 endangered bird species.
Now, if you follow the eastern trail curving around the central duck pond, the large glasshouse situated in the northeast corner is Building C, the Reptile & Amphibian Bio-Dome.
Directly south of the Bio-Dome along the east boundary fence is Building D, the Woodland Treehouse Cafe and refreshment terrace.
Finally, right next to the South Gate on your right-hand side as you enter is Building E, the First Aid and Park Ranger Office.""",
                "questions": [
                    {"num": 11, "type": "Multiple Choice", "text": "What is the total area of the sanctuary?", "opts": ["A) 100 acres", "B) 150 acres", "C) 200 acres", "D) 300 acres"], "ans": "C) 200 acres", "exp": "The sanctuary spans over 200 acres."},
                    {"num": 12, "type": "Multiple Choice", "text": "What time do guided safari walks begin daily?", "opts": ["A) 9:00 AM", "B) 10:00 AM", "C) 11:00 AM", "D) 1:00 PM"], "ans": "C) 11:00 AM", "exp": "Guided safari walks begin at 11:00 AM."},
                    {"num": 13, "type": "Multiple Choice", "text": "How many bird species are housed in the aviary?", "opts": ["A) Over 40", "B) Over 60", "C) Over 80", "D) Over 100"], "ans": "B) Over 60", "exp": "Housing over 60 endangered bird species."},
                    {"num": 14, "type": "Multiple Choice", "text": "Where is the duck pond located?", "opts": ["A) West boundary", "B) Center of the park", "C) Outside South Gate", "D) North riverbank"], "ans": "B) Center of the park", "exp": "Trail curves around the central duck pond."},
                    {"num": 15, "type": "Multiple Choice", "text": "What is the closing time of the park?", "opts": ["A) 5:00 PM", "B) 6:00 PM", "C) 7:00 PM", "D) Dusk"], "ans": "B) 6:00 PM", "exp": "Open daily from 9:00 AM until 6:00 PM."},
                    {"num": 16, "type": "Map Labelling", "text": "Educational Discovery Centre", "opts": ["A", "B", "C", "D", "E"], "ans": "A", "exp": "First building on the left along the central path is A."},
                    {"num": 17, "type": "Map Labelling", "text": "Tropical Bird Aviary", "opts": ["A", "B", "C", "D", "E"], "ans": "B", "exp": "In the northwest along the canopy boardwalk is B."},
                    {"num": 18, "type": "Map Labelling", "text": "Reptile & Amphibian Bio-Dome", "opts": ["A", "B", "C", "D", "E"], "ans": "C", "exp": "Northeast corner glasshouse is C."},
                    {"num": 19, "type": "Map Labelling", "text": "Woodland Treehouse Cafe", "opts": ["A", "B", "C", "D", "E"], "ans": "D", "exp": "South of the Bio-Dome along the east fence is D."},
                    {"num": 20, "type": "Map Labelling", "text": "First Aid & Ranger Office", "opts": ["A", "B", "C", "D", "E"], "ans": "E", "exp": "Right next to the South Gate on the right side is E."}
                ]
            },
            {
                "section_number": 3,
                "title": "Section 3: Ocean Wave Energy Engineering Seminar",
                "instructions": "Questions 21–30: Listen to the research seminar between Professor Miller and students Leo and Sarah.",
                "transcript": """Prof. Miller: Welcome Leo and Sarah. Today let's review your research paper on Oscillating Water Column, or OWC, wave energy converters. Leo, explain how the air turbine functions.
Leo: Thank you, Professor. In an OWC chamber, rising wave motion compresses the trapped air column, forcing high-velocity air through a bidirectional Wells turbine.
Sarah: And because the Wells turbine utilizes symmetrical aerofoil blades, it maintains continuous unidirectional rotation regardless of whether the wave is rising or receding.
Prof. Miller: That is the core thermodynamic advantage. What were the key findings regarding offshore survivability during 50-year storm simulations?
Leo: The hydraulic moorings experienced maximum peak tension loads when wave heights exceeded 8.5 meters.
Sarah: To prevent structural failure, we implemented an automated pneumatic pressure relief valve that activates when chamber pressure rises above 2.4 bar.
Prof. Miller: What was the recorded overall conversion efficiency from kinetic wave energy to usable electric grid power?
Leo: The prototype delivered an average electrical conversion efficiency of 28 percent during sustained tidal swell tests.
Sarah: And the estimated levelized cost of energy dropped to 11 pence per kilowatt-hour when scaled across an 8-generator wave farm array.""",
                "questions": [
                    {"num": 21, "type": "Multiple Choice", "text": "What type of turbine is utilized in the OWC system?", "opts": ["A) Pelton turbine", "B) Wells bidirectional turbine", "C) Kaplan turbine", "D) Francis turbine"], "ans": "B) Wells bidirectional turbine", "exp": "Leo describes the bidirectional Wells turbine."},
                    {"num": 22, "type": "Multiple Choice", "text": "Why does the Wells turbine rotate in one continuous direction?", "opts": ["A) Electronic motors", "B) Symmetrical aerofoil blades", "C) One-way airflow valves", "D) High water pressure"], "ans": "B) Symmetrical aerofoil blades", "exp": "Sarah explains symmetrical aerofoil blades maintain continuous rotation."},
                    {"num": 23, "type": "Multiple Choice", "text": "What emergency device protects the chamber during storm surges?", "opts": ["A) Concrete breakwater", "B) Pneumatic pressure relief valve", "C) Anchor release mechanism", "D) Steel mesh filter"], "ans": "B) Pneumatic pressure relief valve", "exp": "Sarah notes the pneumatic pressure relief valve."},
                    {"num": 24, "type": "Sentence Completion", "text": "Critical wave height threshold was recorded at ________ meters.", "opts": [], "ans": "8.5", "exp": "Wave heights exceeded 8.5 meters."},
                    {"num": 25, "type": "Sentence Completion", "text": "The relief valve triggers at chamber pressure of ________ bar.", "opts": [], "ans": "2.4", "exp": "Activates when pressure rises above 2.4 bar."},
                    {"num": 26, "type": "Sentence Completion", "text": "Average electrical conversion efficiency was ________ percent.", "opts": [], "ans": "28", "exp": "Average electrical efficiency was 28 percent."},
                    {"num": 27, "type": "Sentence Completion", "text": "Levelized energy cost was estimated at ________ pence per kWh.", "opts": [], "ans": "11", "exp": "Cost dropped to 11 pence per kWh."},
                    {"num": 28, "type": "Sentence Completion", "text": "The scaled commercial model utilizes ________ generators in an array.", "opts": [], "ans": "8", "exp": "Scaled across an 8-generator wave farm array."},
                    {"num": 29, "type": "Multiple Choice", "text": "What happens to the air column when ocean waves rise?", "opts": ["A) It escapes through the base", "B) It is compressed upwards", "C) It cools down rapidly", "D) It turns into steam"], "ans": "B) It is compressed upwards", "exp": "Rising wave compresses the trapped air column."},
                    {"num": 30, "type": "Sentence Completion", "text": "Tests were conducted during sustained tidal ________ conditions.", "opts": [], "ans": "swell", "exp": "During sustained tidal swell tests."}
                ]
            },
            {
                "section_number": 4,
                "title": "Section 4: Cognitive Anthropology & Language Evolution Lecture",
                "instructions": "Complete the lecture notes below. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each answer.",
                "transcript": """Lecturer: Good morning, students. Today's lecture explores the biological and sociocultural origins of human spoken language.
Linguistic anthropologists estimate that anatomically modern syntax evolved roughly 70,000 years ago during the Upper Paleolithic Cognitive Revolution.
Key morphological changes in hominid anatomy enabled vocal versatility.
Specifically, the descent of the human larynx created an expanded pharyngeal cavity, allowing diverse formant modulation.
Additionally, geneticists discovered that mutations in the FOXP2 gene significantly enhanced fine motor control of the tongue and lips.
Social cohesion theories, notably proposed by Robin Dunbar, suggest language evolved primarily as a cognitive substitute for physical social grooming in expanding hunter-gatherer bands.
Furthermore, archaeological evidence of Neanderthal burial sites containing red ochre pigment and ceremonial beads implies symbolic communication preceded modern syntactic language by at least 30,000 years.
Today, linguists categorize the world's 7,000 extant languages into approximately 140 distinct language families, with Indo-European and Sino-Tibetan accounting for over 60 percent of the global population.""",
                "questions": [
                    {"num": 31, "type": "Note Completion", "text": "Modern syntax emerged approximately ________ years ago.", "opts": [], "ans": "70,000", "exp": "Evolved roughly 70,000 years ago."},
                    {"num": 32, "type": "Note Completion", "text": "Anatomical flexibility increased due to the lower position of the ________.", "opts": [], "ans": "larynx", "exp": "The descent of the larynx."},
                    {"num": 33, "type": "Note Completion", "text": "Motor speech articulation is regulated by the ________ gene.", "opts": [], "ans": "FOXP2", "exp": "Mutations in the FOXP2 gene."},
                    {"num": 34, "type": "Note Completion", "text": "Robin Dunbar argued language replaced physical social ________.", "opts": [], "ans": "grooming", "exp": "Substitute for physical social grooming."},
                    {"num": 35, "type": "Note Completion", "text": "Early symbolic culture is evidenced by the use of red ________ pigment.", "opts": [], "ans": "ochre", "exp": "Burial sites containing red ochre pigment."},
                    {"num": 36, "type": "Note Completion", "text": "Symbolic artifacts predate modern syntax by ________ years.", "opts": [], "ans": "30,000", "exp": "Preceded syntactic language by at least 30,000 years."},
                    {"num": 37, "type": "Note Completion", "text": "There are approximately ________ surviving languages in the world.", "opts": [], "ans": "7,000", "exp": "The world's 7,000 extant languages."},
                    {"num": 38, "type": "Note Completion", "text": "Languages are classified into around ________ language families.", "opts": [], "ans": "140", "exp": "Approximately 140 distinct language families."},
                    {"num": 39, "type": "Note Completion", "text": "Indo-European and ________ represent over 60% of all speakers.", "opts": [], "ans": "Sino-Tibetan", "exp": "Indo-European and Sino-Tibetan."},
                    {"num": 40, "type": "Note Completion", "text": "Formant sound modulation occurs in the expanded ________ cavity.", "opts": [], "ans": "pharyngeal", "exp": "Expanded pharyngeal cavity."}
                ]
            }
        ]
    }

def get_set_c():
    return {
        "set_id": "C",
        "name": "Cambridge 17 - Test 3 (Car Rental, Riverfront Arts Festival Map, Microplastics Ecology, Space Archaeology)",
        "cambridge_book": 17,
        "test_number": 3,
        "sections": [
            {
                "section_number": 1,
                "title": "Section 1: City Car Rental & Insurance Registration",
                "instructions": "Complete the form below. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each answer.",
                "transcript": """Agent: Apex Executive Car Rental, how may I help you?
Customer: Hi! I need to reserve a rental car for a business trip next Tuesday.
Agent: Absolutely. Let's start with your driver details. Surname please?
Customer: It's Radcliffe. R-A-D-C-L-I-F-F-E.
Agent: Thank you. And your first name?
Customer: Gregory.
Agent: Contact mobile number?
Customer: 07892 411039.
Agent: Driver's license issuing country?
Customer: United Kingdom.
Agent: Vehicle category requested? We have Compact Hatchback, Electric Sedan, and Full-size SUV.
Customer: I would like the Electric Sedan, please.
Agent: Pick-up date and time?
Customer: 14th of September at 8:30 AM from the Central Railway Station branch.
Agent: And drop-off location?
Customer: Airport Terminal 2 branch on the 18th of September.
Agent: Would you like our Zero-Excess Comprehensive Insurance protection?
Customer: Yes, please add the Zero-Excess coverage and an optional GPS navigation unit.
Agent: Total daily rate is £48, plus a refundable security deposit of £200.""",
                "questions": [
                    {"num": 1, "type": "Form Completion", "text": "Customer Surname: ________", "opts": [], "ans": "Radcliffe", "exp": "Spells R-A-D-C-L-I-F-F-E."},
                    {"num": 2, "type": "Form Completion", "text": "Customer First Name: ________", "opts": [], "ans": "Gregory", "exp": "First name is Gregory."},
                    {"num": 3, "type": "Form Completion", "text": "Mobile Phone: ________", "opts": [], "ans": "07892 411039", "exp": "Phone is 07892 411039."},
                    {"num": 4, "type": "Form Completion", "text": "Vehicle Category: Electric ________", "opts": [], "ans": "Sedan", "exp": "Selected the Electric Sedan."},
                    {"num": 5, "type": "Form Completion", "text": "Pick-up Date: ________ September", "opts": [], "ans": "14th", "exp": "Pick-up date is 14th of September."},
                    {"num": 6, "type": "Form Completion", "text": "Pick-up Station: Central ________ Station", "opts": [], "ans": "Railway", "exp": "Central Railway Station branch."},
                    {"num": 7, "type": "Form Completion", "text": "Drop-off Location: Airport Terminal ________", "opts": [], "ans": "2", "exp": "Airport Terminal 2 branch."},
                    {"num": 8, "type": "Form Completion", "text": "Insurance Option: ________ Comprehensive", "opts": [], "ans": "Zero-Excess", "exp": "Requested Zero-Excess coverage."},
                    {"num": 9, "type": "Form Completion", "text": "Optional Equipment: ________ navigation unit", "opts": [], "ans": "GPS", "exp": "Added optional GPS navigation."},
                    {"num": 10, "type": "Form Completion", "text": "Refundable Security Deposit: £________", "opts": [], "ans": "200", "exp": "Security deposit is £200."}
                ]
            },
            {
                "section_number": 2,
                "title": "Section 2: Riverfront Arts & Music Festival Grounds",
                "instructions": "Questions 11–15: Choose the correct letter, A, B, C, or D. Questions 16–20: Label the map below.",
                "transcript": """Coordinator: Welcome volunteers to the briefing for the annual Riverfront Arts & Music Festival!
The festival runs from Friday through Sunday and is expected to attract over 15,000 visitors.
Let's review the festival grounds layout. You are standing at the South Pedestrian Entrance facing north toward the riverbank promenade.
Directly to your left on the west lawn is Area A, the Acoustic Folk Stage.
Further northwest along the riverwalk promenade is Area B, the International Food Pavilion with over 25 gourmet street food trucks.
Across on the eastern side, in the far northeast corner next to the marina, is Area C, the Artisan Craft Market and sculpture exhibition.
Immediately south of the craft market along the eastern border is Area D, the Kids Carnival & Puppet Theater tent.
Finally, right beside the South Pedestrian Entrance on your right is Area E, the Volunteer Operations & Lost Property tent.""",
                "questions": [
                    {"num": 11, "type": "Multiple Choice", "text": "How many days does the festival run?", "opts": ["A) 2 days", "B) 3 days", "C) 4 days", "D) 7 days"], "ans": "B) 3 days", "exp": "Runs from Friday through Sunday (3 days)."},
                    {"num": 12, "type": "Multiple Choice", "text": "What is the expected visitor attendance?", "opts": ["A) 5,000", "B) 10,000", "C) 15,000", "D) 25,000"], "ans": "C) 15,000", "exp": "Expected to attract over 15,000 visitors."},
                    {"num": 13, "type": "Multiple Choice", "text": "How many food trucks are at the food pavilion?", "opts": ["A) Over 15", "B) Over 20", "C) Over 25", "D) Over 50"], "ans": "C) Over 25", "exp": "Over 25 gourmet street food trucks."},
                    {"num": 14, "type": "Multiple Choice", "text": "Where is the artisan craft market located?", "opts": ["A) South Gate", "B) West Lawn", "C) Northeast corner near marina", "D) Central plaza"], "ans": "C) Northeast corner near marina", "exp": "In the northeast corner next to the marina."},
                    {"num": 15, "type": "Multiple Choice", "text": "What is located on the west lawn?", "opts": ["A) Food Pavilion", "B) Acoustic Folk Stage", "C) Car park", "D) Beer tent"], "ans": "B) Acoustic Folk Stage", "exp": "West lawn holds the Acoustic Folk Stage."},
                    {"num": 16, "type": "Map Labelling", "text": "Acoustic Folk Stage", "opts": ["A", "B", "C", "D", "E"], "ans": "A", "exp": "On the west lawn is Area A."},
                    {"num": 17, "type": "Map Labelling", "text": "International Food Pavilion", "opts": ["A", "B", "C", "D", "E"], "ans": "B", "exp": "Northwest along the riverwalk is Area B."},
                    {"num": 18, "type": "Map Labelling", "text": "Artisan Craft Market", "opts": ["A", "B", "C", "D", "E"], "ans": "C", "exp": "Northeast corner near marina is Area C."},
                    {"num": 19, "type": "Map Labelling", "text": "Kids Carnival & Puppet Tent", "opts": ["A", "B", "C", "D", "E"], "ans": "D", "exp": "South of the craft market on the east border is Area D."},
                    {"num": 20, "type": "Map Labelling", "text": "Volunteer Operations & Lost Property", "opts": ["A", "B", "C", "D", "E"], "ans": "E", "exp": "Beside the South Entrance on the right is Area E."}
                ]
            },
            {
                "section_number": 3,
                "title": "Section 3: Urban Microplastics Freshwater Ecology Seminar",
                "instructions": "Questions 21–30: Listen to the research discussion and answer questions 21–30.",
                "transcript": """Tutor: Good afternoon, Liam and Chloe. Let's discuss your field sampling study on synthetic microfibers in urban river catchments. Liam, what was your sampling protocol?
Liam: We sampled surface water and sediment cores across 12 monitoring stations along the River Mersey over a 6-month period.
Chloe: For filtration, we used 50-micrometer stainless steel mesh sieves and digested organic matter with hydrogen peroxide.
Tutor: Which polymer type was most prevalent in your spectroscopic analysis?
Liam: Polyester fibers represented 54 percent of all identified particles, primarily originating from domestic laundry wastewater effluent.
Chloe: The second most abundant was polyamide nylon from commercial fishing and textile runoff, accounting for 22 percent.
Tutor: Did you detect bioaccumulation in benthic macroinvertebrates?
Liam: Yes, freshwater river mussels displayed an average bio-load of 18 microplastic particles per gram of soft tissue.
Chloe: And laboratory assays showed a 30 percent reduction in filter-feeding filtration rates when exposed to high microplastic concentrations.
Tutor: Excellent data. Make sure you highlight storm runoff discharge peaks in your final discussion chapter.""",
                "questions": [
                    {"num": 21, "type": "Multiple Choice", "text": "How many sampling stations were monitored along the river?", "opts": ["A) 6", "B) 8", "C) 12", "D) 24"], "ans": "C) 12", "exp": "Sampled across 12 monitoring stations."},
                    {"num": 22, "type": "Multiple Choice", "text": "What size mesh sieve was used for filtration?", "opts": ["A) 20-micrometer", "B) 50-micrometer", "C) 100-micrometer", "D) 250-micrometer"], "ans": "B) 50-micrometer", "exp": "Used 50-micrometer stainless steel mesh."},
                    {"num": 23, "type": "Multiple Choice", "text": "Which chemical was used to digest organic matter?", "opts": ["A) Sulfuric acid", "B) Hydrogen peroxide", "C) Sodium hydroxide", "D) Ethanol"], "ans": "B) Hydrogen peroxide", "exp": "Digested organic matter with hydrogen peroxide."},
                    {"num": 24, "type": "Sentence Completion", "text": "Polyester fibers accounted for ________ percent of all particles.", "opts": [], "ans": "54", "exp": "Polyester fibers represented 54 percent."},
                    {"num": 25, "type": "Sentence Completion", "text": "Polyamide nylon accounted for ________ percent of runoff.", "opts": [], "ans": "22", "exp": "Polyamide nylon accounted for 22 percent."},
                    {"num": 26, "type": "Sentence Completion", "text": "Mussels contained ________ microplastic particles per gram.", "opts": [], "ans": "18", "exp": "Average bio-load of 18 particles per gram."},
                    {"num": 27, "type": "Sentence Completion", "text": "Filtration rates dropped by ________ percent in laboratory trials.", "opts": [], "ans": "30", "exp": "Showed a 30 percent reduction in filtration rates."},
                    {"num": 28, "type": "Sentence Completion", "text": "Sampling was conducted over a duration of ________ months.", "opts": [], "ans": "6", "exp": "Conducted over a 6-month period."},
                    {"num": 29, "type": "Multiple Choice", "text": "What was the primary source of polyester fibers?", "opts": ["A) Agricultural plastics", "B) Domestic laundry wastewater", "C) Car tire degradation", "D) Beverage packaging"], "ans": "B) Domestic laundry wastewater", "exp": "Originating from domestic laundry wastewater effluent."},
                    {"num": 30, "type": "Sentence Completion", "text": "Tutor recommended highlighting storm ________ peaks in the paper.", "opts": [], "ans": "runoff", "exp": "Highlight storm runoff discharge peaks."}
                ]
            },
            {
                "section_number": 4,
                "title": "Section 4: Space Archaeology & LiDAR Ancient Settlement Detection",
                "instructions": "Complete the lecture notes below. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each answer.",
                "transcript": """Lecturer: Welcome everyone to Archaeological Remote Sensing. Today we examine satellite imaging and airborne LiDAR in uncovering lost civilizations.
LiDAR stands for Light Detection and Ranging.
By pulsing up to 500,000 laser beams per second from an aircraft and measuring the time of flight for the light to return, researchers can map micro-topography beneath dense tropical canopies.
In 2016, the PACUNAM LiDAR initiative scanned over 2,100 square kilometers of the Maya Biosphere Reserve in northern Guatemala.
The survey revealed more than 61,000 previously unrecorded structures, including raised agricultural terraces, defensive fortifications, and elevated stone causeways known as sacbeob.
Furthermore, multispectral thermal infrared sensors aboard satellites like Landsat and Sentinel detect sub-surface soil moisture anomalies caused by buried stone foundations.
In the Nile Delta, satellite imagery identified over 17 buried ancient river channels and 3,000 lost settlements, radically transforming Egyptological demographic models.
Today, autonomous drones equipped with hyperspectral cameras provide ground resolution under 2 centimeters, enabling non-destructive excavation mapping.""",
                "questions": [
                    {"num": 31, "type": "Note Completion", "text": "LiDAR pulses up to ________ laser beams per second.", "opts": [], "ans": "500,000", "exp": "Pulsing up to 500,000 laser beams per second."},
                    {"num": 32, "type": "Note Completion", "text": "LiDAR measures time of ________ to calculate distance.", "opts": [], "ans": "flight", "exp": "Measuring the time of flight for light to return."},
                    {"num": 33, "type": "Note Completion", "text": "PACUNAM surveyed ________ square kilometers in Guatemala.", "opts": [], "ans": "2,100", "exp": "Scanned over 2,100 square kilometers."},
                    {"num": 34, "type": "Note Completion", "text": "The survey discovered over ________ unknown structures.", "opts": [], "ans": "61,000", "exp": "Revealed more than 61,000 previously unrecorded structures."},
                    {"num": 35, "type": "Note Completion", "text": "Elevated Maya stone causeways are named ________.", "opts": [], "ans": "sacbeob", "exp": "Elevated stone causeways known as sacbeob."},
                    {"num": 36, "type": "Note Completion", "text": "Satellites detect soil ________ anomalies above buried walls.", "opts": [], "ans": "moisture", "exp": "Soil moisture anomalies caused by buried foundations."},
                    {"num": 37, "type": "Note Completion", "text": "Nile Delta surveys found ________ lost river channels.", "opts": [], "ans": "17", "exp": "Identified over 17 buried ancient river channels."},
                    {"num": 38, "type": "Note Completion", "text": "Over ________ ancient settlements were mapped in Egypt.", "opts": [], "ans": "3,000", "exp": "Mapped over 3,000 lost settlements."},
                    {"num": 39, "type": "Note Completion", "text": "Drones achieve ground resolution under ________ centimeters.", "opts": [], "ans": "2", "exp": "Resolution under 2 centimeters."},
                    {"num": 40, "type": "Note Completion", "text": "Aerial surveys allow non-destructive excavation ________.", "opts": [], "ans": "mapping", "exp": "Enabling non-destructive excavation mapping."}
                ]
            }
        ]
    }

def get_set_d():
    return {
        "set_id": "D",
        "name": "Cambridge 16 - Test 4 (Homestay Accommodation, Botanic Gardens Map, AI Healthcare Ethics, Lighthouses)",
        "cambridge_book": 16,
        "test_number": 4,
        "sections": [
            {
                "section_number": 1,
                "title": "Section 1: International Student Homestay Registration",
                "instructions": "Complete the form below. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each answer.",
                "transcript": """Officer: University International Student Services. How may I help you?
Student: Hello! I am arriving for the autumn semester and would like to apply for the homestay family accommodation program.
Officer: Wonderful. Let's get your details on file. May I have your family name?
Customer: Yes, it is Tanaka. T-A-N-A-K-A.
Officer: First name?
Customer: Kenji.
Officer: Country of origin?
Customer: Japan.
Officer: Contact email address?
Customer: kenji.tanaka@tokyomail.jp.
Officer: What degree course will you be studying?
Customer: I am enrolled in the Master of Architecture program.
Officer: Planned arrival date in the UK?
Customer: On the 22nd of September.
Officer: Expected duration of homestay placement?
Customer: For 6 months.
Officer: Do you have any dietary requirements or pet allergies?
Customer: I am a vegetarian, and I have a slight allergy to cats.
Officer: Noted: vegetarian meals and no cats in the household. Do you have a location preference?
Customer: I prefer accommodation within 30 minutes by bus from the Central Campus.
Officer: The standard homestay fee is £190 per week, which includes half-board meals and all utility bills.""",
                "questions": [
                    {"num": 1, "type": "Form Completion", "text": "Student Surname: ________", "opts": [], "ans": "Tanaka", "exp": "Spells T-A-N-A-K-A."},
                    {"num": 2, "type": "Form Completion", "text": "Student First Name: ________", "opts": [], "ans": "Kenji", "exp": "First name is Kenji."},
                    {"num": 3, "type": "Form Completion", "text": "Country of Origin: ________", "opts": [], "ans": "Japan", "exp": "Origin is Japan."},
                    {"num": 4, "type": "Form Completion", "text": "Course of Study: Master of ________", "opts": [], "ans": "Architecture", "exp": "Master of Architecture."},
                    {"num": 5, "type": "Form Completion", "text": "Arrival Date: ________ September", "opts": [], "ans": "22nd", "exp": "Arrives on 22nd of September."},
                    {"num": 6, "type": "Form Completion", "text": "Placement Duration: ________ months", "opts": [], "ans": "6", "exp": "Duration is 6 months."},
                    {"num": 7, "type": "Form Completion", "text": "Dietary Requirement: ________ meals", "opts": [], "ans": "vegetarian", "exp": "Requires vegetarian meals."},
                    {"num": 8, "type": "Form Completion", "text": "Pet Allergy: allergic to ________", "opts": [], "ans": "cats", "exp": "Allergic to cats."},
                    {"num": 9, "type": "Form Completion", "text": "Commute Preference: within ________ minutes by bus", "opts": [], "ans": "30", "exp": "Within 30 minutes by bus."},
                    {"num": 10, "type": "Form Completion", "text": "Weekly Homestay Fee: £________", "opts": [], "ans": "190", "exp": "Standard fee is £190 per week."}
                ]
            },
            {
                "section_number": 2,
                "title": "Section 2: Royal Botanic Gardens & Conservatory Tour",
                "instructions": "Questions 11–15: Choose the correct letter, A, B, C, or D. Questions 16–20: Label the map below.",
                "transcript": """Guide: Welcome visitors to the Royal Botanic Gardens and Heritage Conservatory!
Established in 1840, our gardens house over 28,000 living plant accessions across 40 landscaped hectares.
Let's review the visitor map. You are currently standing at the Main South Palm Gate.
Directly on your left as you enter along the western perimeter walk is Building A, our Mediterranean Succulent House.
Following the path northwest past the central lily pond brings you to Building B, the Victorian Tropical Palm Conservatory, featuring our 15-meter tall giant bamboo.
Directly across on the northeast side near the rose gardens is Building C, the Orchid Pavilion & Seed Vault.
South of the Orchid Pavilion along the eastern tree-lined promenade is Building D, the Botanical Library and Herbarium Research Wing.
Finally, right by the South Palm Gate on your right-hand side is Building E, the Garden Cafe and Gift Nursery.""",
                "questions": [
                    {"num": 11, "type": "Multiple Choice", "text": "When were the Royal Botanic Gardens established?", "opts": ["A) 1820", "B) 1840", "C) 1860", "D) 1900"], "ans": "B) 1840", "exp": "Established in 1840."},
                    {"num": 12, "type": "Multiple Choice", "text": "How many living plant accessions are cultivated?", "opts": ["A) Over 10,000", "B) Over 20,000", "C) Over 28,000", "D) Over 50,000"], "ans": "C) Over 28,000", "exp": "House over 28,000 living plant accessions."},
                    {"num": 13, "type": "Multiple Choice", "text": "How tall is the giant bamboo in the palm house?", "opts": ["A) 10 meters", "B) 12 meters", "C) 15 meters", "D) 20 meters"], "ans": "C) 15 meters", "exp": "Featuring 15-meter tall giant bamboo."},
                    {"num": 14, "type": "Multiple Choice", "text": "Where is the lily pond located?", "opts": ["A) Entrance", "B) Center of the gardens", "C) East boundary", "D) South corner"], "ans": "B) Center of the gardens", "exp": "Path passes the central lily pond."},
                    {"num": 15, "type": "Multiple Choice", "text": "What is housed next to the Orchid Pavilion?", "opts": ["A) Car park", "B) Seed Vault", "C) Rose garden", "D) Birdhouse"], "ans": "B) Seed Vault", "exp": "Orchid Pavilion & Seed Vault."},
                    {"num": 16, "type": "Map Labelling", "text": "Mediterranean Succulent House", "opts": ["A", "B", "C", "D", "E"], "ans": "A", "exp": "On the left along the western walk is Building A."},
                    {"num": 17, "type": "Map Labelling", "text": "Victorian Tropical Palm Conservatory", "opts": ["A", "B", "C", "D", "E"], "ans": "B", "exp": "Northwest past the lily pond is Building B."},
                    {"num": 18, "type": "Map Labelling", "text": "Orchid Pavilion & Seed Vault", "opts": ["A", "B", "C", "D", "E"], "ans": "C", "exp": "Northeast side near rose gardens is Building C."},
                    {"num": 19, "type": "Map Labelling", "text": "Herbarium Research Wing", "opts": ["A", "B", "C", "D", "E"], "ans": "D", "exp": "South of Orchid Pavilion on eastern walk is Building D."},
                    {"num": 20, "type": "Map Labelling", "text": "Garden Cafe and Gift Nursery", "opts": ["A", "B", "C", "D", "E"], "ans": "E", "exp": "Right by the South Gate on the right is Building E."}
                ]
            },
            {
                "section_number": 3,
                "title": "Section 3: AI in Healthcare Clinical Ethics Debate",
                "instructions": "Questions 21–30: Listen to the clinical tutorial between Dr. Collins and medical students Mark and Rachel.",
                "transcript": """Dr. Collins: Good afternoon, Mark and Rachel. Today let's evaluate algorithmic transparency and diagnostic accountability in clinical AI deployments. Mark, summarize the radiology findings.
Mark: In our comparative study of deep learning models for detecting pulmonary nodules on CT scans, the neural network matched expert radiologists with a 94 percent sensitivity rate.
Rachel: However, false-positive rates were nearly double when processing patient scans with pre-existing chronic fibrosis.
Dr. Collins: That underscores the black box interpretability problem. How did you assess algorithmic bias across demographic cohorts?
Mark: We discovered that diagnostic error rates increased by 16 percent in elderly cohorts over 75 years old due to underrepresentation in training datasets.
Rachel: To ensure ethical compliance, we recommend mandatory human-in-the-loop validation for all high-risk clinical triage categories.
Dr. Collins: What regulatory standard should hospitals adopt for patient informed consent?
Mark: Patients must have the legal right to opt out of automated algorithmic diagnostic assessments and request a human second opinion without penalty.
Rachel: And healthcare institutions should maintain immutable audit logs of all automated recommendations for a minimum of 10 years.""",
                "questions": [
                    {"num": 21, "type": "Multiple Choice", "text": "What sensitivity rate did the AI model achieve in radiology?", "opts": ["A) 84%", "B) 90%", "C) 94%", "D) 99%"], "ans": "C) 94%", "exp": "Matched expert radiologists with 94 percent sensitivity."},
                    {"num": 22, "type": "Multiple Choice", "text": "Why did false positive rates increase in some scans?", "opts": ["A) Low image resolution", "B) Chronic fibrosis", "C) Patient movement", "D) Software crash"], "ans": "B) Chronic fibrosis", "exp": "Higher in patients with pre-existing chronic fibrosis."},
                    {"num": 23, "type": "Multiple Choice", "text": "What caused higher error rates in elderly patients?", "opts": ["A) Slower computers", "B) Underrepresentation in training datasets", "C) Medication interference", "D) Shorter scan time"], "ans": "B) Underrepresentation in training datasets", "exp": "Due to underrepresentation in training datasets."},
                    {"num": 24, "type": "Sentence Completion", "text": "Diagnostic error rate increased by ________ percent in elderly cohorts.", "opts": [], "ans": "16", "exp": "Error rates increased by 16 percent."},
                    {"num": 25, "type": "Sentence Completion", "text": "The affected cohort included patients over ________ years of age.", "opts": [], "ans": "75", "exp": "Cohorts over 75 years old."},
                    {"num": 26, "type": "Sentence Completion", "text": "Rachel recommends mandatory human-in-the-loop ________ for triage.", "opts": [], "ans": "validation", "exp": "Mandatory human-in-the-loop validation."},
                    {"num": 27, "type": "Sentence Completion", "text": "Patients should have the right to opt ________ of automated diagnosis.", "opts": [], "ans": "out", "exp": "Legal right to opt out."},
                    {"num": 28, "type": "Sentence Completion", "text": "Audit logs of AI decisions must be stored for at least ________ years.", "opts": [], "ans": "10", "exp": "Minimum of 10 years."},
                    {"num": 29, "type": "Multiple Choice", "text": "What right should patients retain without penalty?", "opts": ["A) Free treatment", "B) Request a human second opinion", "C) Immediate discharge", "D) Access to source code"], "ans": "B) Request a human second opinion", "exp": "Request a human second opinion without penalty."},
                    {"num": 30, "type": "Sentence Completion", "text": "The core interpretability issue is known as the black ________ problem.", "opts": [], "ans": "box", "exp": "The black box interpretability problem."}
                ]
            },
            {
                "section_number": 4,
                "title": "Section 4: Deep-Sea Lighthouse Architecture & Engineering Lecture",
                "instructions": "Complete the lecture notes below. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each answer.",
                "transcript": """Lecturer: Good morning class. Today we examine the civil and marine engineering history of offshore deep-sea lighthouses.
Building masonry structures capable of withstanding relentless North Atlantic wave impacts required groundbreaking innovations.
The most legendary breakthrough occurred at the Eddystone Rocks off the coast of Cornwall.
In 1759, civil engineer John Smeaton constructed the third Eddystone Lighthouse using dovetailed granite blocks.
Each granite block was individually carved with interlocking mortise and tenon joints, creating an indestructible monolithic stone cylinder modeled after the trunk of an English oak tree.
Furthermore, Smeaton formulated a quick-setting hydraulic lime mortar that cured underwater, resisting salt water wave scour.
In 1822, French physicist Augustin Fresnel invented the stepped Fresnel lens, utilizing concentric annular prisms to capture 83 percent of light output and project a concentrated horizontal beam visible up to 20 nautical miles across the horizon.
Modern automated lighthouses utilize solar photovoltaic arrays and LED optic arrays requiring service maintenance only once every 5 years.""",
                "questions": [
                    {"num": 31, "type": "Note Completion", "text": "John Smeaton built the third Eddystone Lighthouse in ________.", "opts": [], "ans": "1759", "exp": "Constructed in 1759."},
                    {"num": 32, "type": "Note Completion", "text": "The structural design was inspired by the trunk of an oak ________.", "opts": [], "ans": "tree", "exp": "Modeled after the trunk of an English oak tree."},
                    {"num": 33, "type": "Note Completion", "text": "Blocks were joined using interlocking ________ joints.", "opts": [], "ans": "dovetailed", "exp": "Dovetailed granite blocks."},
                    {"num": 34, "type": "Note Completion", "text": "Smeaton developed hydraulic ________ mortar that cured underwater.", "opts": [], "ans": "lime", "exp": "Hydraulic lime mortar."},
                    {"num": 35, "type": "Note Completion", "text": "The stepped lens was invented by Augustin ________ in 1822.", "opts": [], "ans": "Fresnel", "exp": "Invented by Augustin Fresnel."},
                    {"num": 36, "type": "Note Completion", "text": "The lens captures ________ percent of lamp light output.", "opts": [], "ans": "83", "exp": "Capture 83 percent of light output."},
                    {"num": 37, "type": "Note Completion", "text": "Beam is visible up to ________ nautical miles away.", "opts": [], "ans": "20", "exp": "Visible up to 20 nautical miles."},
                    {"num": 38, "type": "Note Completion", "text": "Modern beacons are powered by solar ________ arrays.", "opts": [], "ans": "photovoltaic", "exp": "Solar photovoltaic arrays."},
                    {"num": 39, "type": "Note Completion", "text": "Automated units require maintenance once every ________ years.", "opts": [], "ans": "5", "exp": "Once every 5 years."},
                    {"num": 40, "type": "Note Completion", "text": "The granite structure forms an indestructible monolithic ________.", "opts": [], "ans": "cylinder", "exp": "An indestructible monolithic stone cylinder."}
                ]
            }
        ]
    }

ALL_SETS = {
    "A": get_set_a,
    "B": get_set_b,
    "C": get_set_c,
    "D": get_set_d
}

def seed_full_cambridge_listening_set(set_name="A"):
    conn = sqlite3.connect('ielts_platform.db')
    cursor = conn.cursor()
    
    set_fn = ALL_SETS.get(set_name.upper(), get_set_a)
    data = set_fn()
    insert_listening_set(cursor, data)
    
    conn.commit()
    conn.close()
    return data

def seed_random_listening_set():
    chosen_key = random.choice(list(ALL_SETS.keys()))
    return seed_full_cambridge_listening_set(chosen_key)

if __name__ == '__main__':
    seed_full_cambridge_listening_set("A")
    print("Seeded Default Listening Set A (Cambridge 19) successfully.")