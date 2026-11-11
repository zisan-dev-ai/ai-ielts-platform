"""
Authentic Cambridge IELTS Speaking Full Test Pool Seeder (Cambridge 15 - 19)
Implements official 2-Frame Part 1:
- Frame 1 (Q1-Q2): Mandatory Baseline Topic (Hometown & Neighbourhood / Work & Studies / Home & Accommodation)
- Frame 2 (Q3-Q4): Specialized Cambridge Secondary Topic (Tech, Weather, Food, Photography, Childhood, Shopping, Animals, Sports, Music, Travel, Books, Art)
"""

import sqlite3
import json

def seed_authentic_cambridge_speaking():
    conn = sqlite3.connect('ielts_platform.db')
    cursor = conn.cursor()

    # Clear legacy speaking questions
    cursor.execute("DELETE FROM questions WHERE skill = 'Speaking'")

    speaking_tests = [
        # TEST 1: Technology & Modern Life (Cambridge 19 Test 1)
        {
            "cambridge_book": 19, "test_number": 1, "difficulty_band": 7.5,
            "part1": {
                "title": "Hometown → Technology & Daily Transport",
                "topic": "Hometown & Technology",
                "mandatory_topic": "Hometown & Neighbourhood",
                "secondary_topic": "Technology & Smart Transport",
                "questions": [
                    "Can you tell me about the town or city where you grew up?",
                    "What do you like most about living in your hometown?",
                    "How often do you use digital apps and smartphones to travel or commute?",
                    "Do you think modern technology has made daily life more convenient?"
                ],
                "model_answers": [
                    "I hail from Chittagong, a vibrant coastal port city in southeastern Bangladesh, known as the commercial capital.",
                    "What appeals to me most is the unique juxtaposition of dynamic urban commercial life and scenic natural landscapes like nearby hills and beaches.",
                    "I rely on ride-sharing and navigation apps on a daily basis; digital transport platforms have completely transformed urban commuting.",
                    "Undoubtedly. From instant communication to automated transit routing, technological innovations have eliminated tedious friction from everyday tasks."
                ]
            },
            "part2": {
                "title": "Describe a time when you used technology to solve an important problem",
                "topic": "Technology & Problem Solving",
                "cue_card_prompt": """<div class="cambridge-cue-card-inner"><h4>Describe a time when you used technology to solve an important problem.</h4><p><b>You should say:</b></p><ul><li>What the problem was</li><li>What technology or digital tool you used</li><li>How you used it to address the situation</li></ul><p><b>and explain how you felt after solving the problem with this technology.</b></p></div>""",
                "model_answer": "I would like to recount an experience from last year when our university research team faced a critical data synchronization bottleneck just forty-eight hours prior to a national symposium deadline. We had amassed raw survey datasets from over six hundred respondents, but our members were physically isolated due to transport strikes. To circumvent this, I established a cloud-based collaborative pipeline using automated data-cleaning scripts. Resolving this crisis instilled an immense sense of relief and demonstrated the power of digital infrastructure."
            },
            "part3": {
                "title": "Technology in Society & Future Automation",
                "topic": "Artificial Intelligence & Workforce",
                "questions": [
                    "How has modern communication technology altered interpersonal relationships?",
                    "Do you believe reliance on smartphones is diminishing people's problem-solving faculties?",
                    "In what ways will artificial intelligence restructure the future employment landscape?",
                    "Should governments implement stricter regulations on digital tech corporations?"
                ],
                "model_answers": [
                    "Modern digital communication has eradicated geographical barriers, facilitating instantaneous global connectivity; however, it has simultaneously eroded face-to-face emotional depth.",
                    "To a certain extent, yes. The instantaneous availability of search algorithms tends to discourage deep cognitive struggle and spatial memory.",
                    "AI is poised to automate routine cognitive and manual tasks, which will displace certain legacy professions while birthing novel sectors demanding emotional intelligence and ethical oversight.",
                    "Absolutely. Robust state regulatory frameworks are imperative to safeguard personal data privacy, prevent algorithmic monopolization, and mitigate misinformation."
                ]
            }
        },

        # TEST 2: Environment & Daily Routine (Cambridge 18 Test 2)
        {
            "cambridge_book": 18, "test_number": 2, "difficulty_band": 7.5,
            "part1": {
                "title": "Work/Studies → Environment & Daily Routine",
                "topic": "Studies & Environment",
                "mandatory_topic": "Work or Studies",
                "secondary_topic": "Environment & Recycling",
                "questions": [
                    "Are you currently studying or do you have a full-time job?",
                    "What inspired you to choose your current field of specialization?",
                    "Do you make an effort to recycle or reduce plastic waste in your daily life?",
                    "Do you think people in your country are becoming more environmentally conscious?"
                ],
                "model_answers": [
                    "I am currently completing my undergraduate degree in Computer Science and Applied Data Analytics at a leading university.",
                    "I was captivated by the immense transformative power of predictive algorithms to solve real-world logistical and environmental challenges.",
                    "Yes, I always carry a reusable canvas bag and stainless steel water bottle, and I separate compostable kitchen waste from plastics.",
                    "Increasingly so. Younger generations especially are participating in urban tree planting drives and advocating for cleaner public transport."
                ]
            },
            "part2": {
                "title": "Describe an environmental project or activity that you participated in",
                "topic": "Environmental Conservation",
                "cue_card_prompt": """<div class="cambridge-cue-card-inner"><h4>Describe an environmental project or activity that you participated in.</h4><p><b>You should say:</b></p><ul><li>What the project or activity was</li><li>When and where it took place</li><li>What you specifically contributed to it</li></ul><p><b>and explain why this environmental activity was meaningful to you.</b></p></div>""",
                "model_answer": "I would like to speak about an impactful community mangrove afforestation initiative in coastal Cox's Bazar. In July 2024, alongside a local conservation collective, we mobilized to restore a degraded coastline. Over four intensive days, our cohort planted over three thousand mangrove saplings. This was profoundly meaningful because mangroves act as vital bioshields against catastrophic cyclonic storm surges."
            },
            "part3": {
                "title": "Environmental Protection and Global Sustainability",
                "topic": "Climate Change & Sustainable Policy",
                "questions": [
                    "What are the most pressing environmental challenges facing developing nations today?",
                    "Who bears greater responsibility for climate mitigation: individual citizens or multinational corporations?",
                    "How can educational institutions better instill environmental awareness in younger generations?",
                    "Do you believe renewable energy will completely supplant fossil fuels in the near future?"
                ],
                "model_answers": [
                    "Developing nations grapple with rapid unplanned urbanization, industrial effluent discharge contaminating potable water supplies, and severe air quality degradation.",
                    "While individual conscious consumerism is commendable, multinational corporations and national governments unquestionably shoulder the lion's share of responsibility due to massive emissions.",
                    "Schools must transition from theoretical textbook instruction to experiential pedagogy, such as campus compost management, waste audits, and renewable energy workshops.",
                    "While a complete transition is technologically feasible, geopolitical dependencies on fossil fuel subsidies may prolong the complete global phase-out for another few decades."
                ]
            }
        },

        # TEST 3: Weather, Climate & Accommodation (Cambridge 18 Test 1)
        {
            "cambridge_book": 18, "test_number": 1, "difficulty_band": 7.5,
            "part1": {
                "title": "Accommodation → Weather & Seasons",
                "topic": "Accommodation & Weather",
                "mandatory_topic": "Home & Accommodation",
                "secondary_topic": "Weather & Climate",
                "questions": [
                    "Do you live in a house or an apartment?",
                    "What is your favourite room in your home and why?",
                    "What kind of weather do you enjoy the most, and why?",
                    "Does the weather ever influence your mood or daily productivity?"
                ],
                "model_answers": [
                    "I live in a comfortable fifth-floor apartment in a residential neighbourhood with ample natural sunlight and ventilation.",
                    "My favourite room is my study room because it has a large window overlooking a quiet park, making it ideal for reading and deep work.",
                    "I find crisp, mildly temperate autumn afternoons most invigorating, as the moderate humidity and cool breeze create ideal conditions for outdoor activities.",
                    "Without question. Prolonged overcast skies often induce a sense of lethargy, whereas bright sunshine elevates my cognitive alertness."
                ]
            },
            "part2": {
                "title": "Describe a memorable journey that was delayed or affected by bad weather",
                "topic": "Travel & Weather",
                "cue_card_prompt": """<div class="cambridge-cue-card-inner"><h4>Describe a memorable journey that was delayed or affected by bad weather.</h4><p><b>You should say:</b></p><ul><li>Where you were traveling to</li><li>What kind of bad weather occurred</li><li>What happened during the delay</li></ul><p><b>and explain how you managed the situation and how it ended.</b></p></div>""",
                "model_answer": "I would like to describe an arduous journey from Dhaka to Sylhet during the peak of the monsoon season two years ago. Heavy flash floods inundated the rail tracks, leaving our intercity train stranded midway for over seven hours. Passengers shared drinking water and snacks, and I passed the time playing cards and engaging in fascinating conversations with fellow travelers. It taught me patience and resilience in the face of nature."
            },
            "part3": {
                "title": "Extreme Weather, Tourism & Urban Planning",
                "topic": "Weather Disruption & Urban Infrastructure",
                "questions": [
                    "How does extreme weather impact a country's economic and transport infrastructure?",
                    "Do people's leisure activities differ significantly depending on the local climate?",
                    "How can modern city planners design infrastructure that withstands severe weather events?",
                    "Do you think weather forecasting technology has become sufficiently reliable?"
                ],
                "model_answers": [
                    "Severe weather events inflict severe financial setbacks by disrupting supply chains, damaging roads, and causing flight cancellations.",
                    "Climate plays a pivotal role. Residents of colder regions naturally favor indoor sports and thermal retreats, whereas tropical communities engage in outdoor watersports.",
                    "Urban planners must integrate permeable pavements, flood-retention basins, and robust subterranean drainage networks to prevent catastrophic waterlogging.",
                    "Meteorological models powered by supercomputers and satellite telemetry have vastly improved short-term accuracy, though long-term projections remain inherently volatile."
                ]
            }
        },

        # TEST 4: Food & Culinary Culture (Cambridge 17 Test 1)
        {
            "cambridge_book": 17, "test_number": 1, "difficulty_band": 7.5,
            "part1": {
                "title": "Hometown → Food & Cooking",
                "topic": "Hometown & Food",
                "mandatory_topic": "Hometown & Neighbourhood",
                "secondary_topic": "Food & Cooking",
                "questions": [
                    "Is your hometown a good place for young people to grow up? Why?",
                    "Has your hometown changed noticeably in recent years?",
                    "What is your favourite type of food, and how often do you eat it?",
                    "Do you enjoy cooking meals at home or do you prefer dining out?"
                ],
                "model_answers": [
                    "Yes, it has great educational facilities, safe neighbourhoods, and vibrant community parks, making it very hospitable for growing up.",
                    "Significantly. Many modern commercial complexes, flyovers, and IT hubs have emerged over the last decade.",
                    "I am passionate about traditional South Asian culinary dishes, particularly aromatic mutton biryani infused with saffron and indigenous spices.",
                    "I find cooking at home deeply therapeutic and rewarding, though I occasionally dine out on weekends to sample international cuisines."
                ]
            },
            "part2": {
                "title": "Describe a special traditional meal or culinary experience you enjoyed",
                "topic": "Traditional Cuisine",
                "cue_card_prompt": """<div class="cambridge-cue-card-inner"><h4>Describe a special traditional meal or culinary experience you enjoyed.</h4><p><b>You should say:</b></p><ul><li>What the meal consisted of</li><li>Where and with whom you ate it</li><li>Why this meal was prepared</li></ul><p><b>and explain why this culinary experience was particularly memorable.</b></p></div>""",
                "model_answer": "I would like to describe a lavish Bengali feast prepared during the Pohela Boishakh (Bengali New Year) celebration at my grandmother's ancestral home. The centerpiece was traditional Panta Ilish (fermented rice paired with crispy fried Hilsa fish), accompanied by a dozen varieties of spicy mashed vegetable bhortas. The authentic clay plates and heartfelt family bonding made it an unforgettable gastronomic experience."
            },
            "part3": {
                "title": "Food Security, Globalization & Dietary Trends",
                "topic": "Global Food Culture & Nutrition",
                "questions": [
                    "How has globalization influenced people's dietary choices across different continents?",
                    "Should governments impose sugar taxes on unhealthy processed foods?",
                    "What role does food play in preserving cultural heritage and national identity?",
                    "How can sustainable agricultural practices resolve future global food scarcity?"
                ],
                "model_answers": [
                    "Globalization has democratized international cuisines; sushi, pasta, and tacos are now staple options in virtually every metropolitan city worldwide.",
                    "Evidence from several European nations suggests that targeted fiscal disincentives effectively curtail the consumption of sugary beverages and incentivize healthier alternatives.",
                    "Culinary traditions embody ancestral history, local geography, and social customs; preserving traditional recipes is synonymous with guarding intangible cultural heritage.",
                    "Adopting precision agriculture, vertical farming, and drought-resistant crops can maximize caloric yield while minimizing pesticide runoff and soil degradation."
                ]
            }
        },

        # TEST 5: Photography & Visual Arts (Cambridge 17 Test 3)
        {
            "cambridge_book": 17, "test_number": 3, "difficulty_band": 7.5,
            "part1": {
                "title": "Work/Studies → Photography & Visual Arts",
                "topic": "Studies & Photography",
                "mandatory_topic": "Work or Studies",
                "secondary_topic": "Photography & Mobile Snaps",
                "questions": [
                    "What do you find most interesting or challenging about your work or studies?",
                    "Do you see yourself staying in this career path in the future?",
                    "How often do you take photographs using your smartphone or camera?",
                    "Do you prefer taking pictures of landscapes and nature, or photos of people?"
                ],
                "model_answers": [
                    "What fascinates me most is the creative problem-solving aspect, where theoretical models are translated into tangible software solutions.",
                    "Certainly. The technology and data analytics sectors offer continuous professional growth and dynamic international opportunities.",
                    "I take photos almost daily, whether capturing architectural nuances on my commute or documenting spontaneous gatherings with friends.",
                    "I lean toward architectural and natural landscape photography because I love capturing unique lighting, symmetrical lines, and organic textures."
                ]
            },
            "part2": {
                "title": "Describe a photograph of yourself or your family that you cherish",
                "topic": "Cherished Photograph",
                "cue_card_prompt": """<div class="cambridge-cue-card-inner"><h4>Describe a photograph of yourself or your family that you cherish.</h4><p><b>You should say:</b></p><ul><li>When and where the photograph was taken</li><li>Who is in the photograph with you</li><li>What everyone was doing in the picture</li></ul><p><b>and explain why this particular photograph is so precious to you.</b></p></div>""",
                "model_answer": "I would like to speak about a vintage sepia-toned photograph taken during my grandfather's 80th birthday in our ancestral village garden. In the frame, three generations of our family are laughing hysterically while trying to balance a homemade chocolate cake on an uneven wooden table. It captures pure unchoreographed joy and serves as a timeless reminder of familial unity."
            },
            "part3": {
                "title": "Visual Arts, Media Ethics & Artificial Imagery",
                "topic": "Visual Culture & AI Art",
                "questions": [
                    "Why do humans have such a deep emotional connection to visual imagery and paintings?",
                    "How has digital photo manipulation affected the credibility of photojournalism?",
                    "Do you believe AI-generated art can possess genuine emotional and artistic value?",
                    "Should public funding be dedicated to supporting art galleries and museums?"
                ],
                "model_answers": [
                    "Visuals bypass linguistic barriers and directly stimulate the limbic system, evoking visceral nostalgia, empathy, and aesthetic appreciation far quicker than text.",
                    "Pervasive digital manipulation and deepfakes have severely undermined public trust, compelling news agencies to institute stringent cryptographic metadata verification.",
                    "While AI algorithms can synthesize stunning aesthetic compositions, they lack consciousness, emotional suffering, and lived experience, which are the essence of true art.",
                    "Public subsidies for arts institutions are vital to democratize cultural enrichment, ensuring that artistic heritage is accessible to all socioeconomic strata."
                ]
            }
        },

        # TEST 6: Childhood & Memories (Cambridge 16 Test 2)
        {
            "cambridge_book": 16, "test_number": 2, "difficulty_band": 7.5,
            "part1": {
                "title": "Accommodation → Childhood & Growing Up",
                "topic": "Accommodation & Childhood",
                "mandatory_topic": "Home & Accommodation",
                "secondary_topic": "Childhood & Growing Up",
                "questions": [
                    "How long have you lived in your current home?",
                    "Is there anything in particular you would like to change about your home?",
                    "What was your favourite toy or game when you were a child?",
                    "Did you prefer playing outdoors or staying indoors when you were young?"
                ],
                "model_answers": [
                    "My family and I have resided in our current home for roughly six years.",
                    "If given the opportunity, I would love to expand the balcony garden to accommodate more flowering plants and outdoor seating.",
                    "My all-time favorite childhood possession was an intricate LEGO construction set, with which I would spend endless hours designing miniature bridges.",
                    "I was decidedly an outdoor enthusiast; my neighborhood peers and I would play street cricket and badminton until sunset every single evening."
                ]
            },
            "part2": {
                "title": "Describe a valuable skill you learned during your childhood",
                "topic": "Childhood Skill",
                "cue_card_prompt": """<div class="cambridge-cue-card-inner"><h4>Describe a valuable skill you learned during your childhood.</h4><p><b>You should say:</b></p><ul><li>What the skill was</li><li>Who taught it to you and how you learned it</li><li>How difficult it was to master</li></ul><p><b>and explain how this skill has helped you in your adult life.</b></p></div>""",
                "model_answer": "I would like to talk about learning how to swim at the age of eight in a freshwater river near my grandparents' house. My uncle, a seasoned lifeguard, patiently guided me through breathing techniques and freestyle strokes over several summer weeks. Mastering swimming gave me lifelong physical stamina and confidence in emergency aquatic situations."
            },
            "part3": {
                "title": "Childhood Development, Parenting & Education",
                "topic": "Child Psychology & Modern Parenting",
                "questions": [
                    "What are the long-term benefits of unstructured free play in early childhood development?",
                    "How can parents strike a healthy balance between academic discipline and recreational freedom?",
                    "Should schools focus more on practical life skills rather than purely theoretical curricula?",
                    "Do you think modern children mature intellectually faster due to internet access?"
                ],
                "model_answers": [
                    "Unstructured play fosters neural plasticity, social negotiation skills, emotional self-regulation, and creative problem-solving without the pressure of adult judgment.",
                    "Parents should establish clear non-negotiable study boundaries while allocating inviolable blocks for self-directed hobbies and sports.",
                    "Absolutely. Incorporating financial literacy, basic coding, critical media analysis, and interpersonal conflict resolution would produce far more adaptable adults.",
                    "While digital access accelerates access to factual information, it can also lead to premature exposure to complex adult themes without emotional maturity."
                ]
            }
        },

        # TEST 7: Shopping & Personal Style (Cambridge 16 Test 3)
        {
            "cambridge_book": 16, "test_number": 3, "difficulty_band": 7.5,
            "part1": {
                "title": "Hometown → Shopping & Personal Style",
                "topic": "Hometown & Shopping",
                "mandatory_topic": "Hometown & Neighbourhood",
                "secondary_topic": "Shopping & Personal Style",
                "questions": [
                    "Where is your hometown located, and what is it known for?",
                    "Do you think you will continue living in your hometown in the future?",
                    "Do you enjoy shopping for clothes and footwear?",
                    "Do you prefer shopping at physical brick-and-mortar stores or online websites?"
                ],
                "model_answers": [
                    "My hometown is located in the southeastern region of Bangladesh, renowned for its port trade, lush hills, and maritime history.",
                    "While I cherish my roots, I anticipate relocating internationally for postgraduate studies and career advancement over the next few years.",
                    "I view shopping pragmatically rather than as recreation; I shop when I need to replace worn garments or acquire formal attire for specific events.",
                    "I prefer physical stores for footwear and tailored suits where tactile fit is critical, but I utilize e-commerce platforms for electronics and books."
                ]
            },
            "part2": {
                "title": "Describe a purchase you made that you were extremely satisfied with",
                "topic": "Satisfying Purchase",
                "cue_card_prompt": """<div class="cambridge-cue-card-inner"><h4>Describe a purchase you made that you were extremely satisfied with.</h4><p><b>You should say:</b></p><ul><li>What item you bought</li><li>Where and when you purchased it</li><li>Why you needed to buy this particular item</li></ul><p><b>and explain why you were so satisfied with this purchase.</b></p></div>""",
                "model_answer": "I would like to describe an ergonomic noise-canceling headset that I purchased six months ago for my academic study station. Living in a noisy urban apartment, ambient street noise was severely eroding my concentration. This device provides active acoustic isolation and exceptional battery life, allowing me to maintain deep uninterrupted focus for hours."
            },
            "part3": {
                "title": "Consumer Psychology, Advertising & Sustainable Fashion",
                "topic": "Consumerism & Fast Fashion Ethics",
                "questions": [
                    "How do targeted social media advertisements manipulate consumer purchasing impulses?",
                    "What are the severe ecological consequences of the global fast-fashion industry?",
                    "Why are younger generations increasingly embracing thrift stores and secondhand clothing?",
                    "Do you believe material wealth is an accurate indicator of personal fulfillment?"
                ],
                "model_answers": [
                    "Predictive algorithms analyze user browsing telemetry to deliver hyper-personalized ads at moments of peak vulnerability, creating artificial needs.",
                    "Fast fashion generates colossal textile waste in landfills, depletes groundwater reserves for cotton cultivation, and pollutes waterways with synthetic microplastics.",
                    "Gen-Z consumers are acutely conscious of climate ethics and seek distinct vintage aesthetics while protesting against unethical sweatshop labor.",
                    "Sociological research consistently demonstrates that beyond a baseline of financial security, material accumulation yields diminishing returns in happiness."
                ]
            }
        },

        # TEST 8: Animals & Wildlife (Cambridge 15 Test 1)
        {
            "cambridge_book": 15, "test_number": 1, "difficulty_band": 7.5,
            "part1": {
                "title": "Work/Studies → Animals & Nature",
                "topic": "Studies & Wildlife",
                "mandatory_topic": "Work or Studies",
                "secondary_topic": "Animals & Pets",
                "questions": [
                    "Are you currently studying or do you work?",
                    "How do you organize your daily routine to stay productive?",
                    "Did you have any domestic pets when you were growing up?",
                    "What is your favourite wild animal, and why?"
                ],
                "model_answers": [
                    "I am currently an undergraduate student majoring in Engineering and Data Systems.",
                    "I use digital time-blocking calendars, dedicating mornings to analytical work and afternoons to reading and collaboration.",
                    "Yes, our family had a rescue dog who was an affectionate and loyal companion throughout my childhood.",
                    "I have always been mesmerized by the Royal Bengal Tiger; its majestic poise, solitary hunting prowess, and ecological role as an apex predator are truly awe-inspiring."
                ]
            },
            "part2": {
                "title": "Describe an encounter with a wild animal or a visit to a wildlife habitat",
                "topic": "Wildlife Encounter",
                "cue_card_prompt": """<div class="cambridge-cue-card-inner"><h4>Describe an encounter with a wild animal or a visit to a wildlife habitat.</h4><p><b>You should say:</b></p><ul><li>What animal you saw</li><li>Where and when this encounter took place</li><li>What the animal was doing</li></ul><p><b>and explain how you felt during and after this wildlife encounter.</b></p></div>""",
                "model_answer": "I would like to recount an exhilarating boat expedition through the Sundarbans mangrove delta during the winter of 2023. As our silent vessel navigated a narrow brackish canal, we spotted a majestic spotted deer herd grazing cautiously near the riverbank. Witnessing these animals in their undisturbed natural habitat filled me with reverence for untouched ecosystems."
            },
            "part3": {
                "title": "Species Extinction, Zoos & Ecological Equilibrium",
                "topic": "Biodiversity Loss & Ethical Conservation",
                "questions": [
                    "Why are wildlife species disappearing at an unprecedented rate across the globe?",
                    "Are traditional zoological parks ethically justifiable in the twenty-first century?",
                    "How can human-wildlife conflict in rural agricultural zones be sustainably managed?",
                    "Should international laws against illegal wildlife poaching be enforced more rigorously?"
                ],
                "model_answers": [
                    "Anthropogenic habitat fragmentation, illegal poaching, deforestation, and climate-induced ecosystem disruption are the primary catalysts of mass extinction.",
                    "Traditional cramped display cages are ethically indefensible; modern institutions must pivot entirely toward scientific breeding programs and rehabilitation sanctuaries.",
                    "Deploying bio-fences, solar-powered acoustic deterrents, and community insurance funds can compensate farmers without resorting to lethal retaliation.",
                    "Stringent transnational intelligence-sharing and severing financial syndicates in black-market ivory and exotic species trade are essential to stop poaching."
                ]
            }
        }
    ]

    # Insert into database
    for test in speaking_tests:
        book = test["cambridge_book"]
        t_num = test["test_number"]
        band = test["difficulty_band"]

        # 1. Part 1
        p1 = test["part1"]
        p1_ctx = json.dumps({
            "topic": p1["topic"],
            "mandatory_topic": p1.get("mandatory_topic", "General"),
            "secondary_topic": p1.get("secondary_topic", "General"),
            "instructions": "Part 1: Answer the examiner's interview questions fluently (2 on background, 2 on topic)."
        })
        cursor.execute('''INSERT INTO questions 
            (title, skill, test_type, section_number, question_type, passage_or_context, question_text, options_json, answer_key, explanation, difficulty, cambridge_book, test_number, difficulty_band)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (p1["title"], 'Speaking', 'Academic', 1, 'Speaking Part 1 - Interview', p1_ctx,
             "Answer each of the 4 Part 1 questions naturally.", json.dumps(p1["questions"]), json.dumps(p1["model_answers"]),
             "Demonstrate fluency, everyday vocabulary, and coherent sentences without excessive pausing.",
             'medium', book, t_num, band))

        # 2. Part 2
        p2 = test["part2"]
        cursor.execute('''INSERT INTO questions 
            (title, skill, test_type, section_number, question_type, passage_or_context, question_text, options_json, answer_key, explanation, difficulty, cambridge_book, test_number, difficulty_band)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (p2["title"], 'Speaking', 'Academic', 2, 'Speaking Part 2 - Cue Card', p2["cue_card_prompt"],
             "You have 1 minute to prepare and 2 minutes to speak on this cue card topic.", json.dumps([]), p2["model_answer"],
             "Structure your speech using the 4 bullet points. Maintain continuous speech for 1.5 to 2 minutes.",
             'hard', book, t_num, band))

        # 3. Part 3
        p3 = test["part3"]
        p3_ctx = json.dumps({"topic": p3["topic"], "instructions": "Part 3: Provide analytical, well-argued 3-4 sentence answers."})
        cursor.execute('''INSERT INTO questions 
            (title, skill, test_type, section_number, question_type, passage_or_context, question_text, options_json, answer_key, explanation, difficulty, cambridge_book, test_number, difficulty_band)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (p3["title"], 'Speaking', 'Academic', 3, 'Speaking Part 3 - Discussion', p3_ctx,
             "Discuss the broader societal implications with the examiner.", json.dumps(p3["questions"]), json.dumps(p3["model_answers"]),
             "Use discourse markers, counterarguments, and hypothetical examples to support your viewpoint.",
             'hard', book, t_num, band))

    conn.commit()
    conn.close()
    print(f"Successfully seeded {len(speaking_tests)} 2-Stage Authentic Cambridge Speaking sets!")

if __name__ == "__main__":
    seed_authentic_cambridge_speaking()
