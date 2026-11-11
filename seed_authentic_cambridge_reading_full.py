import sqlite3
import json

def insert_questions(cursor, questions):
    for q in questions:
        cursor.execute('''
            INSERT INTO questions (
                title, skill, test_type, section_number, question_type, 
                passage_or_context, question_text, options_json, answer_key, 
                explanation, difficulty, cambridge_book, test_number, 
                passage_or_section, difficulty_band, group_id, group_instructions
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            q.get('title', ''),
            'Reading',
            'Academic',
            q.get('section_number', 1),
            q.get('question_type', ''),
            q.get('passage_or_context', ''),
            q.get('question_text', ''),
            json.dumps(q.get('options_json', [])),
            q.get('answer_key', ''),
            q.get('explanation', ''),
            q.get('difficulty', 'Medium'),
            q.get('cambridge_book', 19),
            q.get('test_number', 1),
            q.get('passage_or_section', 1),
            q.get('difficulty_band', '6.5'),
            q.get('group_id', ''),
            q.get('group_instructions', '')
        ))

def get_set_a_questions():
    passage_1a = """
The History of Chocolate: From Ancient Mesoamerica to Modern Industry

A. The story of chocolate begins in Mesoamerica, where the cacao tree is native. Archaeological evidence suggests that the Olmec civilization, which flourished in the southern Gulf Coast of Mexico between 1500 BC and 400 BC, were the first humans to consume chocolate. They used it initially in the form of a bitter beverage. Later, the Mayans and Aztecs adopted the practice. For these ancient civilizations, cacao was not merely a source of food; it held profound spiritual and economic significance. Cacao beans were used as currency, and the drink made from them was reserved for royalty, priests, and successful warriors. The Aztec emperor Montezuma II was reputed to consume dozens of goblets of the frothy, bitter chocolate drink each day, flavored with chili peppers and vanilla.

B. When Spanish conquistadors, led by Hernán Cortés, arrived in the Aztec empire in the early 16th century, they encountered this peculiar beverage. Initially met with distaste due to its bitterness, the Spaniards soon discovered that adding sugar and honey made it far more palatable to European tastes. Cortés recognized the economic potential of cacao and established plantations in the conquered territories. The secret of chocolate was kept mostly within Spain for nearly a century before it gradually spread to other European courts, becoming a fashionable luxury among the aristocracy. The process of making chocolate remained labor-intensive, ensuring it stayed an exclusive commodity for the wealthy.

C. The industrial revolution in the 18th and 19th centuries transformed chocolate from a rare luxury into a mass-market commodity. In 1828, a Dutch chemist named Coenraad Johannes van Houten invented the cocoa press. This device squeezed out the fatty cocoa butter from roasted cacao beans, leaving a dry cake that could be pulverized into a fine powder—what we now know as cocoa powder. This innovation made it much easier to mix chocolate with water or milk, significantly reducing production costs. It also paved the way for the creation of solid chocolate.

D. The final major evolution in chocolate's history occurred in 1847, when Joseph Fry, a British chocolatier, discovered that by adding melted cocoa butter back into Dutch cocoa, he could create a moldable chocolate paste. This was the world's first modern chocolate bar. Later, in 1875, Daniel Peter, a Swiss chocolatier, revolutionized the industry again by adding powdered milk—invented by his neighbor Henri Nestlé—to the chocolate mix, thus creating milk chocolate. These innovations dramatically altered the texture and taste of chocolate, propelling it to unprecedented global popularity. Today, the chocolate industry is a multibillion-dollar global enterprise, although it faces ongoing challenges related to sustainability and fair labor practices in cacao-producing regions.
"""

    passage_2a = """
Urban Vertical Farming and the Future of Food Security

A. As the global population steadily marches towards a projected 9.7 billion by 2050, the challenge of feeding humanity is becoming increasingly acute. Traditional agriculture is facing unprecedented pressures: arable land is diminishing due to urbanization and soil degradation, freshwater resources are depleting, and climate change is causing unpredictable weather patterns that disrupt crop yields. In response to these existential threats, agricultural scientists and urban planners are increasingly turning their attention to innovative solutions, with vertical farming emerging as one of the most promising paradigms.

B. Vertical farming is the practice of producing food in vertically stacked layers, typically integrated into other structures like skyscrapers, shipping containers, or repurposed warehouses. Unlike traditional farming, which relies on vast expanses of land, vertical farms utilize Controlled Environment Agriculture (CEA) technology. This involves meticulously managing variables such as temperature, humidity, light, and nutrient delivery to optimize plant growth. By isolating crops from external environmental factors, vertical farms can achieve year-round production, immune to droughts, floods, or unseasonal frosts.

C. The environmental benefits of vertical farming are substantial. Most notably, it dramatically reduces water consumption. Traditional agriculture accounts for roughly 70% of global freshwater withdrawals. Vertical farms, primarily utilizing hydroponic or aeroponic systems, can use up to 95% less water than conventional soil-based farming by capturing and recycling transpired moisture. Furthermore, by locating food production within or adjacent to urban centers, vertical farming significantly curtails the 'food miles'—the distance food travels from farm to plate. This localized production drastically reduces greenhouse gas emissions associated with transportation and cold storage logistics.

D. Despite its immense potential, vertical farming is not without significant challenges. The most pressing issue is the exorbitant initial capital expenditure required to establish a facility. The technology—LED lighting systems, climate control sensors, and automated nutrient delivery mechanisms—is costly. Moreover, the operational energy demand, primarily for artificial lighting, remains a major hurdle. While LED efficiency has improved remarkably, the energy footprint of a large-scale vertical farm is considerable, leading critics to question its overall environmental sustainability if the energy source is not renewable. Proponents argue that as renewable energy becomes cheaper and more prevalent, this energy paradox will resolve itself, making vertical farming a critical component of resilient future food systems.
"""

    passage_3a = """
Neuroplasticity and the Adaptive Human Brain

The human brain, once thought to be a static organ whose structure was largely fixed in childhood, is now understood to be remarkably malleable. This extraordinary ability of the nervous system to change its activity in response to intrinsic or extrinsic stimuli by reorganizing its structure, functions, or connections is known as neuroplasticity.

In the mid-20th century, the prevailing scientific consensus maintained that the adult brain was essentially hardwired. It was believed that after a critical developmental period in early life, the brain lost its capacity to generate new neurons or forge new neural pathways. However, pioneering research by Dr. Michael Merzenich in the 1980s began to dismantle this dogma. Merzenich's experiments with primates demonstrated that the brain's sensory maps—the areas of the cortex that correspond to specific body parts—were not immutable. When a primate's finger was amputated, the cortical area previously dedicated to that digit did not go dormant; instead, it was 'colonized' by the neural networks representing the adjacent fingers.

Another pivotal study illuminating neuroplasticity was conducted by Eleanor Maguire in 2000, involving London taxi drivers. To obtain their licenses, these drivers must pass 'The Knowledge,' a grueling examination requiring them to memorize the labyrinthine streets of the city. Maguire used functional magnetic resonance imaging (fMRI) to scan the brains of licensed taxi drivers and found that their posterior hippocampi—a region crucial for spatial memory and navigation—were significantly larger than those of control subjects. Crucially, the size of the posterior hippocampus correlated positively with the amount of time the driver had spent on the job, providing compelling evidence that intensive cognitive training can induce structural changes in the adult human brain.

Neuroplasticity manifests in two primary forms: functional and structural. Functional plasticity refers to the brain's ability to shift functions from a damaged area to an undamaged one, a phenomenon frequently observed in stroke survivors undergoing rehabilitation. Structural plasticity, on the other hand, involves the brain physically changing its physical structure as a result of learning or experiencing something new. Every time we learn a new skill, whether it's playing the piano or acquiring a second language, our brain physically rewires itself, strengthening synaptic connections between neurons that communicate frequently.

While neuroplasticity underpins our capacity for lifelong learning and recovery from brain injury, it is a double-edged sword. Just as the brain can adapt in beneficial ways, it can also become entrenched in maladaptive patterns. For instance, chronic stress or trauma can alter neural architecture, shrinking areas like the prefrontal cortex, which governs executive function, while enlarging the amygdala, the brain's fear center. Similarly, addiction hijacking the brain's reward pathways is a form of negative neuroplasticity.

The burgeoning field of neuroplasticity holds immense therapeutic promise. Researchers are exploring non-invasive brain stimulation techniques, such as transcranial magnetic stimulation (TMS), to intentionally induce neuroplastic changes to treat conditions ranging from major depressive disorder to chronic pain. As our understanding of the brain's adaptive mechanisms deepens, it becomes increasingly clear that we are not merely passive recipients of our neurobiology; rather, through deliberate practice and focused attention, we have the capacity to actively sculpt the structure and function of our own minds.
"""

    questions_set_a = [
        # Passage 1 - T/F/NG
        {
            "title": "History of Chocolate",
            "section_number": 1,
            "question_type": "True / False / Not Given",
            "passage_or_context": passage_1a,
            "question_text": "The Olmec civilization consumed chocolate primarily as a sweet food.",
            "options_json": ["True", "False", "Not Given"],
            "answer_key": "False",
            "explanation": "Paragraph A states they used it 'in the form of a bitter beverage'.",
            "group_id": "P1_G1",
            "group_instructions": "Do the following statements agree with the information given in Reading Passage 1?\nWrite TRUE, FALSE or NOT GIVEN."
        },
        {
            "title": "History of Chocolate",
            "section_number": 1,
            "question_type": "True / False / Not Given",
            "passage_or_context": passage_1a,
            "question_text": "Cacao beans were utilized as a form of money by the ancient civilizations.",
            "options_json": ["True", "False", "Not Given"],
            "answer_key": "True",
            "explanation": "Paragraph A mentions: 'Cacao beans were used as currency'.",
            "group_id": "P1_G1",
            "group_instructions": ""
        },
        {
            "title": "History of Chocolate",
            "section_number": 1,
            "question_type": "True / False / Not Given",
            "passage_or_context": passage_1a,
            "question_text": "Montezuma II prepared his own chocolate drink every day.",
            "options_json": ["True", "False", "Not Given"],
            "answer_key": "Not Given",
            "explanation": "The text says he consumed dozens of goblets, but not who prepared it.",
            "group_id": "P1_G1",
            "group_instructions": ""
        },
        {
            "title": "History of Chocolate",
            "section_number": 1,
            "question_type": "True / False / Not Given",
            "passage_or_context": passage_1a,
            "question_text": "The Spanish conquerors immediately enjoyed the taste of the Aztec chocolate beverage.",
            "options_json": ["True", "False", "Not Given"],
            "answer_key": "False",
            "explanation": "Paragraph B states it was 'Initially met with distaste due to its bitterness'.",
            "group_id": "P1_G1",
            "group_instructions": ""
        },
        {
            "title": "History of Chocolate",
            "section_number": 1,
            "question_type": "True / False / Not Given",
            "passage_or_context": passage_1a,
            "question_text": "Spain kept the recipe for the sweetened chocolate drink secret from the rest of Europe for almost 100 years.",
            "options_json": ["True", "False", "Not Given"],
            "answer_key": "True",
            "explanation": "Paragraph B states 'The secret of chocolate was kept mostly within Spain for nearly a century'.",
            "group_id": "P1_G1",
            "group_instructions": ""
        },
        # Passage 1 - Short Answer
        {
            "title": "History of Chocolate",
            "section_number": 1,
            "question_type": "Short Answer Questions",
            "passage_or_context": passage_1a,
            "question_text": "What piece of equipment, invented in 1828, changed chocolate production?",
            "options_json": [],
            "answer_key": "cocoa press",
            "explanation": "Paragraph C mentions 'a Dutch chemist named Coenraad Johannes van Houten invented the cocoa press.'",
            "group_id": "P1_G2",
            "group_instructions": "Choose NO MORE THAN THREE WORDS from the passage for each answer."
        },
        {
            "title": "History of Chocolate",
            "section_number": 1,
            "question_type": "Short Answer Questions",
            "passage_or_context": passage_1a,
            "question_text": "What type of product was created by Joseph Fry in 1847?",
            "options_json": [],
            "answer_key": "chocolate bar",
            "explanation": "Paragraph D states he created a moldable paste, 'the world's first modern chocolate bar'.",
            "group_id": "P1_G2",
            "group_instructions": ""
        },
        {
            "title": "History of Chocolate",
            "section_number": 1,
            "question_type": "Short Answer Questions",
            "passage_or_context": passage_1a,
            "question_text": "What ingredient was added to chocolate by Daniel Peter to create a new product?",
            "options_json": [],
            "answer_key": "powdered milk",
            "explanation": "Paragraph D states Daniel Peter 'revolutionary... by adding powdered milk'.",
            "group_id": "P1_G2",
            "group_instructions": ""
        },
        # Passage 1 - Table Completion
        {
            "title": "History of Chocolate",
            "section_number": 1,
            "question_type": "Table Completion",
            "passage_or_context": passage_1a,
            "question_text": "Aztec Chocolate: Flavored with vanilla and [Q9].",
            "options_json": [],
            "answer_key": "chili peppers",
            "explanation": "Paragraph A states flavored with chili peppers and vanilla.",
            "group_id": "P1_G3",
            "group_instructions": "Complete the table below. Choose ONE WORD ONLY from the passage."
        },
        {
            "title": "History of Chocolate",
            "section_number": 1,
            "question_type": "Table Completion",
            "passage_or_context": passage_1a,
            "question_text": "Aztec Chocolate: Status: Consumed mostly by [Q10], priests, and warriors.",
            "options_json": [],
            "answer_key": "royalty",
            "explanation": "Paragraph A says reserved for royalty, priests, and successful warriors.",
            "group_id": "P1_G3",
            "group_instructions": ""
        },
        {
            "title": "History of Chocolate",
            "section_number": 1,
            "question_type": "Table Completion",
            "passage_or_context": passage_1a,
            "question_text": "European Chocolate: Flavored with honey and [Q11] to make it palatable.",
            "options_json": [],
            "answer_key": "sugar",
            "explanation": "Paragraph B states adding sugar and honey made it far more palatable.",
            "group_id": "P1_G3",
            "group_instructions": ""
        },
        {
            "title": "History of Chocolate",
            "section_number": 1,
            "question_type": "Table Completion",
            "passage_or_context": passage_1a,
            "question_text": "European Chocolate: Status: Seen as a fashionable [Q12] by the aristocracy.",
            "options_json": [],
            "answer_key": "luxury",
            "explanation": "Paragraph B mentions 'becoming a fashionable luxury among the aristocracy'.",
            "group_id": "P1_G3",
            "group_instructions": ""
        },
        {
            "title": "History of Chocolate",
            "section_number": 1,
            "question_type": "Table Completion",
            "passage_or_context": passage_1a,
            "question_text": "19th Century Change: Transitioned from an exclusive item into a mass-market [Q13].",
            "options_json": [],
            "answer_key": "commodity",
            "explanation": "Paragraph C says 'transformed chocolate from a rare luxury into a mass-market commodity'.",
            "group_id": "P1_G3",
            "group_instructions": ""
        },
        
        # Passage 2 - Matching Headings
        {
            "title": "Urban Vertical Farming",
            "section_number": 2,
            "question_type": "Matching Headings",
            "passage_or_context": passage_2a,
            "question_text": "Paragraph A",
            "options_json": ["i. Addressing the financial and energy costs", "ii. The role of natural sunlight in plant growth", "iii. Ecological advantages and resource efficiency", "iv. Global pressures necessitating agricultural innovation", "v. The mechanics and environment of stacked agriculture", "vi. Government subsidies for urban farmers", "vii. Historical failures of vertical farms"],
            "answer_key": "iv",
            "explanation": "Paragraph A discusses population growth, land degradation, and the need for innovation.",
            "group_id": "P2_G1",
            "group_instructions": "Choose the correct heading for each paragraph from the list of headings below."
        },
        {
            "title": "Urban Vertical Farming",
            "section_number": 2,
            "question_type": "Matching Headings",
            "passage_or_context": passage_2a,
            "question_text": "Paragraph B",
            "options_json": ["i. Addressing the financial and energy costs", "ii. The role of natural sunlight in plant growth", "iii. Ecological advantages and resource efficiency", "iv. Global pressures necessitating agricultural innovation", "v. The mechanics and environment of stacked agriculture", "vi. Government subsidies for urban farmers", "vii. Historical failures of vertical farms"],
            "answer_key": "v",
            "explanation": "Paragraph B explains how vertical farming works, using CEA technology in stacked layers.",
            "group_id": "P2_G1",
            "group_instructions": ""
        },
        {
            "title": "Urban Vertical Farming",
            "section_number": 2,
            "question_type": "Matching Headings",
            "passage_or_context": passage_2a,
            "question_text": "Paragraph C",
            "options_json": ["i. Addressing the financial and energy costs", "ii. The role of natural sunlight in plant growth", "iii. Ecological advantages and resource efficiency", "iv. Global pressures necessitating agricultural innovation", "v. The mechanics and environment of stacked agriculture", "vi. Government subsidies for urban farmers", "vii. Historical failures of vertical farms"],
            "answer_key": "iii",
            "explanation": "Paragraph C details water savings and reduced food miles (ecological advantages).",
            "group_id": "P2_G1",
            "group_instructions": ""
        },
        {
            "title": "Urban Vertical Farming",
            "section_number": 2,
            "question_type": "Matching Headings",
            "passage_or_context": passage_2a,
            "question_text": "Paragraph D",
            "options_json": ["i. Addressing the financial and energy costs", "ii. The role of natural sunlight in plant growth", "iii. Ecological advantages and resource efficiency", "iv. Global pressures necessitating agricultural innovation", "v. The mechanics and environment of stacked agriculture", "vi. Government subsidies for urban farmers", "vii. Historical failures of vertical farms"],
            "answer_key": "i",
            "explanation": "Paragraph D discusses exorbitant capital expenditure and operational energy demand.",
            "group_id": "P2_G1",
            "group_instructions": ""
        },
        
        # Passage 2 - Matching Information
        {
            "title": "Urban Vertical Farming",
            "section_number": 2,
            "question_type": "Matching Information",
            "passage_or_context": passage_2a,
            "question_text": "A mention of a specific percentage regarding water usage reduction.",
            "options_json": ["A", "B", "C", "D"],
            "answer_key": "C",
            "explanation": "Paragraph C states vertical farms can use up to 95% less water.",
            "group_id": "P2_G2",
            "group_instructions": "Which paragraph contains the following information? You may use any letter more than once."
        },
        {
            "title": "Urban Vertical Farming",
            "section_number": 2,
            "question_type": "Matching Information",
            "passage_or_context": passage_2a,
            "question_text": "A reference to the dependence of vertical farms on artificial power sources.",
            "options_json": ["A", "B", "C", "D"],
            "answer_key": "D",
            "explanation": "Paragraph D mentions the operational energy demand, primarily for artificial lighting.",
            "group_id": "P2_G2",
            "group_instructions": ""
        },
        {
            "title": "Urban Vertical Farming",
            "section_number": 2,
            "question_type": "Matching Information",
            "passage_or_context": passage_2a,
            "question_text": "An explanation of how traditional farming is threatened by shifting climatic conditions.",
            "options_json": ["A", "B", "C", "D"],
            "answer_key": "A",
            "explanation": "Paragraph A states 'climate change is causing unpredictable weather patterns that disrupt crop yields.'",
            "group_id": "P2_G2",
            "group_instructions": ""
        },
        {
            "title": "Urban Vertical Farming",
            "section_number": 2,
            "question_type": "Matching Information",
            "passage_or_context": passage_2a,
            "question_text": "The concept that crops can be grown continuously regardless of the season.",
            "options_json": ["A", "B", "C", "D"],
            "answer_key": "B",
            "explanation": "Paragraph B states they can achieve year-round production.",
            "group_id": "P2_G2",
            "group_instructions": ""
        },
        
        # Passage 2 - Multiple Choice (Single)
        {
            "title": "Urban Vertical Farming",
            "section_number": 2,
            "question_type": "Multiple Choice",
            "passage_or_context": passage_2a,
            "question_text": "According to the passage, the primary reason for reducing 'food miles' is to:",
            "options_json": ["A. Ensure produce is fresher upon arrival.", "B. Cut greenhouse gas emissions from transportation.", "C. Eliminate the need for chemical preservatives.", "D. Support local rural economies."],
            "answer_key": "B",
            "explanation": "Paragraph C states 'localized production drastically reduces greenhouse gas emissions associated with transportation'.",
            "group_id": "P2_G3",
            "group_instructions": "Choose the correct letter, A, B, C or D."
        },
        {
            "title": "Urban Vertical Farming",
            "section_number": 2,
            "question_type": "Multiple Choice",
            "passage_or_context": passage_2a,
            "question_text": "Critics of vertical farming often point out that it may not be environmentally sustainable if:",
            "options_json": ["A. It uses too much water.", "B. It relies on non-renewable energy sources.", "C. It takes up too much urban real estate.", "D. It produces crops that lack nutritional value."],
            "answer_key": "B",
            "explanation": "Paragraph D says critics question sustainability 'if the energy source is not renewable'.",
            "group_id": "P2_G3",
            "group_instructions": ""
        },
        
        # Passage 2 - Sentence Completion
        {
            "title": "Urban Vertical Farming",
            "section_number": 2,
            "question_type": "Sentence Completion",
            "passage_or_context": passage_2a,
            "question_text": "Vertical farms manage variables using a technology known as [Q24].",
            "options_json": [],
            "answer_key": "Controlled Environment",
            "explanation": "Paragraph B mentions 'Controlled Environment Agriculture (CEA) technology'.",
            "group_id": "P2_G4",
            "group_instructions": "Complete the sentences below. Choose NO MORE THAN TWO WORDS from the passage."
        },
        {
            "title": "Urban Vertical Farming",
            "section_number": 2,
            "question_type": "Sentence Completion",
            "passage_or_context": passage_2a,
            "question_text": "Hydroponic and aeroponic systems save water by recycling [Q25].",
            "options_json": [],
            "answer_key": "transpired moisture",
            "explanation": "Paragraph C states 'by capturing and recycling transpired moisture'.",
            "group_id": "P2_G4",
            "group_instructions": ""
        },
        {
            "title": "Urban Vertical Farming",
            "section_number": 2,
            "question_type": "Sentence Completion",
            "passage_or_context": passage_2a,
            "question_text": "The main obstacle to setting up a vertical farm is the [Q26].",
            "options_json": [],
            "answer_key": "capital expenditure",
            "explanation": "Paragraph D states 'The most pressing issue is the exorbitant initial capital expenditure'.",
            "group_id": "P2_G4",
            "group_instructions": ""
        },

        # Passage 3 - Y/N/NG
        {
            "title": "Neuroplasticity",
            "section_number": 3,
            "question_type": "Yes / No / Not Given",
            "passage_or_context": passage_3a,
            "question_text": "Before the 1980s, scientists generally agreed that the adult human brain could not form new neural pathways.",
            "options_json": ["Yes", "No", "Not Given"],
            "answer_key": "Yes",
            "explanation": "The text says in the mid-20th century the consensus was that the adult brain was hardwired and lost the capacity to forge new neural pathways.",
            "group_id": "P3_G1",
            "group_instructions": "Do the following statements agree with the views of the writer in Reading Passage 3?\nWrite YES, NO or NOT GIVEN."
        },
        {
            "title": "Neuroplasticity",
            "section_number": 3,
            "question_type": "Yes / No / Not Given",
            "passage_or_context": passage_3a,
            "question_text": "Michael Merzenich was the first scientist to use fMRI in neuroplasticity research.",
            "options_json": ["Yes", "No", "Not Given"],
            "answer_key": "Not Given",
            "explanation": "The text mentions Maguire used fMRI, but doesn't say if Merzenich used it or who was first.",
            "group_id": "P3_G1",
            "group_instructions": ""
        },
        {
            "title": "Neuroplasticity",
            "section_number": 3,
            "question_type": "Yes / No / Not Given",
            "passage_or_context": passage_3a,
            "question_text": "When a primate loses a finger, the brain region representing that finger becomes completely inactive.",
            "options_json": ["Yes", "No", "Not Given"],
            "answer_key": "No",
            "explanation": "The text says 'the cortical area... did not go dormant; instead, it was 'colonized' by the neural networks representing the adjacent fingers.'",
            "group_id": "P3_G1",
            "group_instructions": ""
        },
        {
            "title": "Neuroplasticity",
            "section_number": 3,
            "question_type": "Yes / No / Not Given",
            "passage_or_context": passage_3a,
            "question_text": "London taxi drivers with more years of experience tended to have larger posterior hippocampi.",
            "options_json": ["Yes", "No", "Not Given"],
            "answer_key": "Yes",
            "explanation": "The text states 'the size of the posterior hippocampus correlated positively with the amount of time the driver had spent on the job'.",
            "group_id": "P3_G1",
            "group_instructions": ""
        },
        {
            "title": "Neuroplasticity",
            "section_number": 3,
            "question_type": "Yes / No / Not Given",
            "passage_or_context": passage_3a,
            "question_text": "Functional plasticity is more common in younger stroke survivors than older ones.",
            "options_json": ["Yes", "No", "Not Given"],
            "answer_key": "Not Given",
            "explanation": "Age of stroke survivors is not discussed in relation to functional plasticity frequency.",
            "group_id": "P3_G1",
            "group_instructions": ""
        },
        
        # Passage 3 - Matching Features
        {
            "title": "Neuroplasticity",
            "section_number": 3,
            "question_type": "Matching Features",
            "passage_or_context": passage_3a,
            "question_text": "Demonstrated that sensory maps in the brain can physically reorganize after limb loss.",
            "options_json": ["A. Michael Merzenich", "B. Eleanor Maguire", "C. Stroke survivors", "D. Both A and B"],
            "answer_key": "A",
            "explanation": "Merzenich did the primate finger amputation study.",
            "group_id": "P3_G2",
            "group_instructions": "Match each finding with the correct researcher or subject group."
        },
        {
            "title": "Neuroplasticity",
            "section_number": 3,
            "question_type": "Matching Features",
            "passage_or_context": passage_3a,
            "question_text": "Provided evidence that extensive spatial navigation training alters brain structure.",
            "options_json": ["A. Michael Merzenich", "B. Eleanor Maguire", "C. Stroke survivors", "D. Both A and B"],
            "answer_key": "B",
            "explanation": "Maguire did the taxi driver study.",
            "group_id": "P3_G2",
            "group_instructions": ""
        },
        {
            "title": "Neuroplasticity",
            "section_number": 3,
            "question_type": "Matching Features",
            "passage_or_context": passage_3a,
            "question_text": "Showed examples of functional plasticity by shifting tasks to undamaged brain areas.",
            "options_json": ["A. Michael Merzenich", "B. Eleanor Maguire", "C. Stroke survivors", "D. Both A and B"],
            "answer_key": "C",
            "explanation": "The text mentions stroke survivors as examples of functional plasticity.",
            "group_id": "P3_G2",
            "group_instructions": ""
        },
        {
            "title": "Neuroplasticity",
            "section_number": 3,
            "question_type": "Matching Features",
            "passage_or_context": passage_3a,
            "question_text": "Their research helped to disprove the idea that the adult brain is entirely 'hardwired'.",
            "options_json": ["A. Michael Merzenich", "B. Eleanor Maguire", "C. Stroke survivors", "D. Both A and B"],
            "answer_key": "D",
            "explanation": "Both scientists provided key evidence against the hardwired dogma.",
            "group_id": "P3_G2",
            "group_instructions": ""
        },
        
        # Passage 3 - Multiple Choice (Select TWO)
        {
            "title": "Neuroplasticity",
            "section_number": 3,
            "question_type": "Multiple Choice",
            "passage_or_context": passage_3a,
            "question_text": "Which TWO of the following are examples of maladaptive (negative) neuroplasticity mentioned in the text?",
            "options_json": ["A. The enlargement of the posterior hippocampus", "B. The shrinking of the prefrontal cortex due to trauma", "C. The 'colonization' of sensory maps", "D. The strengthening of synapses during language learning", "E. Addiction altering reward pathways"],
            "answer_key": "B, E",
            "explanation": "The text mentions chronic stress shrinking the prefrontal cortex and addiction hijacking reward pathways as negative plasticity.",
            "group_id": "P3_G3",
            "group_instructions": "Choose TWO letters, A-E."
        },
        {
            "title": "Neuroplasticity",
            "section_number": 3,
            "question_type": "Multiple Choice",
            "passage_or_context": passage_3a,
            "question_text": "Which TWO methods are mentioned as ways to induce neuroplastic changes intentionally?",
            "options_json": ["A. Transcranial magnetic stimulation (TMS)", "B. Amputating adjacent digits", "C. Memorizing labyrinthine streets", "D. Deliberate practice and focused attention", "E. Shrinking the amygdala through surgery"],
            "answer_key": "A, D",
            "explanation": "The text mentions TMS and deliberate practice/focused attention as ways to intentionally shape the brain.",
            "group_id": "P3_G4",
            "group_instructions": "Choose TWO letters, A-E."
        },
        
        # Passage 3 - Summary Completion (Word Bank)
        {
            "title": "Neuroplasticity",
            "section_number": 3,
            "question_type": "Summary Completion",
            "passage_or_context": passage_3a,
            "question_text": "Neuroplasticity refers to the brain's ability to adapt its [Q38].",
            "options_json": ["A. size", "B. structure", "C. memories", "D. rigid", "E. fluid", "F. negative", "G. sensory", "H. therapies"],
            "answer_key": "B",
            "explanation": "The text says 'reorganizing its structure, functions, or connections'.",
            "group_id": "P3_G5",
            "group_instructions": "Complete the summary using the list of words, A-H, below."
        },
        {
            "title": "Neuroplasticity",
            "section_number": 3,
            "question_type": "Summary Completion",
            "passage_or_context": passage_3a,
            "question_text": "While historically the brain was viewed as [Q39], modern research proves otherwise.",
            "options_json": ["A. size", "B. structure", "C. memories", "D. rigid", "E. fluid", "F. negative", "G. sensory", "H. therapies"],
            "answer_key": "D",
            "explanation": "The text states it was thought to be 'static' or 'hardwired' (rigid).",
            "group_id": "P3_G5",
            "group_instructions": ""
        },
        {
            "title": "Neuroplasticity",
            "section_number": 3,
            "question_type": "Summary Completion",
            "passage_or_context": passage_3a,
            "question_text": "This adaptability can be harnessed for beneficial [Q40], but can also result in harmful conditions like addiction.",
            "options_json": ["A. size", "B. structure", "C. memories", "D. rigid", "E. fluid", "F. negative", "G. sensory", "H. therapies"],
            "answer_key": "H",
            "explanation": "The text says it holds 'immense therapeutic promise' (therapies).",
            "group_id": "P3_G5",
            "group_instructions": ""
        },
    ]
    return questions_set_a

def seed_full_cambridge_reading():
    conn = sqlite3.connect('ielts_platform.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM questions WHERE skill = 'Reading'")
    insert_questions(cursor, get_set_a_questions())
    conn.commit()
    conn.close()

def get_set_b_questions():
    # SET B PASSAGES
    passage_1b = """
The Science of Sleep: Circadian Rhythms and Cognitive Performance

A. For decades, the biological imperative of sleep remained one of science's most profound mysteries. While it was empirically evident that humans require sleep to function, the precise physiological mechanisms and evolutionary advantages were poorly understood. Today, advancements in neuroscience have illuminated the complex architecture of sleep, revealing it to be a highly active, orchestrated state vital for cognitive maintenance, memory consolidation, and overall health. Central to this architecture is the circadian rhythm, a roughly 24-hour internal clock governed by the suprachiasmatic nucleus (SCN) in the brain's hypothalamus.

B. The SCN is exquisitely sensitive to environmental cues, most notably light. When retinal ganglion cells detect morning sunlight, they transmit signals to the SCN, which in turn suppresses the pineal gland's production of melatonin, a hormone that promotes sleepiness. Conversely, as darkness falls, melatonin secretion rises, signaling to the body that it is time to rest. This delicate chronobiological dance aligns our physiological processes with the Earth's day-night cycle. Disruptions to this rhythm—such as those caused by shift work, jet lag, or excessive exposure to blue light from electronic devices at night—can have profound negative consequences on cognitive performance and metabolic health.

C. Sleep itself is not a uniform state but is divided into distinct cycles, typically lasting 90 to 110 minutes, which repeat several times a night. These cycles comprise two main types of sleep: Non-Rapid Eye Movement (NREM) and Rapid Eye Movement (REM) sleep. NREM sleep is further subdivided into three stages. Stage 1 is the transition from wakefulness to light sleep. Stage 2 features the appearance of sleep spindles and K-complexes on an EEG, signifying deeper relaxation. Stage 3, often called slow-wave sleep (SWS), is the deepest restorative phase. During SWS, heart rate and respiration drop to their lowest levels, and the body engages in critical tissue repair and immune system strengthening.

D. Following the NREM stages, the brain enters REM sleep. Unlike the deep physiological relaxation of NREM, REM sleep is characterized by brain wave activity that paradoxically resembles wakefulness. This phase is when the most vivid dreaming occurs. Crucially, REM sleep is deeply implicated in memory consolidation and emotional regulation. During REM, the brain selectively strengthens neural connections related to newly acquired information while pruning irrelevant synapses. A chronic lack of REM sleep has been strongly correlated with cognitive deficits, mood disorders, and impaired learning capacity, underscoring that quality of sleep is just as critical as quantity.
"""

    passage_2b = """
Coral Reef Ecosystems and Climate Change

A. Coral reefs, often colloquially termed the "rainforests of the sea," are among the most biodiverse and productive ecosystems on Earth. Covering less than 0.1% of the ocean floor, they support roughly 25% of all marine species. These intricate structures are built by colonies of tiny animals called polyps. The polyps secrete calcium carbonate to form a hard exoskeleton, which accumulates over millennia to create vast reef structures. The foundation of this ecosystem's success is a remarkable symbiotic relationship between the coral polyps and microscopic, photosynthetic algae called zooxanthellae, which reside within the coral's tissues.

B. The zooxanthellae provide their hosts with essential nutrients produced through photosynthesis, supplying up to 90% of the coral's energy requirements. In return, the coral provides the algae with a protected environment and the compounds necessary for photosynthesis. This mutualistic exchange is highly efficient but also exceptionally fragile. It operates within a narrow window of environmental conditions, particularly concerning water temperature and quality. When these parameters are disrupted, the delicate balance collapses, leading to a phenomenon known as coral bleaching.

C. Climate change is the most severe and immediate threat to coral reefs globally. Anthropogenic greenhouse gas emissions have caused ocean temperatures to rise significantly over the past century. When waters become unusually warm—even by just 1 or 2 degrees Celsius above the normal summer maximum—corals experience severe physiological stress. In response, they expel the zooxanthellae. Because these algae give corals their vibrant colors, their expulsion leaves the coral's white calcium carbonate skeleton visible, hence the term "bleaching." While a bleached coral is not immediately dead, it is severely compromised, stripped of its primary food source, and highly susceptible to disease and starvation.

D. If water temperatures return to normal relatively quickly, corals can reabsorb zooxanthellae and recover. However, the increasing frequency and intensity of marine heatwaves mean that reefs often lack the necessary recovery time between bleaching events. The mass bleaching events on Australia's Great Barrier Reef in recent years highlight the devastating scale of this problem. Furthermore, climate change exacerbates ocean acidification. As the oceans absorb excess carbon dioxide from the atmosphere, the water's pH lowers. This more acidic environment makes it exceedingly difficult for corals to calcify and build their protective skeletons, threatening the long-term structural integrity of the reefs and the myriads of species that rely on them.
"""

    passage_3b = """
The Economics of Renewable Energy Transition

A. The global transition from fossil fuels to renewable energy sources is arguably the most significant economic and technological shift of the 21st century. Driven primarily by the urgent need to mitigate anthropogenic climate change, this transition is fundamentally reshaping energy markets, geopolitics, and global investment strategies. Historically, fossil fuels—coal, oil, and natural gas—have dominated the energy landscape due to their high energy density, dispatchability, and established infrastructure. However, the negative externalities associated with their combustion, namely greenhouse gas emissions and air pollution, have prompted a global consensus on the necessity of decarbonization.

B. The core economic argument for renewables rests on the concept of Levelized Cost of Energy (LCOE), which measures the average net present cost of electricity generation for a generating plant over its lifetime. Over the past decade, technological advancements, economies of scale, and optimized supply chains have driven the LCOE of solar photovoltaic (PV) and onshore wind power down dramatically. In many jurisdictions, new utility-scale solar and wind projects are now cheaper than new coal or gas plants, and increasingly, they undercut the operating costs of existing fossil fuel facilities. This cost parity represents a critical tipping point, shifting renewable energy from a heavily subsidized environmental imperative to an economically rational choice.

C. Despite these falling costs, the transition is not without substantial economic friction. A primary challenge is the inherent intermittency of solar and wind resources. The sun does not always shine, and the wind does not always blow, which misaligns with the continuous, on-demand nature of modern electricity consumption. To guarantee grid stability and reliability, significant investments are required in energy storage technologies, such as lithium-ion batteries, pumped hydro, and potentially green hydrogen. Furthermore, the existing electrical grid infrastructure, designed for centralized fossil fuel generation, requires massive upgrades to accommodate decentralized, bidirectional power flows from renewable sources.

D. The transition also poses profound socio-economic challenges, particularly for regions whose economies are deeply intertwined with fossil fuel extraction. The concept of a "just transition" emphasizes the need to support workers and communities displaced by the shift away from coal and oil. While the renewable energy sector is a major engine for job creation—in manufacturing, installation, and maintenance—these new jobs often require different skill sets and are frequently located in different geographic regions than the jobs being lost. Policymakers face the complex task of designing retraining programs, economic diversification strategies, and robust social safety nets to ensure that the economic benefits of the energy transition are equitably distributed and that vulnerable communities are not left behind.
"""

    questions_set_b = [
        # Passage 1 - Y/N/NG
        {
            "title": "Science of Sleep", "section_number": 1, "question_type": "Yes / No / Not Given", "passage_or_context": passage_1b, "question_text": "Scientists have always understood the evolutionary advantages of sleep.", "options_json": ["Yes", "No", "Not Given"], "answer_key": "No", "explanation": "Paragraph A says the evolutionary advantages were 'poorly understood' for decades.", "group_id": "PB1_G1", "group_instructions": "Do the following statements agree with the views of the writer in Reading Passage 1?\nWrite YES, NO or NOT GIVEN."
        },
        {
            "title": "Science of Sleep", "section_number": 1, "question_type": "Yes / No / Not Given", "passage_or_context": passage_1b, "question_text": "The suprachiasmatic nucleus is located in the hypothalamus.", "options_json": ["Yes", "No", "Not Given"], "answer_key": "Yes", "explanation": "Paragraph A states it is 'governed by the suprachiasmatic nucleus (SCN) in the brain's hypothalamus.'", "group_id": "PB1_G1", "group_instructions": ""
        },
        {
            "title": "Science of Sleep", "section_number": 1, "question_type": "Yes / No / Not Given", "passage_or_context": passage_1b, "question_text": "Melatonin production decreases when eyes detect morning sunlight.", "options_json": ["Yes", "No", "Not Given"], "answer_key": "Yes", "explanation": "Paragraph B states sunlight 'suppresses the pineal gland's production of melatonin'.", "group_id": "PB1_G1", "group_instructions": ""
        },
        {
            "title": "Science of Sleep", "section_number": 1, "question_type": "Yes / No / Not Given", "passage_or_context": passage_1b, "question_text": "Blue light from electronic devices is more harmful to teenagers than adults.", "options_json": ["Yes", "No", "Not Given"], "answer_key": "Not Given", "explanation": "The text mentions blue light disrupts sleep but does not compare age groups.", "group_id": "PB1_G1", "group_instructions": ""
        },
        {
            "title": "Science of Sleep", "section_number": 1, "question_type": "Yes / No / Not Given", "passage_or_context": passage_1b, "question_text": "Sleep spindles only appear during Stage 3 of NREM sleep.", "options_json": ["Yes", "No", "Not Given"], "answer_key": "No", "explanation": "Paragraph C states sleep spindles appear in Stage 2.", "group_id": "PB1_G1", "group_instructions": ""
        },
        {
            "title": "Science of Sleep", "section_number": 1, "question_type": "Yes / No / Not Given", "passage_or_context": passage_1b, "question_text": "The brain prunes irrelevant synapses during REM sleep.", "options_json": ["Yes", "No", "Not Given"], "answer_key": "Yes", "explanation": "Paragraph D states 'The brain... pruning irrelevant synapses'.", "group_id": "PB1_G1", "group_instructions": ""
        },

        # Passage 1 - Flow-chart Completion
        {
            "title": "Science of Sleep", "section_number": 1, "question_type": "Flow-chart Completion", "passage_or_context": passage_1b, "question_text": "Retinal ganglion cells detect morning sunlight -> Signal is transmitted to the [Q7].", "options_json": [], "answer_key": "SCN", "explanation": "Paragraph B: 'transmit signals to the SCN'.", "group_id": "PB1_G2", "group_instructions": "Complete the flow-chart below. Choose NO MORE THAN THREE WORDS from the passage."
        },
        {
            "title": "Science of Sleep", "section_number": 1, "question_type": "Flow-chart Completion", "passage_or_context": passage_1b, "question_text": "Signal reaches destination -> The pineal gland is suppressed from producing [Q8].", "options_json": [], "answer_key": "melatonin", "explanation": "Paragraph B: 'suppresses the pineal gland's production of melatonin'.", "group_id": "PB1_G2", "group_instructions": ""
        },
        {
            "title": "Science of Sleep", "section_number": 1, "question_type": "Flow-chart Completion", "passage_or_context": passage_1b, "question_text": "Night falls -> Hormone secretion rises, signaling to the body to [Q9].", "options_json": [], "answer_key": "rest", "explanation": "Paragraph B: 'signaling to the body that it is time to rest.'", "group_id": "PB1_G2", "group_instructions": ""
        },

        # Passage 1 - Note Completion
        {
            "title": "Science of Sleep", "section_number": 1, "question_type": "Note Completion", "passage_or_context": passage_1b, "question_text": "Stage 3 of NREM is also referred to as [Q10] sleep.", "options_json": [], "answer_key": "slow-wave", "explanation": "Paragraph C: 'Stage 3, often called slow-wave sleep (SWS)'.", "group_id": "PB1_G3", "group_instructions": "Complete the notes below. Choose ONE WORD ONLY from the passage."
        },
        {
            "title": "Science of Sleep", "section_number": 1, "question_type": "Note Completion", "passage_or_context": passage_1b, "question_text": "During Stage 3, the immune system undergoes [Q11].", "options_json": [], "answer_key": "strengthening", "explanation": "Paragraph C: 'tissue repair and immune system strengthening'.", "group_id": "PB1_G3", "group_instructions": ""
        },
        {
            "title": "Science of Sleep", "section_number": 1, "question_type": "Note Completion", "passage_or_context": passage_1b, "question_text": "Unlike NREM, the brain wave activity in REM sleep resembles [Q12].", "options_json": [], "answer_key": "wakefulness", "explanation": "Paragraph D: 'resembles wakefulness'.", "group_id": "PB1_G3", "group_instructions": ""
        },
        {
            "title": "Science of Sleep", "section_number": 1, "question_type": "Note Completion", "passage_or_context": passage_1b, "question_text": "A lack of REM sleep can negatively impact one's [Q13] capacity.", "options_json": [], "answer_key": "learning", "explanation": "Paragraph D: 'impaired learning capacity'.", "group_id": "PB1_G3", "group_instructions": ""
        },

        # Passage 2 - Matching Sentence Endings
        {
            "title": "Coral Reef Ecosystems", "section_number": 2, "question_type": "Matching Sentence Endings", "passage_or_context": passage_2b, "question_text": "Coral reefs occupy a very small portion of the ocean floor", "options_json": ["A. yet they house a quarter of all marine species.", "B. because they require a highly protected environment.", "C. which leads to the phenomenon known as coral bleaching.", "D. as it makes building their protective skeletons difficult.", "E. when waters become unusually warm.", "F. to form a hard exoskeleton over millennia."], "answer_key": "A", "explanation": "Paragraph A states they cover less than 0.1% but support 25% of species.", "group_id": "PB2_G1", "group_instructions": "Match each sentence beginning with the correct ending, A-F."
        },
        {
            "title": "Coral Reef Ecosystems", "section_number": 2, "question_type": "Matching Sentence Endings", "passage_or_context": passage_2b, "question_text": "Polyps secrete calcium carbonate", "options_json": ["A. yet they house a quarter of all marine species.", "B. because they require a highly protected environment.", "C. which leads to the phenomenon known as coral bleaching.", "D. as it makes building their protective skeletons difficult.", "E. when waters become unusually warm.", "F. to form a hard exoskeleton over millennia."], "answer_key": "F", "explanation": "Paragraph A states 'The polyps secrete calcium carbonate to form a hard exoskeleton'.", "group_id": "PB2_G1", "group_instructions": ""
        },
        {
            "title": "Coral Reef Ecosystems", "section_number": 2, "question_type": "Matching Sentence Endings", "passage_or_context": passage_2b, "question_text": "The delicate mutualistic exchange collapses", "options_json": ["A. yet they house a quarter of all marine species.", "B. because they require a highly protected environment.", "C. which leads to the phenomenon known as coral bleaching.", "D. as it makes building their protective skeletons difficult.", "E. when waters become unusually warm.", "F. to form a hard exoskeleton over millennia."], "answer_key": "C", "explanation": "Paragraph B explains the collapse leads to 'a phenomenon known as coral bleaching.'", "group_id": "PB2_G1", "group_instructions": ""
        },
        {
            "title": "Coral Reef Ecosystems", "section_number": 2, "question_type": "Matching Sentence Endings", "passage_or_context": passage_2b, "question_text": "Corals experience severe physiological stress", "options_json": ["A. yet they house a quarter of all marine species.", "B. because they require a highly protected environment.", "C. which leads to the phenomenon known as coral bleaching.", "D. as it makes building their protective skeletons difficult.", "E. when waters become unusually warm.", "F. to form a hard exoskeleton over millennia."], "answer_key": "E", "explanation": "Paragraph C: 'When waters become unusually warm... corals experience severe physiological stress.'", "group_id": "PB2_G1", "group_instructions": ""
        },
        {
            "title": "Coral Reef Ecosystems", "section_number": 2, "question_type": "Matching Sentence Endings", "passage_or_context": passage_2b, "question_text": "Ocean acidification threatens coral survival", "options_json": ["A. yet they house a quarter of all marine species.", "B. because they require a highly protected environment.", "C. which leads to the phenomenon known as coral bleaching.", "D. as it makes building their protective skeletons difficult.", "E. when waters become unusually warm.", "F. to form a hard exoskeleton over millennia."], "answer_key": "D", "explanation": "Paragraph D: 'makes it exceedingly difficult for corals to calcify and build their protective skeletons'.", "group_id": "PB2_G1", "group_instructions": ""
        },

        # Passage 2 - Summary Completion from Text
        {
            "title": "Coral Reef Ecosystems", "section_number": 2, "question_type": "Summary Completion", "passage_or_context": passage_2b, "question_text": "The foundation of the coral reef ecosystem is a [Q19] between the coral polyps and zooxanthellae.", "options_json": [], "answer_key": "symbiotic relationship", "explanation": "Paragraph A mentions 'a remarkable symbiotic relationship'.", "group_id": "PB2_G2", "group_instructions": "Complete the summary below. Choose NO MORE THAN TWO WORDS from the passage."
        },
        {
            "title": "Coral Reef Ecosystems", "section_number": 2, "question_type": "Summary Completion", "passage_or_context": passage_2b, "question_text": "Through photosynthesis, these algae provide up to 90% of the coral's [Q20].", "options_json": [], "answer_key": "energy requirements", "explanation": "Paragraph B: 'supplying up to 90% of the coral's energy requirements'.", "group_id": "PB2_G2", "group_instructions": ""
        },
        {
            "title": "Coral Reef Ecosystems", "section_number": 2, "question_type": "Summary Completion", "passage_or_context": passage_2b, "question_text": "However, this relationship is vulnerable to changes in water temperature and [Q21].", "options_json": [], "answer_key": "quality", "explanation": "Paragraph B: 'particularly concerning water temperature and quality.'", "group_id": "PB2_G2", "group_instructions": ""
        },
        {
            "title": "Coral Reef Ecosystems", "section_number": 2, "question_type": "Summary Completion", "passage_or_context": passage_2b, "question_text": "When stressed, corals expel the algae, resulting in a white [Q22] becoming visible.", "options_json": [], "answer_key": "skeleton", "explanation": "Paragraph C: 'leaves the coral's white calcium carbonate skeleton visible'.", "group_id": "PB2_G2", "group_instructions": ""
        },

        # Passage 2 - Multiple Choice
        {
            "title": "Coral Reef Ecosystems", "section_number": 2, "question_type": "Multiple Choice", "passage_or_context": passage_2b, "question_text": "According to the passage, a bleached coral is:", "options_json": ["A. immediately dead.", "B. highly vulnerable to starvation.", "C. able to survive indefinitely without algae.", "D. no longer affected by ocean acidification."], "answer_key": "B", "explanation": "Paragraph C: 'is not immediately dead, it is severely compromised... highly susceptible to disease and starvation.'", "group_id": "PB2_G3", "group_instructions": "Choose the correct letter, A, B, C or D."
        },
        {
            "title": "Coral Reef Ecosystems", "section_number": 2, "question_type": "Multiple Choice", "passage_or_context": passage_2b, "question_text": "The mass bleaching events on the Great Barrier Reef demonstrate that:", "options_json": ["A. corals are evolving to withstand higher temperatures.", "B. heatwaves are occurring too frequently for corals to recover.", "C. ocean acidification is a myth.", "D. human intervention is successfully saving the reefs."], "answer_key": "B", "explanation": "Paragraph D: 'reefs often lack the necessary recovery time between bleaching events.'", "group_id": "PB2_G3", "group_instructions": ""
        },
        {
            "title": "Coral Reef Ecosystems", "section_number": 2, "question_type": "Multiple Choice", "passage_or_context": passage_2b, "question_text": "Ocean acidification occurs because the oceans absorb excessive:", "options_json": ["A. sunlight.", "B. calcium carbonate.", "C. carbon dioxide.", "D. zooxanthellae."], "answer_key": "C", "explanation": "Paragraph D: 'oceans absorb excess carbon dioxide from the atmosphere'.", "group_id": "PB2_G3", "group_instructions": ""
        },
        {
            "title": "Coral Reef Ecosystems", "section_number": 2, "question_type": "Multiple Choice", "passage_or_context": passage_2b, "question_text": "The term 'rainforests of the sea' refers to the reefs':", "options_json": ["A. high rainfall.", "B. vast size compared to the ocean.", "C. extreme biodiversity.", "D. green coloration."], "answer_key": "C", "explanation": "Paragraph A states they are 'among the most biodiverse and productive ecosystems', similar to rainforests.", "group_id": "PB2_G3", "group_instructions": ""
        },

        # Passage 3 - Matching Headings
        {
            "title": "Economics of Renewable Energy", "section_number": 3, "question_type": "Matching Headings", "passage_or_context": passage_3b, "question_text": "Paragraph A", "options_json": ["i. Addressing the financial and energy costs", "ii. The societal impact of job displacement", "iii. The historical dominance of fossil fuels and the push for change", "iv. Achieving cost competitiveness with traditional energy", "v. Overcoming the unpredictable nature of green energy", "vi. Government subsidies for solar power", "vii. Ecological advantages of wind farms"], "answer_key": "iii", "explanation": "Paragraph A discusses fossil fuel history and the need to decarbonize.", "group_id": "PB3_G1", "group_instructions": "Choose the correct heading for each paragraph from the list of headings below."
        },
        {
            "title": "Economics of Renewable Energy", "section_number": 3, "question_type": "Matching Headings", "passage_or_context": passage_3b, "question_text": "Paragraph B", "options_json": ["i. Addressing the financial and energy costs", "ii. The societal impact of job displacement", "iii. The historical dominance of fossil fuels and the push for change", "iv. Achieving cost competitiveness with traditional energy", "v. Overcoming the unpredictable nature of green energy", "vi. Government subsidies for solar power", "vii. Ecological advantages of wind farms"], "answer_key": "iv", "explanation": "Paragraph B explains LCOE dropping and renewables becoming cheaper.", "group_id": "PB3_G1", "group_instructions": ""
        },
        {
            "title": "Economics of Renewable Energy", "section_number": 3, "question_type": "Matching Headings", "passage_or_context": passage_3b, "question_text": "Paragraph C", "options_json": ["i. Addressing the financial and energy costs", "ii. The societal impact of job displacement", "iii. The historical dominance of fossil fuels and the push for change", "iv. Achieving cost competitiveness with traditional energy", "v. Overcoming the unpredictable nature of green energy", "vi. Government subsidies for solar power", "vii. Ecological advantages of wind farms"], "answer_key": "v", "explanation": "Paragraph C deals with intermittency of solar/wind and need for storage.", "group_id": "PB3_G1", "group_instructions": ""
        },
        {
            "title": "Economics of Renewable Energy", "section_number": 3, "question_type": "Matching Headings", "passage_or_context": passage_3b, "question_text": "Paragraph D", "options_json": ["i. Addressing the financial and energy costs", "ii. The societal impact of job displacement", "iii. The historical dominance of fossil fuels and the push for change", "iv. Achieving cost competitiveness with traditional energy", "v. Overcoming the unpredictable nature of green energy", "vi. Government subsidies for solar power", "vii. Ecological advantages of wind farms"], "answer_key": "ii", "explanation": "Paragraph D covers just transition, job losses, and community support.", "group_id": "PB3_G1", "group_instructions": ""
        },

        # Passage 3 - T/F/NG
        {
            "title": "Economics of Renewable Energy", "section_number": 3, "question_type": "True / False / Not Given", "passage_or_context": passage_3b, "question_text": "Fossil fuels have historically been favored because they are easy to dispatch and have high energy density.", "options_json": ["True", "False", "Not Given"], "answer_key": "True", "explanation": "Paragraph A states they dominated 'due to their high energy density, dispatchability'.", "group_id": "PB3_G2", "group_instructions": "Do the following statements agree with the information given in Reading Passage 3?\nWrite TRUE, FALSE or NOT GIVEN."
        },
        {
            "title": "Economics of Renewable Energy", "section_number": 3, "question_type": "True / False / Not Given", "passage_or_context": passage_3b, "question_text": "The LCOE of offshore wind power has decreased faster than onshore wind power.", "options_json": ["True", "False", "Not Given"], "answer_key": "Not Given", "explanation": "The text only mentions onshore wind power dropping dramatically.", "group_id": "PB3_G2", "group_instructions": ""
        },
        {
            "title": "Economics of Renewable Energy", "section_number": 3, "question_type": "True / False / Not Given", "passage_or_context": passage_3b, "question_text": "Modern electrical grids are perfectly suited for decentralized renewable energy sources.", "options_json": ["True", "False", "Not Given"], "answer_key": "False", "explanation": "Paragraph C says the existing grid requires 'massive upgrades'.", "group_id": "PB3_G2", "group_instructions": ""
        },
        {
            "title": "Economics of Renewable Energy", "section_number": 3, "question_type": "True / False / Not Given", "passage_or_context": passage_3b, "question_text": "New jobs in the renewable energy sector are usually found in the same locations as traditional fossil fuel jobs.", "options_json": ["True", "False", "Not Given"], "answer_key": "False", "explanation": "Paragraph D states they are 'frequently located in different geographic regions'.", "group_id": "PB3_G2", "group_instructions": ""
        },

        # Passage 3 - Table Completion
        {
            "title": "Economics of Renewable Energy", "section_number": 3, "question_type": "Table Completion", "passage_or_context": passage_3b, "question_text": "Fossil Fuels: High [Q35] and dispatchability.", "options_json": [], "answer_key": "energy density", "explanation": "Paragraph A: 'high energy density'.", "group_id": "PB3_G3", "group_instructions": "Complete the table below. Choose NO MORE THAN TWO WORDS from the passage."
        },
        {
            "title": "Economics of Renewable Energy", "section_number": 3, "question_type": "Table Completion", "passage_or_context": passage_3b, "question_text": "Fossil Fuels: Cause negative externalities like air pollution and [Q36].", "options_json": [], "answer_key": "greenhouse gas emissions", "explanation": "Paragraph A: 'greenhouse gas emissions and air pollution'.", "group_id": "PB3_G3", "group_instructions": ""
        },
        {
            "title": "Economics of Renewable Energy", "section_number": 3, "question_type": "Table Completion", "passage_or_context": passage_3b, "question_text": "Renewable Energy: Plagued by the inherent [Q37] of wind and solar sources.", "options_json": [], "answer_key": "intermittency", "explanation": "Paragraph C: 'inherent intermittency of solar and wind resources.'", "group_id": "PB3_G3", "group_instructions": ""
        },

        # Passage 3 - Short Answer
        {
            "title": "Economics of Renewable Energy", "section_number": 3, "question_type": "Short Answer Questions", "passage_or_context": passage_3b, "question_text": "What metric is used to measure the average net present cost of electricity generation?", "options_json": [], "answer_key": "Levelized Cost of Energy", "explanation": "Paragraph B: 'Levelized Cost of Energy (LCOE), which measures...'", "group_id": "PB3_G4", "group_instructions": "Answer the questions below. Choose NO MORE THAN THREE WORDS from the passage for each answer."
        },
        {
            "title": "Economics of Renewable Energy", "section_number": 3, "question_type": "Short Answer Questions", "passage_or_context": passage_3b, "question_text": "What technologies are required to guarantee grid stability due to the unpredictable nature of renewables?", "options_json": [], "answer_key": "energy storage technologies", "explanation": "Paragraph C mentions 'significant investments are required in energy storage technologies'.", "group_id": "PB3_G4", "group_instructions": ""
        },
        {
            "title": "Economics of Renewable Energy", "section_number": 3, "question_type": "Short Answer Questions", "passage_or_context": passage_3b, "question_text": "What concept emphasizes the need to assist workers displaced by the energy transition?", "options_json": [], "answer_key": "just transition", "explanation": "Paragraph D: 'concept of a \"just transition\" emphasizes the need...'", "group_id": "PB3_G4", "group_instructions": ""
        },
    ]
    return questions_set_b

def seed_cambridge_reading_set_b():
    conn = sqlite3.connect('ielts_platform.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM questions WHERE skill = 'Reading'")
    insert_questions(cursor, get_set_b_questions())
    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_full_cambridge_reading()
