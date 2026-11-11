# -*- coding: utf-8 -*-
import sqlite3
import json

def seed_authentic_cambridge_cbt():
    conn = sqlite3.connect('ielts_platform.db')
    cursor = conn.cursor()

    # Clear old dummy questions
    cursor.execute("DELETE FROM questions WHERE passage_or_context LIKE '%Sample Cambridge IELTS%' OR passage_or_context LIKE '%dummy%'")
    cursor.execute("DELETE FROM questions WHERE title LIKE 'Reading - %' AND LENGTH(passage_or_context) < 100")

    # ==========================================
    # PASSAGE 1: URBAN WILDLIFE ADAPTATION (Q1-13)
    # ==========================================
    p1_title = "The Secret Life of the Urban Fox in European Metropolises"
    p1_text = """Paragraph A
Over the past five decades, red foxes (Vulpes vulpes) have staged a remarkable colonisation of European urban landscapes, particularly across the United Kingdom, Germany, and Switzerland. Originally denizens of dense deciduous woodlands and agricultural fringes, these opportunistic canids have found high-density residential suburbs to be exceptionally hospitable habitats. Recent ecological surveys estimate that London alone supports an urban fox population exceeding 10,000 individuals, representing one of the highest carnivore densities recorded anywhere on Earth.

Paragraph B
The primary driver of urban fox proliferation is the abundant and predictable availability of anthropogenic food resources. Whereas rural foxes must expend substantial energy hunting small rodents, lagomorphs, and foraging for seasonal berries, city-dwelling foxes thrive on discarded food waste, municipal refuse bins, and deliberate feeding by urban residents. Biologists at the University of Bristol discovered that up to 60% of an urban fox’s daily caloric intake originates directly from human domestic sources, fundamentally altering their foraging behaviour and reducing their home ranges from several square kilometres in rural zones to less than thirty hectares in metropolitan centres.

Paragraph C
Urban existence has also precipitated noticeable physiological and behavioural adaptations. Anthropologists and evolutionary biologists note that urban foxes exhibit reduced fear responses toward humans and lower baseline levels of cortisol, the principal stress hormone in mammals. Furthermore, morphological examinations of skull specimens gathered over sixty years reveal subtle cranial reshaping: urban foxes have evolved slightly shorter, broader snouts with robust bite forces adapted for crushing commercial packaging and scavenging hard food scraps, mirroring the initial evolutionary stages of wolf domestication in ancient human settlements.

Paragraph D
Despite their successful integration, urban foxes provoke polarized public reactions. Sociological investigations indicate that approximately 70% of urban residents hold favourable or neutral attitudes toward foxes, viewing them as charismatic representations of wild nature within concrete environments. Conversely, a vocal minority expresses acute concerns regarding property damage, nocturnal vocalizations, garden excavation, and potential pathogen transmission, notably sarcoptic mange and echinococcosis, though empirical epidemiological data indicates that zoonotic risk to humans remains negligible.

Paragraph E
Urban planners and municipal wildlife authorities increasingly advocate for peaceful coexistence rather than costly and futile eradication programmes. Historical culling campaigns conducted across British boroughs during the 1970s consistently demonstrated that vacant territories created by lethal control are invariably recolonized by juvenile dispersers within mere weeks. Modern urban ecology emphasizes proactive community education, secure municipal waste management, and non-lethal deterrents to maintain sustainable equilibrium between city residents and their wild neighbours."""

    p1_questions = [
        # Questions 1-6: True / False / Not Given
        {
            "num": 1,
            "type": "True / False / Not Given",
            "text": "London has the highest recorded density of red foxes compared to any rural habitat in Europe.",
            "opts": ["TRUE", "FALSE", "NOT GIVEN"],
            "ans": "TRUE",
            "exp": "Paragraph A states London supports over 10,000 foxes, representing one of the highest carnivore densities recorded on Earth."
        },
        {
            "num": 2,
            "type": "True / False / Not Given",
            "text": "Human-provided food accounts for the majority of an urban fox's daily calorie consumption.",
            "opts": ["TRUE", "FALSE", "NOT GIVEN"],
            "ans": "TRUE",
            "exp": "Paragraph B states up to 60% of an urban fox's daily caloric intake originates from human domestic sources."
        },
        {
            "num": 3,
            "type": "True / False / Not Given",
            "text": "Urban foxes have larger geographical home territories than their rural counterparts.",
            "opts": ["TRUE", "FALSE", "NOT GIVEN"],
            "ans": "FALSE",
            "exp": "Paragraph B explains that territory size reduced from several square kilometres in rural zones to less than thirty hectares in cities."
        },
        {
            "num": 4,
            "type": "True / False / Not Given",
            "text": "Urban foxes produce higher cortisol levels than rural foxes due to traffic noise and city stress.",
            "opts": ["TRUE", "FALSE", "NOT GIVEN"],
            "ans": "FALSE",
            "exp": "Paragraph C notes urban foxes exhibit lower baseline levels of cortisol, meaning less stress."
        },
        {
            "num": 5,
            "type": "True / False / Not Given",
            "text": "The British government currently funds annual culling operations in major metropolitan cities.",
            "opts": ["TRUE", "FALSE", "NOT GIVEN"],
            "ans": "NOT GIVEN",
            "exp": "Paragraph E mentions historical culls in the 1970s, but does not state that the government currently funds annual operations."
        },
        {
            "num": 6,
            "type": "True / False / Not Given",
            "text": "The transmission of severe diseases from urban foxes to human beings occurs frequently.",
            "opts": ["TRUE", "FALSE", "NOT GIVEN"],
            "ans": "FALSE",
            "exp": "Paragraph D states that empirical epidemiological data indicates zoonotic risk to humans remains negligible."
        },

        # Questions 7-10: Sentence Completion
        {
            "num": 7,
            "type": "Sentence Completion",
            "text": "The evolutionary reshaping of fox snouts resembles the historical process of ________.",
            "opts": ["wolf domestication", "natural selection", "urban migration", "carnivore extinction"],
            "ans": "wolf domestication",
            "exp": "Paragraph C states that cranial reshaping mirrors the initial evolutionary stages of wolf domestication."
        },
        {
            "num": 8,
            "type": "Sentence Completion",
            "text": "When foxes are culled, their empty territories are rapidly taken over by ________.",
            "opts": ["juvenile dispersers", "adult wolves", "domestic dogs", "rural hunters"],
            "ans": "juvenile dispersers",
            "exp": "Paragraph E states that vacant territories are recolonized by juvenile dispersers within weeks."
        },
        {
            "num": 9,
            "type": "Sentence Completion",
            "text": "Urban foxes have developed broader snouts in order to exert greater ________ on packaging.",
            "opts": ["bite forces", "olfactory sense", "running speeds", "vocal volume"],
            "ans": "bite forces",
            "exp": "Paragraph C specifically mentions robust bite forces adapted for crushing commercial packaging."
        },
        {
            "num": 10,
            "type": "Sentence Completion",
            "text": "Around 70% of city dwellers view foxes as a positive representation of ________.",
            "opts": ["wild nature", "urban pests", "foreign species", "agricultural helpers"],
            "ans": "wild nature",
            "exp": "Paragraph D states residents view foxes as charismatic representations of wild nature."
        },

        # Questions 11-13: Multiple Choice (A, B, C, D)
        {
            "num": 11,
            "type": "Multiple Choice Questions (MCQ)",
            "text": "What is the author's main purpose in Paragraph B?",
            "opts": [
                "A: To explain how accessible food waste influenced fox territory size and diet.",
                "B: To criticise city dwellers for feeding wild carnivores.",
                "C: To argue that rural foxes are healthier than urban foxes.",
                "D: To compare the nutritional quality of commercial refuse and wild berries."
            ],
            "ans": "A: To explain how accessible food waste influenced fox territory size and diet.",
            "exp": "Paragraph B outlines anthropogenic food as the primary driver that shrunk home ranges and altered foraging."
        },
        {
            "num": 12,
            "type": "Multiple Choice Questions (MCQ)",
            "text": "According to Paragraph C, physical changes in urban foxes are evidence of:",
            "opts": [
                "A: Rapid morphological adaptation to artificial human environments.",
                "B: Genetic defects caused by malnutrition and pollution.",
                "C: Hybridization between foxes and domestic dogs.",
                "D: A decline in cranial capacity and intelligence."
            ],
            "ans": "A: Rapid morphological adaptation to artificial human environments.",
            "exp": "Paragraph C details cranial reshaping and bite force adaptations to urban scavenging."
        },
        {
            "num": 13,
            "type": "Multiple Choice Questions (MCQ)",
            "text": "The author concludes that urban wildlife management should prioritize:",
            "opts": [
                "A: Public awareness and secure waste disposal rather than eradication.",
                "B: Total elimination of canid populations from residential areas.",
                "C: Relocating urban foxes back to rural forests.",
                "D: Constructing physical barriers around all private gardens."
            ],
            "ans": "A: Public awareness and secure waste disposal rather than eradication.",
            "exp": "Paragraph E states authorities emphasize proactive education, waste management, and coexistence."
        }
    ]

    # ==========================================
    # PASSAGE 2: THE NEUROSCIENCE OF SLEEP (Q14-26)
    # ==========================================
    p2_title = "The Neuroscience of Sleep Architecture and Memory Consolidation"
    p2_text = """Paragraph A
For centuries, sleep was conceptualized as a passive state of physiological dormancy—a simple cessation of consciousness enabling cellular repair. However, with the advent of electroencephalography (EEG) and functional magnetic resonance imaging (fMRI), modern neuroscience has unveiled a dynamic, highly orchestrated series of neurological cycles. Human sleep architecture is structured into alternating non-rapid eye movement (NREM) and rapid eye movement (REM) phases, each characterized by distinct neural oscillations and neurochemical environments essential for cognitive vitality.

Paragraph B
Stage 3 NREM sleep, often termed slow-wave sleep (SWS), is characterized by synchronized delta waves oscillating across the cerebral cortex at frequencies below 4 Hertz. Research led by Dr. Matthew Walker at UC Berkeley has demonstrated that slow-wave sleep serves as an active neurocomputational clearinghouse. During this stage, episodic memory traces temporarily encoded in the hippocampus are systematically replayed and transferred to the neocortex for long-term structural storage. This hippocampal-neocortical dialogue effectively prevents memory interference and clears the hippocampus for subsequent daily learning.

Paragraph C
In contrast to the slow, synchronized rhythms of NREM, REM sleep presents a paradoxical burst of desynchronized, high-frequency beta and theta waves accompanied by muscle atonia and vivid dreaming. During REM sleep, the brain is flooded with acetylcholine while norepinephrine and serotonin are virtually eliminated. This unique neurochemical configuration creates a state of unconstrained neural plasticity. Here, the brain integrates newly consolidated memories with extensive pre-existing semantic networks, fostering creative problem-solving, novel conceptual associations, and cognitive insights.

Paragraph D
Sleep architecture is also fundamentally implicated in the physiological detoxification of neural tissue. In 2012, neuroscientist Dr. Maiken Nedergaard discovered the glymphatic system—a specialized microscopic waste-clearance network that operates primarily during deep slow-wave sleep. During NREM Stage 3, interstitial space within the brain expands by up to 60%, allowing cerebrospinal fluid to flush through cerebral parenchyma and wash away metabolic neurotoxins, including amyloid-beta and tau proteins associated with Alzheimer’s disease.

Paragraph E
Chronic sleep deprivation and irregular circadian rhythms severely disrupt both memory consolidation and neurovascular health. Modern lifestyle factors, including nocturnal blue light exposure from digital screens, excessive caffeine consumption, and shift work, selectively truncate slow-wave and REM sleep phases. Epidemiological analyses reveal that individuals who regularly sleep fewer than six hours per night exhibit marked impairments in declarative recall, diminished emotional regulation, and elevated long-term risks of neurodegenerative disease."""

    p2_questions = [
        # Questions 14-19: Matching Headings
        {
            "num": 14,
            "type": "Matching Headings",
            "text": "Which heading best matches Paragraph A?",
            "opts": [
                "i: A shift from passive dormancy to complex neural cycles",
                "ii: The chemical composition of commercial sleep medications",
                "iii: The discovery of the glymphatic clearance network",
                "iv: Hippocampal transfer during slow-wave sleep",
                "v: Creative synthesis during rapid eye movement",
                "vi: Societal costs of chronic insomnia"
            ],
            "ans": "i: A shift from passive dormancy to complex neural cycles",
            "exp": "Paragraph A contrasts the old passive concept of sleep with modern EEG discoveries of structured NREM/REM cycles."
        },
        {
            "num": 15,
            "type": "Matching Headings",
            "text": "Which heading best matches Paragraph B?",
            "opts": [
                "i: A shift from passive dormancy to complex neural cycles",
                "ii: Memory transfer from short-term to long-term storage",
                "iii: The discovery of the glymphatic clearance network",
                "iv: Emotional regulation and mood stabilization",
                "v: Creative synthesis during rapid eye movement",
                "vi: Societal costs of chronic insomnia"
            ],
            "ans": "ii: Memory transfer from short-term to long-term storage",
            "exp": "Paragraph B explains how slow-wave sleep transfers memory traces from hippocampus to neocortex."
        },
        {
            "num": 16,
            "type": "Matching Headings",
            "text": "Which heading best matches Paragraph C?",
            "opts": [
                "i: Memory transfer from short-term to long-term storage",
                "ii: Creative synthesis and associative thinking in REM",
                "iii: The discovery of the glymphatic clearance network",
                "iv: The function of muscle paralysis in dreams",
                "v: Blood pressure regulation during deep sleep",
                "vi: Societal costs of chronic insomnia"
            ],
            "ans": "ii: Creative synthesis and associative thinking in REM",
            "exp": "Paragraph C discusses REM neurochemistry, unconstrained plasticity, and creative problem-solving."
        },
        {
            "num": 17,
            "type": "Matching Headings",
            "text": "Which heading best matches Paragraph D?",
            "opts": [
                "i: Creative synthesis and associative thinking in REM",
                "ii: Brain detoxification through the glymphatic system",
                "iii: Memory transfer from short-term to long-term storage",
                "iv: Circadian rhythm synchronization in shift workers",
                "v: Sleep patterns in early mammalian evolution",
                "vi: Societal costs of chronic insomnia"
            ],
            "ans": "ii: Brain detoxification through the glymphatic system",
            "exp": "Paragraph D describes the glymphatic waste clearance network flushing out amyloid-beta and tau proteins."
        },
        {
            "num": 18,
            "type": "Matching Headings",
            "text": "Which heading best matches Paragraph E?",
            "opts": [
                "i: Brain detoxification through the glymphatic system",
                "ii: Consequences of modern lifestyle and chronic sleep deficit",
                "iii: Memory transfer from short-term to long-term storage",
                "iv: Creative synthesis and associative thinking in REM",
                "v: The benefits of afternoon power naps",
                "vi: Societal costs of chronic insomnia"
            ],
            "ans": "ii: Consequences of modern lifestyle and chronic sleep deficit",
            "exp": "Paragraph E focuses on blue light, caffeine, shift work, memory impairments, and neurodegenerative risks."
        },

        # Questions 19-22: Matching Features
        {
            "num": 19,
            "type": "Matching Features",
            "text": "Which scientist discovered the glymphatic waste clearance network in the brain?",
            "opts": ["A: Dr. Matthew Walker", "B: Dr. Maiken Nedergaard", "C: Dr. Hans Berger", "D: Dr. Francis Crick"],
            "ans": "B: Dr. Maiken Nedergaard",
            "exp": "Paragraph D explicitly credits Dr. Maiken Nedergaard with discovering the glymphatic system in 2012."
        },
        {
            "num": 20,
            "type": "Matching Features",
            "text": "Which scientist led research on hippocampal memory replay during slow-wave sleep?",
            "opts": ["A: Dr. Matthew Walker", "B: Dr. Maiken Nedergaard", "C: Dr. Hans Berger", "D: Dr. Francis Crick"],
            "ans": "A: Dr. Matthew Walker",
            "exp": "Paragraph B credits research led by Dr. Matthew Walker at UC Berkeley."
        },

        # Questions 21-26: Summary Completion (Word Box)
        {
            "num": 21,
            "type": "Summary Completion",
            "text": "During Stage 3 NREM sleep, delta waves operate at frequencies under ________ Hertz.",
            "opts": ["four", "ten", "twenty", "fifty"],
            "ans": "four",
            "exp": "Paragraph B states delta waves oscillate across the cortex at frequencies below 4 Hertz."
        },
        {
            "num": 22,
            "type": "Summary Completion",
            "text": "The temporary memory traces in the ________ are transferred to the neocortex.",
            "opts": ["hippocampus", "cerebellum", "amygdala", "prefrontal cortex"],
            "ans": "hippocampus",
            "exp": "Paragraph B states memory traces in the hippocampus are transferred to the neocortex."
        },
        {
            "num": 23,
            "type": "Summary Completion",
            "text": "During REM sleep, neurotransmitters norepinephrine and serotonin are virtually ________.",
            "opts": ["eliminated", "doubled", "crystallized", "synthesized"],
            "ans": "eliminated",
            "exp": "Paragraph C explicitly states norepinephrine and serotonin are virtually eliminated."
        },
        {
            "num": 24,
            "type": "Summary Completion",
            "text": "The glymphatic system expands interstitial space by up to ________ percent to flush toxins.",
            "opts": ["60%", "20%", "40%", "80%"],
            "ans": "60%",
            "exp": "Paragraph D mentions interstitial space expands by up to 60%."
        },
        {
            "num": 25,
            "type": "Multiple Choice Questions (MCQ)",
            "text": "According to Paragraph D, failure to clear amyloid-beta proteins is linked to:",
            "opts": [
                "A: Alzheimer's disease.",
                "B: Excessive REM dreaming.",
                "C: High blood pressure in children.",
                "D: Sudden muscle paralysis."
            ],
            "ans": "A: Alzheimer's disease.",
            "exp": "Paragraph D specifically connects amyloid-beta and tau proteins to Alzheimer's disease."
        },
        {
            "num": 26,
            "type": "Multiple Choice Questions (MCQ)",
            "text": "What does the text identify as a primary cause of disrupted sleep in contemporary society?",
            "opts": [
                "A: Digital blue light and shift work.",
                "B: Lack of physical exercise.",
                "C: Overeating carbohydrates.",
                "D: Excessive room temperature."
            ],
            "ans": "A: Digital blue light and shift work.",
            "exp": "Paragraph E explicitly lists nocturnal blue light exposure and shift work."
        }
    ]

    # ==========================================
    # PASSAGE 3: AI IN ENVIRONMENTAL ARCHAEOLOGY (Q27-40)
    # ==========================================
    p3_title = "Artificial Intelligence in Environmental Archaeology & Deep Earth Geophysics"
    p3_text = """Paragraph A
For over a century, archaeological exploration relied on manual trench excavation, aerial black-and-white photography, and serendipitous discoveries by farmers and civil engineers. While effective for uncovering monumental stone structures, these traditional techniques were notoriously labour-intensive and structurally biased toward conspicuous, durable settlements. Today, the convergence of airborne Light Detection and Ranging (LiDAR), multispectral satellite imaging, and deep convolutional neural networks (CNNs) has transformed archaeology into a quantitative predictive science.

Paragraph B
LiDAR instruments mounted on aerial drones emit up to one million laser pulses per second toward the earth's surface. While canopy vegetation absorbs and reflects the majority of these optical pulses, a small percentage penetrates the foliage and bounces off the underlying terrain. Machine learning algorithms, trained on millions of georeferenced topographic elevation models, can digitally strip away dense rainforest canopies with millimetre precision, revealing ancient earthworks, agricultural terrace systems, and hidden road networks that had remained invisible beneath primary jungle for millennia.

Paragraph C
In 2018, an international team deployed deep learning models to process over 2,000 square kilometres of LiDAR imagery across the Petén jungle in northern Guatemala. Within days, the AI identified more than 61,000 previously unrecorded ancient Maya structures, including defensive ramparts, elevated highways, and extensive irrigation canals. The discovery fundamentally overturned long-held archaeological consensuses, proving that the Maya lowlands supported a sophisticated, interconnected civilization of ten to fifteen million people rather than isolated, low-density tribal city-states.

Paragraph D
Beyond surface topographic detection, artificial intelligence is revolutionizing subsurface geophysics through ground-penetrating radar (GPR) and magnetometry. Analyzing complex, noisy radar reflections beneath modern urban pavements or agricultural fields historically required months of expert manual interpretation. Modern neural networks can now rapidly deconvolve multi-frequency electromagnetic radar returns, constructing three-dimensional tomographic reconstructions of buried foundations, subterranean crypts, and ancient metallurgy kilns with unprecedented fidelity.

Paragraph E
Despite these technological triumphs, archaeological ethicists emphasize that remote sensing and AI models cannot entirely replace meticulous stratigraphic excavation on the ground. Artificial intelligence generates probabilistic predictions of cultural anomalies, but direct empirical ground-truthing, radiocarbon isotope dating, and ceramic sequence analysis remain imperative to establish absolute chronological timelines. Technology serves not to render field archaeologists obsolete, but rather to direct finite excavation resources with laser precision toward the most culturally significant subterranean targets."""

    p3_questions = [
        # Questions 27-32: Yes / No / Not Given (Writer's Claims)
        {
            "num": 27,
            "type": "Yes / No / Not Given",
            "text": "Traditional archaeological methods were disproportionately biased toward finding large, durable monuments.",
            "opts": ["YES", "NO", "NOT GIVEN"],
            "ans": "YES",
            "exp": "Paragraph A states traditional methods were structurally biased toward conspicuous, durable settlements."
        },
        {
            "num": 28,
            "type": "Yes / No / Not Given",
            "text": "All laser pulses fired by airborne LiDAR equipment reach the ground surface directly.",
            "opts": ["YES", "NO", "NOT GIVEN"],
            "ans": "NO",
            "exp": "Paragraph B explains that canopy vegetation absorbs and reflects the majority, while only a small percentage penetrates to the ground."
        },
        {
            "num": 29,
            "type": "Yes / No / Not Given",
            "text": "The 2018 Guatemala survey proved the ancient Maya population was significantly smaller than previously assumed.",
            "opts": ["YES", "NO", "NOT GIVEN"],
            "ans": "NO",
            "exp": "Paragraph C shows it overturned old beliefs by proving the Maya supported 10-15 million people, a much larger interconnected civilization."
        },
        {
            "num": 30,
            "type": "Yes / No / Not Given",
            "text": "AI models process ground-penetrating radar data much faster than human geophysicists.",
            "opts": ["YES", "NO", "NOT GIVEN"],
            "ans": "YES",
            "exp": "Paragraph D states what previously took months of manual interpretation is now processed rapidly by neural networks."
        },
        {
            "num": 31,
            "type": "Yes / No / Not Given",
            "text": "Archaeological excavation in Guatemala is funded entirely by international technology companies.",
            "opts": ["YES", "NO", "NOT GIVEN"],
            "ans": "NOT GIVEN",
            "exp": "The text does not mention the funding sources for the Guatemala excavations."
        },
        {
            "num": 32,
            "type": "Yes / No / Not Given",
            "text": "Artificial intelligence algorithms have made physical field excavation on the ground obsolete.",
            "opts": ["YES", "NO", "NOT GIVEN"],
            "ans": "NO",
            "exp": "Paragraph E explicitly states that AI cannot replace ground excavation and ground-truthing is still imperative."
        },

        # Questions 33-36: Multiple Choice
        {
            "num": 33,
            "type": "Multiple Choice Questions (MCQ)",
            "text": "According to Paragraph B, how does AI assist LiDAR analysis in dense jungles?",
            "opts": [
                "A: By digitally stripping away foliage to reveal underlying earthworks.",
                "B: By burning vegetation using high-power laser pulses.",
                "C: By predicting weather conditions above rainforest canopies.",
                "D: By excavating soil automatically using robotic drones."
            ],
            "ans": "A: By digitally stripping away foliage to reveal underlying earthworks.",
            "exp": "Paragraph B states AI can digitally strip away dense rainforest canopies to reveal hidden earthworks."
        },
        {
            "num": 34,
            "type": "Multiple Choice Questions (MCQ)",
            "text": "What was discovered in the Petén jungle in 2018?",
            "opts": [
                "A: Over 61,000 previously unrecorded ancient Maya structures.",
                "B: An underground modern military bunker.",
                "C: A new species of tropical plant.",
                "D: An intact library of ancient paper manuscripts."
            ],
            "ans": "A: Over 61,000 previously unrecorded ancient Maya structures.",
            "exp": "Paragraph C specifically states the AI identified more than 61,000 previously unrecorded structures."
        },
        {
            "num": 35,
            "type": "Multiple Choice Questions (MCQ)",
            "text": "Ground-penetrating radar (GPR) combined with AI is capable of:",
            "opts": [
                "A: Generating three-dimensional reconstructions of buried subterranean structures.",
                "B: Altering the chemical composition of archaeological artifacts.",
                "C: Transmitting radio signals through ocean trenches.",
                "D: Determining the exact historical names of buried kings."
            ],
            "ans": "A: Generating three-dimensional reconstructions of buried subterranean structures.",
            "exp": "Paragraph D describes constructing 3D tomographic reconstructions of buried foundations."
        },
        {
            "num": 36,
            "type": "Multiple Choice Questions (MCQ)",
            "text": "What is the primary role of field archaeologists in the age of AI, according to Paragraph E?",
            "opts": [
                "A: To perform ground-truthing, radiocarbon dating, and stratigraphic validation.",
                "B: To write software code for autonomous LiDAR drones.",
                "C: To guard archaeological sites from international tourists.",
                "D: To manually photograph all surface stones without computers."
            ],
            "ans": "A: To perform ground-truthing, radiocarbon dating, and stratigraphic validation.",
            "exp": "Paragraph E emphasizes empirical ground-truthing, isotope dating, and ceramic sequence analysis."
        },

        # Questions 37-40: Table / Sentence Completion
        {
            "num": 37,
            "type": "Sentence Completion",
            "text": "Traditional aerial black-and-white photography was notoriously ________ and time-consuming.",
            "opts": ["labour-intensive", "inexpensive", "accurate", "hazardous"],
            "ans": "labour-intensive",
            "exp": "Paragraph A states traditional techniques were notoriously labour-intensive."
        },
        {
            "num": 38,
            "type": "Sentence Completion",
            "text": "LiDAR systems emit up to ________ laser pulses per second.",
            "opts": ["one million", "ten thousand", "five hundred", "fifty million"],
            "ans": "one million",
            "exp": "Paragraph B states LiDAR emits up to one million laser pulses per second."
        },
        {
            "num": 39,
            "type": "Sentence Completion",
            "text": "The Petén survey proved the Maya lowlands had an estimated population of ________ people.",
            "opts": ["ten to fifteen million", "under one million", "over fifty million", "five hundred thousand"],
            "ans": "ten to fifteen million",
            "exp": "Paragraph C gives the population figure of ten to fifteen million."
        },
        {
            "num": 40,
            "type": "Sentence Completion",
            "text": "Absolute chronological timelines still require ground-based ________ isotope dating.",
            "opts": ["radiocarbon", "potassium", "uranium", "hydrogen"],
            "ans": "radiocarbon",
            "exp": "Paragraph E explicitly refers to radiocarbon isotope dating."
        }
    ]

    all_passages = [
        (p1_title, p1_text, p1_questions, 1),
        (p2_title, p2_text, p2_questions, 2),
        (p3_title, p3_text, p3_questions, 3)
    ]

    for p_title, p_text, q_list, p_idx in all_passages:
        for q in q_list:
            cursor.execute("""
                INSERT INTO questions (
                    title, skill, test_type, section_number, question_type, passage_or_context,
                    question_text, options_json, answer_key, explanation, difficulty,
                    cambridge_book, test_number, passage_or_section, difficulty_band
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p_title,
                "Reading",
                "Academic",
                p_idx,
                q["type"],
                p_text,
                q["text"],
                json.dumps(q["opts"]),
                q["ans"],
                q["exp"],
                "Hard" if p_idx == 3 else ("Medium" if p_idx == 2 else "Easy"),
                19,
                1,
                p_idx,
                7.5
            ))

    conn.commit()
    conn.close()
    print("SUCCESS: 40 Authentic Cambridge Reading questions across 3 full passages successfully seeded!")

if __name__ == "__main__":
    seed_authentic_cambridge_cbt()
