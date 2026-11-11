import sqlite3
import os

db_path = 'ielts_platform.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Clear existing grammar rules and mastery
cursor.execute("DELETE FROM grammar_rules")
cursor.execute("DELETE FROM student_grammar_vocab_mastery WHERE item_type = 'grammar'")

rules_seed = [
    # Beginner (Band 4.5-5.5)
    ('Beginner (Band 4.5-5.5)', 'Nouns (Countable & Uncountable)', 'Countable nouns can be pluralized (apples), uncountable nouns cannot (information, advice).', 'The informations are useful.', 'The information is useful.', 'Never add -s to uncountable nouns like advice, research, luggage.'),
    ('Beginner (Band 4.5-5.5)', 'Pronouns (Subject & Object)', 'Use subject pronouns before verbs (I, she, they) and object pronouns after verbs/prepositions (me, her, them).', 'Him went to the store with I.', 'He went to the store with me.', 'Correct pronoun case is essential for basic coherence in Speaking Part 1.'),
    ('Beginner (Band 4.5-5.5)', 'Basic Adjectives', "Adjectives describe nouns and usually come before the noun or after a 'be' verb.", 'He drives a car very fastly.', 'He drives a very fast car.', 'Adjectives do not take plural forms even if the noun is plural.'),
    ('Beginner (Band 4.5-5.5)', 'Basic Adverbs', 'Adverbs describe verbs, adjectives, or other adverbs, often ending in -ly.', 'She speaks English good.', 'She speaks English well.', 'Use well (adverb) instead of good (adjective) when describing an action.'),
    ('Beginner (Band 4.5-5.5)', 'Prepositions of Time & Place', 'Use in for months/years/countries, on for days/surfaces, at for specific times/points.', 'I was born in 5th May at London.', 'I was born on 5th May in London.', 'Preposition errors are very common but easily fixed for a quick Band 5.5 to 6.0 bump.'),
    ('Beginner (Band 4.5-5.5)', 'Basic Conjunctions (And, But, Or, So)', 'Use these coordinating conjunctions to join words, phrases, or independent clauses.', 'I like apples. I like bananas.', 'I like apples and bananas.', 'Combine short sentences to avoid a choppy, low-band writing style.'),
    ('Beginner (Band 4.5-5.5)', 'Present Simple Tense', 'Use for habits, routines, and general facts.', 'The sun is rising in the east.', 'The sun rises in the east.', 'Essential for Task 1 when describing static charts or processes.'),
    
    # Foundational (Band 5.0-6.0)
    ('Foundational (Band 5.0-6.0)', 'Subject-Verb Agreement', 'Singular subjects require singular verbs, plural subjects require plural verbs.', 'The list of items are on the desk.', 'The list of items is on the desk.', 'Watch out for prepositional phrases between subject and verb.'),
    ('Foundational (Band 5.0-6.0)', 'Articles (A/An/The)', 'Use the for specific nouns known to the reader; omit before general uncountable nouns.', 'The government should invest in the education.', 'The government should invest in education.', 'Abstract nouns like education, health, and pollution rarely take the in general statements.'),
    ('Foundational (Band 5.0-6.0)', 'Past Simple Tense', 'Use for completed actions in the past at a specific time.', 'In 2010, the population has increased.', 'In 2010, the population increased.', 'Always use Past Simple with specific past dates (e.g., in 1999) in Task 1 line graphs.'),
    ('Foundational (Band 5.0-6.0)', 'Present Perfect Tense', 'Use for actions starting in the past and continuing to the present, or past actions with present results.', 'I live here since 2015.', 'I have lived here since 2015.', 'Crucial for Speaking Part 1 questions about your hometown or hobbies.'),
    ('Foundational (Band 5.0-6.0)', 'Comparatives & Superlatives', 'Use -er/more for comparing two things, and the -est/the most for comparing three or more.', 'The line graph is more higher than the bar chart.', 'The line graph is higher than the bar chart.', 'Avoid double comparatives (more higher, more better).'),
    ('Foundational (Band 5.0-6.0)', 'Quantifiers', 'Use much/little with uncountable nouns, many/few with countable nouns.', 'There are much students in the class.', 'There are many students in the class.', 'Correct quantifier usage prevents confusion in Task 1 data reporting.'),
    
    # Intermediate (Band 6.5-7.0)
    ('Intermediate (Band 6.5-7.0)', 'Complex Sentence Structures', 'Combine an independent clause with dependent clauses using subordinating conjunctions (Although, Because, While).', 'Although it rained. We went outside.', 'Although it rained, we went outside.', 'Writing Task 2 requires a variety of complex sentences for Band 7.0+ Grammatical Range.'),
    ('Intermediate (Band 6.5-7.0)', 'Relative Clauses (Defining & Non-Defining)', 'Use who/which/that to add essential (defining) or extra (non-defining) information to a noun.', 'The book, that I read, was great.', 'The book that I read was great. OR My father, who is 60, retired.', 'Never use that in non-defining relative clauses (with commas).'),
    ('Intermediate (Band 6.5-7.0)', 'Passive Voice', 'Use to shift focus from the doer to the action/receiver. Form: be + past participle.', 'The government built a new hospital.', 'A new hospital was built (by the government).', 'Extremely important for Task 1 Process Diagrams to maintain an objective tone.'),
    ('Intermediate (Band 6.5-7.0)', 'Conditionals (Type 1 & 2)', 'Type 1 for real future possibilities (If + present, will + verb). Type 2 for unreal present/future (If + past, would + verb).', 'If I will win the lottery, I will travel.', 'If I win the lottery, I will travel.', 'Excellent for proposing solutions in Task 2 Problem/Solution essays.'),
    ('Intermediate (Band 6.5-7.0)', 'Gerunds vs Infinitives', 'Some verbs are followed by V-ing (enjoy reading), others by to + V (want to read).', 'I look forward to hear from you.', 'I look forward to hearing from you.', 'Prepositions are always followed by gerunds (V-ing).'),
    
    # Advanced Master (Band 7.5-9.0)
    ('Advanced Master (Band 7.5-9.0)', 'Inversion for Emphasis', 'Invert subject and auxiliary verb after negative adverbial phrases (e.g. Not only, Rarely, Seldom).', 'Not only governments should act, but also individuals.', 'Not only should governments act, but individuals must also take responsibility.', 'Inversion showcases Band 8.5+ advanced grammatical control when used accurately.'),
    ('Advanced Master (Band 7.5-9.0)', 'Nominalization', 'Convert verbs and adjectives into academic noun phrases to create an objective formal tone.', 'Because cars increased rapidly, air quality got worse.', 'The rapid increase in motor vehicles resulted in severe air quality degradation.', 'Nominalization is essential for Band 8.0 Task 1 reports and Task 2 academic tone.'),
    ('Advanced Master (Band 7.5-9.0)', 'Mixed Conditionals (Type 3 & Mixed)', 'Use to express unreal past situations and their past/present results.', 'If I studied harder, I would have passed.', 'If I had studied harder, I would have passed.', 'Use to discuss hypothetical historical consequences in Speaking Part 3.'),
    ('Advanced Master (Band 7.5-9.0)', 'Participle Clauses', 'Use -ing or -ed clauses to reduce relative clauses and combine sentences elegantly.', 'The man who was walking down the street saw a dog.', 'Walking down the street, the man saw a dog.', 'Demonstrates exceptional sentence variety and compactness.'),
    ('Advanced Master (Band 7.5-9.0)', 'Cleft Sentences', 'Use It is/was... that... or What... is... to emphasize a specific part of a sentence.', 'I need more time.', 'What I really need is more time.', 'Highly effective for emphasis in Speaking Part 3 to show advanced fluency.'),
    ('Advanced Master (Band 7.5-9.0)', 'Advanced Modals of Speculation', 'Use modal + have + past participle to speculate about the past.', 'He must be left his keys.', 'He must have left his keys.', 'Perfect for answering speculative questions in Speaking Part 3.')
]

cursor.executemany("INSERT INTO grammar_rules (level_tier, topic_name, rule_description, common_error, correct_example, cambridge_tip) VALUES (?, ?, ?, ?, ?, ?)", rules_seed)

mastery_seed = []
for idx, rule in enumerate(rules_seed):
    level = rule[0]
    topic = rule[1]
    
    # Initial dummy mastery logic to show varying progress
    if 'Beginner' in level:
        stage = 'Mastered'
        active = 85.0
        passive = 60.0
    elif 'Foundational' in level:
        stage = 'Contextualized'
        active = 65.0
        passive = 45.0
    elif 'Intermediate' in level:
        stage = 'Seen'
        active = 30.0
        passive = 20.0
    else:
        stage = 'Unseen'
        active = 0.0
        passive = 0.0
        
    mastery_seed.append((1, 'grammar', topic, level, stage, passive, active))

cursor.executemany("INSERT INTO student_grammar_vocab_mastery (user_id, item_type, topic_or_word, category, mastery_stage, passive_mastery_pct, active_mastery_pct) VALUES (?, ?, ?, ?, ?, ?, ?)", mastery_seed)

conn.commit()
conn.close()
print(f"Successfully seeded {len(rules_seed)} comprehensive grammar rules!")