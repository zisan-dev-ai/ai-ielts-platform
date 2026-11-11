# -*- coding: utf-8 -*-
import sqlite3
import json

def seed_full_cambridge_listening():
    conn = sqlite3.connect('ielts_platform.db')
    cursor = conn.cursor()

    # Clear old listening questions
    cursor.execute("DELETE FROM questions WHERE skill = 'Listening'")

    # =========================================================================
    # PART 1 (Q1–10): Customer Registration & Tour Booking Form (Dialogue)
    # =========================================================================
    s1_title = "Part 1: Bayview Eco-Lodge & Outdoor Centre Booking"
    s1_instructions = "Complete the notes below. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each answer."
    s1_context = """Officer: Good morning. Bayview Eco-Lodge and Outdoor Centre. How may I help you?
Customer: Hello! I'd like to book accommodation for my family for an autumn break, and also reserve some outdoor activity packages.
Officer: Certainly. Let me take down your details first. Could I have your surname, please?
Customer: Yes, it's Henderson. That's H-E-N-D-E-R-S-O-N.
Officer: Thank you, Mr Henderson. And your first name?
Customer: Mark.
Officer: And a daytime telephone number we can reach you on?
Customer: Yes, it's 07911 802341.
Officer: Great. What date would you like to check in?
Customer: We were originally thinking of the 16th of October, but let's make it the 18th of October.
Officer: 18th of October. And how many nights will you be staying?
Customer: We will be staying for 4 nights, checking out on the 22nd.
Officer: Fine. We have standard family chalets, safari tents, and pine log cabins. Which accommodation type would you prefer?
Customer: We'd definitely like the Pine Log Cabin, please.
Officer: Excellent choice. And how many guests in total?
Customer: Two adults and two children.
Officer: Do any members of your party have special dietary requirements for our organic breakfast buffet?
Customer: Yes, my son has a severe nut allergy, and my wife is lactose-intolerant, so she requires dairy-free meals.
Officer: Noted: nut allergy and dairy-free breakfast. Now, regarding weekend activities, which guided excursion would you like to join on Saturday morning?
Customer: We are keen to do the Forest Canopy Zipline.
Officer: Wonderful. The zipline group departs from Base Camp Station B at 10:15 am.
Customer: That sounds perfect. How much is the initial deposit to secure the booking?
Officer: The required deposit is £120, payable by card today."""

    s1_questions = [
        {"num": 1, "type": "Form Completion", "text": "Customer Surname: ________", "opts": [], "ans": "Henderson", "exp": "The customer spells his surname: H-E-N-D-E-R-S-O-N."},
        {"num": 2, "type": "Form Completion", "text": "Contact Phone: ________", "opts": [], "ans": "07911 802341", "exp": "The customer provides the mobile number 07911 802341."},
        {"num": 3, "type": "Form Completion", "text": "Check-in Date: ________ October", "opts": [], "ans": "18th", "exp": "Customer initially mentions 16th, then corrects to the 18th of October."},
        {"num": 4, "type": "Form Completion", "text": "Length of Stay: ________ nights", "opts": [], "ans": "4", "exp": "Customer confirms staying for 4 nights (checking out on the 22nd)."},
        {"num": 5, "type": "Form Completion", "text": "Accommodation Type: Pine Log ________", "opts": [], "ans": "Cabin", "exp": "Customer specifically selects the Pine Log Cabin."},
        {"num": 6, "type": "Form Completion", "text": "Dietary Requirement 1: Son has severe ________ allergy", "opts": [], "ans": "nut", "exp": "Son has a severe nut allergy."},
        {"num": 7, "type": "Form Completion", "text": "Dietary Requirement 2: Wife requires ________ breakfast", "opts": [], "ans": "dairy-free", "exp": "Wife is lactose-intolerant, requiring dairy-free meals."},
        {"num": 8, "type": "Form Completion", "text": "Weekend Excursion: Forest Canopy ________", "opts": [], "ans": "Zipline", "exp": "Customer books the Forest Canopy Zipline on Saturday morning."},
        {"num": 9, "type": "Form Completion", "text": "Departure Point: Base Camp Station ________", "opts": [], "ans": "B", "exp": "Officer confirms departure from Station B."},
        {"num": 10, "type": "Form Completion", "text": "Initial Deposit: £________", "opts": [], "ans": "120", "exp": "The holding deposit is £120."}
    ]

    # =========================================================================
    # PART 2 (Q11–20): Farley Estate Visitor Guide & Map Labelling (Monologue)
    # =========================================================================
    s2_title = "Part 2: Farley Estate & Historic Grounds Visitor Orientation"
    s2_instructions = "Questions 11–15: Choose the correct letter, A, B, or C. Questions 16–20: Label the map below. Write the correct letter, A–H, next to Questions 16–20."
    s2_context = """Guide: Good morning, everyone, and welcome to Farley House and Country Estate.
Before we begin our walking tour, please have a look at the estate map in your hands.
First, a few historical details about the property. The original estate house was constructed back in 1784 by the prominent textile merchant Sir Thomas Farley.
Today, the historic Stable Block on the western side has been completely renovated and now houses craft workshops where you can watch local artisans making pottery and traditional woodwork.
If you would like to join one of our specialized guided garden walks, these depart from the south terrace every 45 minutes throughout the afternoon.
Visitors often ask about our Farm Shop. Everything on sale there—from heirloom vegetables to herbal teas—is grown entirely inside our walled kitchen gardens on site.
Finally, for those visiting with younger children, please note that while the Adventure Playground is free to use, all children must be accompanied by an adult at all times for safety reasons.

Now, let me orient you with our grounds layout starting from where we are right now at the main Car Park by the south gate.
As you look north straight ahead of you up the main driveway, you can see the grand front facade of Farley House itself with the turning circle in front.
Now, if you take the path heading west, immediately to the east of the historic Stable Block, you will see our popular Farm Shop, marked on your map at letter A.
For visitors requiring wheelchair or step-free access, the dedicated Disabled Access Ramp is located along the western wall of the main house, right at letter B.
Next, if you look to the southeast corner of the estate, just to the right of the main entrance drive, you will find our newly built Adventure Playground at letter C.
Over in the northeast corner of the property, inside the large brick-walled enclosure with traditional planting beds, is the historic Kitchen Gardens at letter D.
And finally, standing on elevated ground in the north-centre behind the main house, you will spot the stone pillars of the Temple of the Four Winds at letter E.
Please feel free to explore the grounds, and remember that our staff at the information desk are always here to help."""

    s2_questions = [
        {"num": 11, "type": "Multiple Choice", "text": "When was the original Farley House constructed?", "opts": ["A) 1748", "B) 1784", "C) 1847"], "ans": "B) 1784", "exp": "The guide states the original house was built in 1784."},
        {"num": 12, "type": "Multiple Choice", "text": "What is currently located inside the historic Stable Block?", "opts": ["A) Craft workshops and local artisans", "B) An antique carriage exhibition", "C) An equestrian riding school"], "ans": "A) Craft workshops and local artisans", "exp": "The renovated stable block houses craft workshops with local artisans."},
        {"num": 13, "type": "Multiple Choice", "text": "How often do guided garden walks depart from the south terrace?", "opts": ["A) Every 15 minutes", "B) Every 30 minutes", "C) Every 45 minutes"], "ans": "C) Every 45 minutes", "exp": "Guided garden walks depart every 45 minutes throughout the afternoon."},
        {"num": 14, "type": "Multiple Choice", "text": "What is notable about the products sold in the Farm Shop?", "opts": ["A) They are imported from organic European farms", "B) They are grown entirely inside the walled gardens", "C) They are produced by local secondary school students"], "ans": "B) They are grown entirely inside the walled gardens", "exp": "The guide confirms all items are grown entirely inside the walled kitchen gardens."},
        {"num": 15, "type": "Multiple Choice", "text": "What rule applies to children using the Adventure Playground?", "opts": ["A) They must be accompanied by an adult", "B) They must wear protective safety helmets", "C) They must be over ten years of age"], "ans": "A) They must be accompanied by an adult", "exp": "All children must be accompanied by an adult at all times."},
        {"num": 16, "type": "Map Labelling", "text": "Farm shop", "opts": ["A", "B", "C", "D", "E", "F", "G", "H"], "ans": "A", "exp": "The Farm Shop is located immediately east of the Stable Block at letter A."},
        {"num": 17, "type": "Map Labelling", "text": "Disabled access ramp", "opts": ["A", "B", "C", "D", "E", "F", "G", "H"], "ans": "B", "exp": "The Disabled Access Ramp is on the western side of the main house at letter B."},
        {"num": 18, "type": "Map Labelling", "text": "Adventure playground", "opts": ["A", "B", "C", "D", "E", "F", "G", "H"], "ans": "C", "exp": "The Adventure Playground is in the southeast corner at letter C."},
        {"num": 19, "type": "Map Labelling", "text": "Kitchen gardens", "opts": ["A", "B", "C", "D", "E", "F", "G", "H"], "ans": "D", "exp": "The Kitchen Gardens are in the northeast walled enclosure at letter D."},
        {"num": 20, "type": "Map Labelling", "text": "Temple of the Four Winds", "opts": ["A", "B", "C", "D", "E", "F", "G", "H"], "ans": "E", "exp": "The Temple of the Four Winds with stone pillars is at letter E in the north-centre."}
    ]

    # =========================================================================
    # PART 3 (Q21–30): Academic Tutorial on Microgrids (Dialogue)
    # =========================================================================
    s3_title = "Part 3: Smart Decentralized Microgrids Academic Tutorial"
    s3_instructions = "Questions 21–25: Choose the correct letter, A, B, or C. Questions 26–30: Complete the sentences below. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each answer."
    s3_context = """Dr Evans: Good afternoon, Jack and Maya. Let's discuss your final-year engineering dissertation proposal on Decentralized Smart Microgrids. Jack, why did you decide to focus on decentralized distribution?
Jack: Well, Dr Evans, when analyzing national grid data, we found that traditional centralized transmission lines lose up to twelve percent of generated electricity through resistance over long distances. Decentralized microgrids generate power right where it's consumed.
Dr Evans: That's a solid rationale. Maya, what practical constraint did you identify when examining residential solar and battery systems?
Maya: The primary obstacle is still the high capital investment required for individual households. Even with government subsidies, payback periods often exceed nine years.
Dr Evans: Indeed. How do you plan to gather empirical data for your computational simulation?
Jack: Rather than relying on generic textbook estimates, we've secured permission to access smart meter telemetry logs from the eco-village in South Devon.
Dr Evans: Excellent. And regarding your literature review, what advice would you give them, Maya?
Maya: We should narrow our scope to recent regulatory frameworks adopted in northern Europe, especially Denmark and Germany, because their grid integration policies are the most mature.
Dr Evans: I agree. Jack, which operational aspect of grid stability will you model first?
Jack: I'll start by simulating frequency fluctuation during peak evening demand, when thousands of heat pumps and electric vehicles are connected simultaneously.

Dr Evans: Good plan. Now let's look at the technical specifications for your prototype model.
Maya: According to our sizing calculations, the backup lithium-iron battery bank needs to provide up to 6 hours of continuous reserve power during blackouts.
Jack: And we are writing a dynamic dispatch algorithm that will automatically balance supply and demand in real time across the fifty microgrid nodes.
Maya: When there is surplus solar energy during sunny midday periods, the excess power will be automatically redirected to local water heating systems rather than being wasted.
Jack: To address security vulnerabilities, we are implementing decentralized blockchain verification for all inter-node energy transactions.
Dr Evans: Very thorough. Keep in mind that your completed final dissertation draft must be submitted to the examination committee by the 15th of June."""

    s3_questions = [
        {"num": 21, "type": "Multiple Choice", "text": "Why did Jack choose decentralized microgrids as his research topic?", "opts": ["A) National energy grids rely too heavily on coal power", "B) Traditional centralized grids suffer high transmission losses", "C) Microgrids are significantly cheaper to construct initially"], "ans": "B) Traditional centralized grids suffer high transmission losses", "exp": "Jack explains centralized lines lose up to 12% of electricity through resistance."},
        {"num": 22, "type": "Multiple Choice", "text": "What major drawback of domestic battery storage did Maya highlight?", "opts": ["A) High capital investment costs for households", "B) Frequent maintenance and degradation issues", "C) Lack of compatibility with modern solar panels"], "ans": "A) High capital investment costs for households", "exp": "Maya identifies high capital investment as the main obstacle."},
        {"num": 23, "type": "Multiple Choice", "text": "How will the students obtain empirical data for their simulation model?", "opts": ["A) By conducting laboratory battery stress tests", "B) By surveying regional utility company engineers", "C) By using smart meter telemetry logs from an eco-village"], "ans": "C) By using smart meter telemetry logs from an eco-village", "exp": "Jack confirms they have permission to access telemetry logs from an eco-village."},
        {"num": 24, "type": "Multiple Choice", "text": "What recommendation is made concerning the literature review?", "opts": ["A) Compare global microgrid policies across fifty nations", "B) Focus on recent regulatory frameworks in northern Europe", "C) Review historical grid patents from the twentieth century"], "ans": "B) Focus on recent regulatory frameworks in northern Europe", "exp": "They agree to focus on northern European regulations (Denmark and Germany)."},
        {"num": 25, "type": "Multiple Choice", "text": "Which grid stability challenge will Jack simulate first?", "opts": ["A) Frequency fluctuation during peak evening demand", "B) Voltage drop caused by severe winter storms", "C) Overheating of local distribution transformers"], "ans": "A) Frequency fluctuation during peak evening demand", "exp": "Jack models frequency fluctuation during peak evening hours first."},
        {"num": 26, "type": "Sentence Completion", "text": "The backup lithium-iron battery bank provides up to ________ hours of reserve power.", "opts": [], "ans": "6", "exp": "Maya states the battery bank provides up to 6 hours of continuous reserve power."},
        {"num": 27, "type": "Sentence Completion", "text": "The dynamic dispatch algorithm balances supply and ________ in real time.", "opts": [], "ans": "demand", "exp": "The algorithm balances supply and demand in real time."},
        {"num": 28, "type": "Sentence Completion", "text": "Surplus midday solar energy is redirected to local ________ systems.", "opts": [], "ans": "water heating", "exp": "Excess solar power is used for local water heating."},
        {"num": 29, "type": "Sentence Completion", "text": "Transaction security is maintained using decentralized ________ verification.", "opts": [], "ans": "blockchain", "exp": "They use decentralized blockchain verification."},
        {"num": 30, "type": "Sentence Completion", "text": "The completed dissertation draft must be submitted by ________ June.", "opts": [], "ans": "15th", "exp": "Dr Evans confirms the submission deadline is the 15th of June."}
    ]

    # =========================================================================
    # PART 4 (Q31–40): University Academic Lecture on Marine Bioluminescence
    # =========================================================================
    s4_title = "Part 4: Marine Bioluminescence Academic Lecture"
    s4_instructions = "Complete the notes below. Write ONE WORD ONLY for each answer."
    s4_context = """Lecturer: Good afternoon, students. Today we are exploring the fascinating biological phenomenon of marine bioluminescence—the generation and emission of visible cold light by living oceanic organisms.
To begin with the chemical mechanics: bioluminescence occurs through an oxidation reaction catalyzed by an enzyme known as luciferase.
When luciferin combines with oxygen in the presence of this enzyme, light is emitted with remarkable efficiency—nearly ninety-five percent of the chemical energy is converted directly into light, producing virtually no heat.
In terms of spectral wavelength, over ninety percent of deep-sea bioluminescence occurs within the blue spectrum. This is because blue light penetrates deepest through seawater and matches the visual sensitivity of most marine animals.
Interestingly, while many organisms produce their own chemical luciferin, others obtain luminescence through symbiotic colonies of marine bacteria housed in specialized organs called photophores.

Now let's examine the primary ecological functions of bioluminescence in deep-water habitats.
The first major function is camouflage. In the twilight mesopelagic zone, predators hunt by looking upward for silhouettes against downwelling sunlight. Certain species of squid and hatchetfish utilize photophores on their ventral underside to match the light from above. This counterillumination effectively eliminates their silhouette.
A second critical function is prey capture. Deep-sea anglerfish possess an illuminated dorsal lure that dangles directly above their mouth, attracting curious prey in the pitch-black abyss.
Thirdly, bioluminescence serves as an effective predator deterrent. When disturbed, single-celled dinoflagellates emit sudden intense flashes to startle and distract approaching grazers.
Some jellyfish species even release clouds of glowing fluid as a chemical alarm, exposing the attacking predator to higher-level carnivores.

Finally, marine bioluminescence has inspired remarkable breakthroughs in modern scientific and industrial technology.
In environmental monitoring, genetically modified bioluminescent bacteria act as living biosensors to detect heavy metal pollution in freshwater rivers and industrial runoff.
In biotechnology and medical oncology, fluorescent proteins derived from luminescent marine species are widely used to tag and track the growth and migration of cancer cells in real time.
Looking forward, bioengineers are experimenting with bioluminescent plant genes to create glowing urban trees as a sustainable alternative to conventional street lighting."""

    s4_questions = [
        {"num": 31, "type": "Note Completion", "text": "Light reaction is catalyzed by an enzyme called ________", "opts": [], "ans": "luciferase", "exp": "The reaction is catalyzed by the enzyme luciferase."},
        {"num": 32, "type": "Note Completion", "text": "Most deep-sea organisms emit light in the ________ spectrum.", "opts": [], "ans": "blue", "exp": "Over 90% of bioluminescence occurs in the blue spectrum."},
        {"num": 33, "type": "Note Completion", "text": "Some creatures host luminescent marine ________ in photophores.", "opts": [], "ans": "bacteria", "exp": "Creatures obtain luminescence from symbiotic marine bacteria."},
        {"num": 34, "type": "Note Completion", "text": "Counterillumination hides an animal's ________ from predators below.", "opts": [], "ans": "silhouette", "exp": "Counterillumination eliminates the animal's silhouette."},
        {"num": 35, "type": "Note Completion", "text": "Anglerfish use a glowing lure to attract unsuspecting ________", "opts": [], "ans": "prey", "exp": "Anglerfish use a glowing lure to attract prey."},
        {"num": 36, "type": "Note Completion", "text": "Dinoflagellates produce sudden flashes to ________ approaching grazers.", "opts": [], "ans": "distract", "exp": "Flashes startle and distract approaching grazers."},
        {"num": 37, "type": "Note Completion", "text": "Jellyfish discharge glowing fluids that act as a burglar ________", "opts": [], "ans": "alarm", "exp": "The glowing fluid acts as a chemical alarm."},
        {"num": 38, "type": "Note Completion", "text": "Bioluminescent biosensors measure industrial ________ in waterways.", "opts": [], "ans": "pollution", "exp": "Biosensors detect heavy metal pollution in rivers and runoff."},
        {"num": 39, "type": "Note Completion", "text": "Fluorescent proteins help researchers track the spread of ________ cells.", "opts": [], "ans": "cancer", "exp": "Proteins track the growth and migration of cancer cells."},
        {"num": 40, "type": "Note Completion", "text": "Bioengineers are designing glowing trees for urban street ________", "opts": [], "ans": "lighting", "exp": "Glowing trees are being developed for urban street lighting."}
    ]

    # Insert all 4 sections into the database
    sections_to_insert = [
        (1, s1_title, s1_instructions, s1_context, s1_questions),
        (2, s2_title, s2_instructions, s2_context, s2_questions),
        (3, s3_title, s3_instructions, s3_context, s3_questions),
        (4, s4_title, s4_instructions, s4_context, s4_questions),
    ]

    for sec_num, sec_title, sec_inst, sec_context, q_list in sections_to_insert:
        for q in q_list:
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
                q.get('type', 'Note Completion'),
                sec_context,
                q.get('text', ''),
                json.dumps(q.get('opts', [])),
                q.get('ans', ''),
                q.get('exp', ''),
                'Medium',
                19,
                1,
                sec_num,
                '7.5',
                f"S{sec_num}_G1",
                sec_inst
            ))

    conn.commit()
    conn.close()
    print("[seed_full_cambridge_listening] Successfully seeded 40 authentic Cambridge 19 questions!")

if __name__ == "__main__":
    seed_full_cambridge_listening()
