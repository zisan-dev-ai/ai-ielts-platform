# -*- coding: utf-8 -*-
"""
Master AI Human Teacher Engine — Complete IELTS Academic & GT Taxonomy
Real lesson content, AI-enhanced teaching, database-driven questions, smart evaluation.
"""
import sys
import json
from typing import Dict, Any, Optional, List
from database import get_db

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ═══════════════════════════════════════════════════════════════════════
# MASTER TAXONOMY — Complete IELTS Question Type Tree
# ═══════════════════════════════════════════════════════════════════════

MASTER_TAXONOMY = {
    'Listening': [
        {'type': 'Multiple Choice — One Answer', 'tag': 'Distractor Recognition', 'icon': '🎧'},
        {'type': 'Multiple Choice — More Than One Answer', 'tag': 'Multi-Detail Extraction', 'icon': '🎧'},
        {'type': 'Matching', 'tag': 'Synonym Matching', 'icon': '🎧'},
        {'type': 'Plan Labelling', 'tag': 'Spatial Navigation', 'icon': '🗺️'},
        {'type': 'Map Labelling', 'tag': 'Directional Language', 'icon': '🗺️'},
        {'type': 'Diagram Labelling', 'tag': 'Process Sequence', 'icon': '🔧'},
        {'type': 'Form Completion', 'tag': 'Numbers & Spelling', 'icon': '📝'},
        {'type': 'Note Completion', 'tag': 'Spelling & Names', 'icon': '📝'},
        {'type': 'Table Completion', 'tag': 'Data Categorization', 'icon': '📊'},
        {'type': 'Flow-chart Completion', 'tag': 'Step-by-step Process', 'icon': '📊'},
        {'type': 'Summary Completion', 'tag': 'Context Prediction', 'icon': '📝'},
        {'type': 'Sentence Completion', 'tag': 'Grammar & Part of Speech', 'icon': '📝'},
        {'type': 'Short-answer Questions', 'tag': 'Exact Word Retrieval', 'icon': '📝'}
    ],
    'Reading': [
        {'type': 'Multiple Choice', 'tag': 'Main Idea & Paraphrasing', 'icon': '📖'},
        {'type': 'True / False / Not Given', 'tag': 'Evidence Identification', 'icon': '📖'},
        {'type': 'Yes / No / Not Given', 'tag': "Writer's Claim & Opinion", 'icon': '📖'},
        {'type': 'Matching Information', 'tag': 'Locating Specific Detail', 'icon': '📖'},
        {'type': 'Matching Headings', 'tag': 'Main Idea Identification', 'icon': '📖'},
        {'type': 'Matching Features', 'tag': 'Author & Theory Attribution', 'icon': '📖'},
        {'type': 'Matching Sentence Endings', 'tag': 'Coherence & Grammar', 'icon': '📖'},
        {'type': 'Sentence Completion', 'tag': 'Paraphrase Matching', 'icon': '📝'},
        {'type': 'Summary Completion', 'tag': 'Vocabulary in Context', 'icon': '📝'},
        {'type': 'Note Completion', 'tag': 'Key Detail Extraction', 'icon': '📝'},
        {'type': 'Table Completion', 'tag': 'Structural Data Alignment', 'icon': '📊'},
        {'type': 'Flow-chart Completion', 'tag': 'Sequential Reasoning', 'icon': '📊'},
        {'type': 'Diagram Label Completion', 'tag': 'Visual-to-Text Mapping', 'icon': '🗺️'},
        {'type': 'Short-answer Questions', 'tag': 'Direct Evidence Scanning', 'icon': '📝'}
    ],
    'Writing': [
        {'type': 'Line Graph (Academic Task 1)', 'tag': 'Trend & Overview Analysis', 'icon': '📈'},
        {'type': 'Bar Chart (Academic Task 1)', 'tag': 'Comparative Data Analysis', 'icon': '📊'},
        {'type': 'Pie Chart (Academic Task 1)', 'tag': 'Proportional Breakdown', 'icon': '🥧'},
        {'type': 'Table (Academic Task 1)', 'tag': 'Complex Matrix Overview', 'icon': '📋'},
        {'type': 'Process Diagram (Academic Task 1)', 'tag': 'Sequential Passive Voice', 'icon': '🔄'},
        {'type': 'Map (Academic Task 1)', 'tag': 'Spatial Change Analysis', 'icon': '🗺️'},
        {'type': 'Formal Letter (GT Task 1)', 'tag': 'Formal Complaint & Request', 'icon': '✉️'},
        {'type': 'Semi-formal Letter (GT Task 1)', 'tag': 'Professional Request', 'icon': '✉️'},
        {'type': 'Informal Letter (GT Task 1)', 'tag': 'Personal Invitation', 'icon': '💌'},
        {'type': 'Opinion Essay (Task 2)', 'tag': 'Thesis Statement & Position', 'icon': '✍️'},
        {'type': 'Agree / Disagree Essay (Task 2)', 'tag': 'Strong Argumentation', 'icon': '⚖️'},
        {'type': 'Discussion Essay (Task 2)', 'tag': 'Balanced Argumentation', 'icon': '🗣️'},
        {'type': 'Advantages / Disadvantages Essay (Task 2)', 'tag': 'Evaluation & Outweigh', 'icon': '⚖️'},
        {'type': 'Problem / Solution Essay (Task 2)', 'tag': 'Cause & Action Analysis', 'icon': '🧩'},
        {'type': 'Two-Part Question Essay (Task 2)', 'tag': 'Dual Response Structure', 'icon': '🧩'}
    ],
    'Speaking': [
        {'type': 'Part 1 Personal Questions', 'tag': 'Answer Extension Formula', 'icon': '🗣️'},
        {'type': 'Part 2 Cue Card', 'tag': 'Story Structure & Monologue', 'icon': '⏱️'},
        {'type': 'Part 3 Opinion & Discussion', 'tag': 'Abstract Reasoning & Evaluation', 'icon': '🧠'},
        {'type': 'Part 3 Comparison', 'tag': 'Past vs Present Analytical Shift', 'icon': '⚖️'},
        {'type': 'Part 3 Prediction', 'tag': 'Future Speculation Structures', 'icon': '🔮'}
    ]
}

# ═══════════════════════════════════════════════════════════════════════
# LESSON CONTENT — Real Teaching Material for Every Question Type
# ═══════════════════════════════════════════════════════════════════════

LESSON_CONTENT = {
    # ──── READING ────
    'True / False / Not Given': {
        'rule_eng': 'TRUE means the statement agrees with the passage information. FALSE means the statement directly contradicts the passage. NOT GIVEN means the passage does not contain this information at all — you cannot determine whether it is true or false. CRITICAL: Do NOT use your own knowledge. Only use what the passage says. Look for synonyms and paraphrases, never expect exact word matches.',
        'rule_bn': 'TRUE মানে বক্তব্যটি passage-এর তথ্যের সাথে মিলে যায়। FALSE মানে বক্তব্যটি passage-এর তথ্যের সরাসরি বিপরীত। NOT GIVEN মানে passage-এ এই বিষয়ে কোনো তথ্যই নেই। গুরুত্বপূর্ণ: নিজের জ্ঞান ব্যবহার করো না। শুধুমাত্র passage যা বলে তার ভিত্তিতে উত্তর দাও। হুবহু একই শব্দ নয়, সমার্থক শব্দ (synonym) ও paraphrase খোঁজো।',
        'demo_eng': '📄 Passage: "The Eiffel Tower was completed in 1889 for the World\'s Fair in Paris."\n\n❓ Statement: "The Eiffel Tower was built for a cultural exhibition."\n\n✅ Answer: TRUE\n\n💡 Why? "World\'s Fair" is a paraphrase of "cultural exhibition". The meaning matches even though the exact words differ. This is the #1 skill IELTS tests — can you recognize paraphrases?',
        'demo_bn': '📄 Passage: "আইফেল টাওয়ার ১৮৮৯ সালে প্যারিসের বিশ্বমেলার জন্য নির্মাণ সম্পন্ন হয়।"\n\n❓ Statement: "আইফেল টাওয়ার একটি সাংস্কৃতিক প্রদর্শনীর জন্য নির্মিত হয়েছিল।"\n\n✅ উত্তর: TRUE\n\n💡 কেন? "বিশ্বমেলা" হলো "সাংস্কৃতিক প্রদর্শনী"-র paraphrase। শব্দ আলাদা কিন্তু অর্থ একই।',
        'tips': ['প্রথমে STATEMENT পড়ো, তারপর passage-এ সেই অংশটি খোঁজো', 'Passage-এ বিষয়টি নিয়ে কিছুই বলা না থাকলে → NOT GIVEN', '"always", "never", "all", "none" — এই extreme শব্দগুলো দেখলে সাবধান, প্রায়ই FALSE হয়', 'FALSE আর NOT GIVEN-এর মধ্যে পার্থক্য: FALSE = passage বিপরীত কথা বলে, NOT GIVEN = passage কিছুই বলে না', 'নিজের জ্ঞান দিয়ে উত্তর দিও না — শুধু passage-এর তথ্য ব্যবহার করো']
    },

    'Yes / No / Not Given': {
        'rule_eng': 'YES/NO/NOT GIVEN is about the WRITER\'S VIEWS or CLAIMS, not facts. YES = the writer agrees with the statement. NO = the writer disagrees. NOT GIVEN = the writer does not express an opinion on this. The key difference from T/F/NG: here you are matching OPINIONS, not facts.',
        'rule_bn': 'YES/NO/NOT GIVEN হলো লেখকের মতামত বা দাবি সম্পর্কে, তথ্য নয়। YES = লেখক বক্তব্যের সাথে একমত। NO = লেখক দ্বিমত পোষণ করেন। NOT GIVEN = লেখক এই বিষয়ে কোনো মতামত প্রকাশ করেননি। T/F/NG-এর সাথে মূল পার্থক্য: এখানে তুমি মতামত মিলাচ্ছ, তথ্য নয়।',
        'demo_eng': '📄 Passage: "Carlyle described industrialization as bringing both material progress and spiritual degradation."\n\n❓ Statement: "Carlyle believed industrialization was entirely beneficial."\n\n✅ Answer: NO — Carlyle saw BOTH positives AND negatives, so he did NOT view it as entirely beneficial.',
        'demo_bn': '📄 Passage: "কার্লাইল শিল্পায়নকে বস্তুগত অগ্রগতি এবং আধ্যাত্মিক অবক্ষয় উভয়ই বলে বর্ণনা করেছেন।"\n\n❓ Statement: "কার্লাইল বিশ্বাস করতেন শিল্পায়ন সম্পূর্ণ উপকারী ছিল।"\n\n✅ উত্তর: NO — কার্লাইল ইতিবাচক ও নেতিবাচক দুটোই দেখেছেন, তাই "সম্পূর্ণ উপকারী" বলা ভুল।',
        'tips': ['লেখকের মতামত বোঝার জন্য "believe", "argue", "suggest", "claim" শব্দগুলো খোঁজো', '"entirely", "completely", "only" এই শব্দগুলো statement-এ থাকলে সাবধান — NO হওয়ার সম্ভাবনা বেশি', 'T/F/NG vs Y/N/NG: প্রশ্নের heading দেখো — "Do the following statements agree with the VIEWS of the writer?" = Y/N/NG']
    },

    'Multiple Choice': {
        'rule_eng': 'Read the question stem BEFORE looking at options. Locate the relevant paragraph in the passage. Eliminate obviously wrong options first. The correct answer will always be a paraphrase of the passage — never an exact word-for-word copy. Beware of options that use words from the passage but change the meaning.',
        'rule_bn': 'অপশন দেখার আগে প্রশ্নটি ভালো করে পড়ো। Passage-এ সঠিক অনুচ্ছেদটি খুঁজে বের করো। স্পষ্টভাবে ভুল অপশনগুলো আগে বাদ দাও। সঠিক উত্তর সবসময় passage-এর paraphrase হবে — কখনো হুবহু কপি নয়। Passage-এর শব্দ ব্যবহার করেও অর্থ পরিবর্তন করা অপশন থেকে সাবধান।',
        'demo_eng': '📄 Passage: "Despite its arid climate, the desert supports a surprising variety of flora and fauna."\n\n❓ Question: What is surprising about the desert?\nA) Its extreme temperatures  B) Its biological diversity  C) Its size  D) Its water sources\n\n✅ Answer: B — "variety of flora and fauna" = "biological diversity" (paraphrase)',
        'demo_bn': '📄 Passage: "শুষ্ক জলবায়ু সত্ত্বেও, মরুভূমিতে আশ্চর্যজনকভাবে নানা ধরণের উদ্ভিদ ও প্রাণী দেখা যায়।"\n\n❓ প্রশ্ন: মরুভূমি সম্পর্কে আশ্চর্যজনক কী?\n\n✅ উত্তর: B (জৈবিক বৈচিত্র্য) — "নানা ধরণের উদ্ভিদ ও প্রাণী" = "জৈবিক বৈচিত্র্য"',
        'tips': ['প্রশ্ন আগে পড়ো, তারপর passage-এ scan করো', 'Passage-এর শব্দ হুবহু থাকা অপশন প্রায়ই ভুল (detail trap)', 'সব অপশন পড়ো — "most correct" টা বাছো, শুধু "correct" নয়']
    },

    'Matching Headings': {
        'rule_eng': 'Each heading represents the MAIN IDEA of a paragraph. Read the first 2 sentences and last sentence of each paragraph — they usually contain the main idea. Do NOT choose a heading because it mentions a word from the paragraph. The heading must capture the OVERALL theme, not just one detail.',
        'rule_bn': 'প্রতিটি heading একটি অনুচ্ছেদের মূল ধারণা (main idea) প্রকাশ করে। প্রতিটি অনুচ্ছেদের প্রথম ২টি বাক্য এবং শেষ বাক্য পড়ো — এগুলোতে সাধারণত main idea থাকে। শুধু একটি শব্দ মিলে গেলেই heading নির্বাচন করো না। Heading-কে পুরো অনুচ্ছেদের সামগ্রিক বিষয়বস্তু ধরতে হবে।',
        'demo_eng': '📄 Paragraph A: "Solar panel efficiency has doubled since 2010 while costs have fallen by 80%. This has made solar energy the fastest-growing power source globally."\n\n❓ Choose the heading:\ni) The Decline of Solar Manufacturing  ii) Economic and Technological Breakthrough in Solar Energy\n\n✅ Answer: ii — Both efficiency (tech) AND cost reduction (economic) are covered. Heading i is a DETAIL TRAP.',
        'demo_bn': '📄 Paragraph A: "২০১০ সাল থেকে সৌর প্যানেলের দক্ষতা দ্বিগুণ হয়েছে এবং খরচ ৮০% কমেছে।"\n\n✅ উত্তর: ii (অর্থনৈতিক ও প্রযুক্তিগত সাফল্য) — দক্ষতা (tech) + খরচ হ্রাস (economic) দুটোই আছে। i হলো DETAIL TRAP।',
        'tips': ['অনুচ্ছেদ পড়ার আগে heading list পড়ো না — আগে paragraph-এর main idea নিজে বুঝো', 'প্রথম ও শেষ বাক্যে main idea থাকে ৮০% ক্ষেত্রে', 'Detail Trap: একটি নির্দিষ্ট তথ্য দেখে heading নির্বাচন করো না — পুরো paragraph-এর theme দেখো']
    },

    'Matching Information': {
        'rule_eng': 'You must match a piece of information to the CORRECT PARAGRAPH. The information will be paraphrased. Scan each paragraph for the key concept, not exact words. One paragraph may contain answers to multiple questions, and some paragraphs may not be used.',
        'rule_bn': 'তোমাকে একটি তথ্যকে সঠিক অনুচ্ছেদের সাথে মেলাতে হবে। তথ্যটি paraphrase করা থাকবে। প্রতিটি অনুচ্ছেদে মূল ধারণাটি scan করো, হুবহু শব্দ নয়।',
        'demo_eng': '❓ "Which paragraph mentions a discovery from the 20th century involving a burial chamber?"\n✅ Paragraph 4 — Tutankhamun\'s tomb (burial chamber) discovered in 1922 (20th century).',
        'demo_bn': '❓ "কোন অনুচ্ছেদে ২০শ শতকে একটি সমাধি কক্ষ আবিষ্কারের কথা বলা হয়েছে?"\n✅ অনুচ্ছেদ ৪ — তুতানখামুনের সমাধি (সমাধি কক্ষ) ১৯২২ সালে (২০শ শতক) আবিষ্কৃত হয়েছিল।',
        'tips': ['প্রতিটি তথ্যের keywords highlight করো', 'Passage-এ synonym/paraphrase খোঁজো', 'একটি paragraph একাধিক উত্তরে ব্যবহৃত হতে পারে']
    },

    'Matching Features': {
        'rule_eng': 'Match statements or descriptions to specific people, theories, dates, or places mentioned in the passage. Focus on WHO said/did WHAT. Names and proper nouns are your scanning anchors.',
        'rule_bn': 'বক্তব্য বা বর্ণনাকে passage-এ উল্লিখিত নির্দিষ্ট ব্যক্তি, তত্ত্ব, তারিখ বা স্থানের সাথে মেলাও। কে কী বলেছে/করেছে সেদিকে মনোযোগ দাও।',
        'demo_eng': '❓ "Which researcher emphasized social interaction in learning?"\n✅ Professor Vygotsky — "Vygotsky emphasized the role of social interaction in learning."',
        'demo_bn': '❓ "কোন গবেষক শিক্ষায় সামাজিক মিথস্ক্রিয়ার ওপর জোর দিয়েছিলেন?"\n✅ অধ্যাপক ভাইগটস্কি — "ভাইগটস্কি শিক্ষায় সামাজিক মিথস্ক্রিয়ার ভূমিকার ওপর জোর দিয়েছিলেন।"',
        'tips': ['নাম, তারিখ, জায়গা — এগুলো scanning anchor', 'একই ব্যক্তি একাধিক উত্তরের সাথে যুক্ত হতে পারে', 'Passage-এ নামের পাশের verb/claim/theory পড়ো']
    },

    'Matching Sentence Endings': {
        'rule_eng': 'Complete the sentence by choosing the correct ending from a list. The completed sentence must be grammatically correct AND match the passage meaning. Focus on both GRAMMAR and CONTENT.',
        'rule_bn': 'তালিকা থেকে সঠিক ending বেছে বাক্যটি সম্পূর্ণ করো। সম্পূর্ণ বাক্যটি ব্যাকরণগতভাবে সঠিক হতে হবে এবং passage-এর অর্থের সাথে মিলতে হবে।',
        'demo_eng': '❓ "Developing countries have become major exporters but..."\n✅ "...they still rely on wealthier nations for technology and capital." — Matches both grammar and passage content.',
        'demo_bn': '❓ "উন্নয়নশীল দেশগুলো বড় রপ্তানিকারক হয়েছে কিন্তু..."\n✅ "...তারা এখনও প্রযুক্তি ও পুঁজির জন্য ধনী দেশগুলোর ওপর নির্ভরশীল।"',
        'tips': ['আগে sentence stem পড়ো, তারপর passage-এ locate করো', 'Grammar check করো — subject-verb agreement, tense']
    },

    'Sentence Completion': {
        'rule_eng': 'Fill in the blank with words DIRECTLY FROM THE PASSAGE. The word limit is usually 1-3 words. Do NOT change the form of the word (singular/plural, tense). The answer must fit grammatically.',
        'rule_bn': 'শূন্যস্থান সরাসরি PASSAGE থেকে শব্দ দিয়ে পূরণ করো। শব্দ সীমা সাধারণত ১-৩ শব্দ। শব্দের রূপ পরিবর্তন করো না (একবচন/বহুবচন, কাল)।',
        'demo_eng': '❓ "The part of the brain that controls planning is the _____"\n✅ "prefrontal cortex" — directly from the passage.',
        'demo_bn': '❓ "মস্তিষ্কের যে অংশ পরিকল্পনা নিয়ন্ত্রণ করে সেটি হলো _____"\n✅ "prefrontal cortex" — সরাসরি passage থেকে।',
        'tips': ['Word limit মানো — "NO MORE THAN THREE WORDS" মানে ৩ শব্দের বেশি নয়', 'Passage-এর হুবহু শব্দ ব্যবহার করো, নিজের শব্দ নয়']
    },

    'Summary Completion': {
        'rule_eng': 'Complete a summary of the passage using words from the passage OR from a given word list. Read the summary first to understand its structure. Then find the relevant section in the passage. Words must fit both MEANING and GRAMMAR.',
        'rule_bn': 'Passage থেকে বা দেওয়া শব্দ তালিকা থেকে শব্দ দিয়ে summary পূরণ করো। আগে summary পড়ো গঠন বুঝতে। তারপর passage-এ সংশ্লিষ্ট অংশ খোঁজো।',
        'demo_eng': '❓ "Plants use _____ to convert carbon dioxide and water into glucose."\n✅ "chlorophyll" — The passage says "Using chlorophyll in their leaves, they transform..."',
        'demo_bn': '❓ "উদ্ভিদ কার্বন ডাই-অক্সাইড ও পানিকে গ্লুকোজে রূপান্তর করতে _____ ব্যবহার করে।"\n✅ "ক্লোরোফিল"',
        'tips': ['Summary-র গঠন passage-এর sequence অনুসরণ করে', 'Word list থাকলে, অর্থ ও grammar দুটোই চেক করো']
    },

    'Note Completion': {
        'rule_eng': 'Complete notes by extracting key information from the passage. Notes are usually organized by topic or category. Focus on specific details: names, numbers, dates, places.',
        'rule_bn': 'Passage থেকে মূল তথ্য বের করে notes পূরণ করো। Notes সাধারণত বিষয় বা ক্যাটাগরি অনুযায়ী সাজানো থাকে। নির্দিষ্ট তথ্য: নাম, সংখ্যা, তারিখ, স্থান — এগুলোতে ফোকাস করো।',
        'demo_eng': '❓ "Hazards should be reported to the _____ officer."\n✅ "safety" — directly stated in the passage.',
        'demo_bn': '❓ "ঝুঁকিগুলো _____ অফিসারের কাছে রিপোর্ট করতে হবে।"\n✅ "safety" — সরাসরি passage-এ বলা আছে।',
        'tips': ['Note format-এর heading/category দেখে passage-এ scanning করো', 'সংখ্যা ও proper noun সাধারণত exact copy হয়']
    },

    'Table Completion': {
        'rule_eng': 'Fill in a table by finding specific data points in the passage. Read the table headers first to understand categories. Scan the passage for matching information in the correct row/column.',
        'rule_bn': 'Passage থেকে নির্দিষ্ট তথ্য খুঁজে table পূরণ করো। আগে table-এর header পড়ো ক্যাটাগরি বুঝতে। সঠিক row/column-এ মিলানো তথ্য passage-এ scan করো।',
        'demo_eng': '❓ "Which group had the lowest rates of heart disease?"\n✅ "Group A" — The passage states "Group A had the lowest rates of heart disease."',
        'demo_bn': '❓ "কোন গ্রুপে হৃদরোগের হার সবচেয়ে কম ছিল?"\n✅ "Group A"',
        'tips': ['Table-এর column header ব্যবহার করে passage-এ scan করো', 'Passage-এ তথ্য table-এর মতো সাজানো নাও থাকতে পারে']
    },

    'Flow-chart Completion': {
        'rule_eng': 'Complete a flow-chart showing a process or sequence. The flow-chart follows the ORDER of events in the passage. Use sequencing words (first, then, next, finally) as clues to locate answers.',
        'rule_bn': 'একটি প্রক্রিয়া বা ক্রম দেখানো flow-chart পূরণ করো। Flow-chart passage-এ ঘটনার ক্রম অনুসরণ করে। Sequencing শব্দ (first, then, next, finally) clue হিসেবে ব্যবহার করো।',
        'demo_eng': '❓ "After sedimentation, water passes through _____ filters."\n✅ "sand and gravel" — The sequence: sedimentation → sand and gravel filters → chlorination.',
        'demo_bn': '❓ "সেডিমেন্টেশনের পর পানি _____ ফিল্টারের মধ্য দিয়ে যায়।"\n✅ "sand and gravel" (বালি ও নুড়িপাথর)',
        'tips': ['ক্রম গুরুত্বপূর্ণ — "after", "before", "then" শব্দগুলো দেখো', 'Flow-chart-এর তীরচিহ্ন ক্রম নির্দেশ করে']
    },

    'Diagram Label Completion': {
        'rule_eng': 'Label parts of a diagram using information from the passage. Match descriptive text to visual elements. Pay attention to spatial relationships and technical terms.',
        'rule_bn': 'Passage-এর তথ্য ব্যবহার করে diagram-এর অংশগুলো label করো। বর্ণনামূলক পাঠ্যকে ভিজুয়াল উপাদানের সাথে মেলাও।',
        'demo_eng': '❓ "In which phase do sister chromatids separate?"\n✅ "Anaphase" — "Sister chromatids separate in anaphase."',
        'demo_bn': '❓ "কোন পর্যায়ে সিস্টার ক্রোমাটিড আলাদা হয়?"\n✅ "অ্যানাফেজ"',
        'tips': ['Diagram-এর label সংখ্যা/তীরচিহ্ন passage-এর বর্ণনার সাথে মেলাও', 'Process diagram-এ ক্রম অনুসরণ করো']
    },

    'Short-answer Questions': {
        'rule_eng': 'Answer with a SHORT phrase using words from the passage (usually 1-3 words). Read the question carefully to identify WHAT information is needed (when, where, how many, who). Scan for keywords.',
        'rule_bn': 'Passage থেকে শব্দ দিয়ে সংক্ষিপ্ত উত্তর দাও (সাধারণত ১-৩ শব্দ)। প্রশ্ন ভালো করে পড়ো কী তথ্য চাওয়া হচ্ছে বুঝতে (কখন, কোথায়, কতগুলো, কে)।',
        'demo_eng': '❓ "How many books can a member borrow at once?" → ✅ "6"',
        'demo_bn': '❓ "একজন সদস্য একসাথে কতগুলো বই ধার নিতে পারে?" → ✅ "৬"',
        'tips': ['Question word (what/when/where/how many) দেখো — এটাই বলে দেবে কী ধরনের উত্তর খুঁজতে হবে', 'Word limit strictly মানো']
    },

    # ──── LISTENING ────
    'Form Completion': {
        'rule_eng': 'Listen for specific details to fill in a form: names, addresses, phone numbers, dates, reference numbers. CRITICAL: Speakers often CORRECT themselves — always use the CORRECTED information. Predict what type of answer is needed before listening (number? name? date?).',
        'rule_bn': 'একটি ফর্ম পূরণের জন্য নির্দিষ্ট তথ্য শোনো: নাম, ঠিকানা, ফোন নম্বর, তারিখ, রেফারেন্স নম্বর। গুরুত্বপূর্ণ: বক্তারা প্রায়ই নিজেদের সংশোধন করেন — সবসময় সংশোধিত তথ্য ব্যবহার করো। শোনার আগে অনুমান করো কী ধরনের উত্তর লাগবে (সংখ্যা? নাম? তারিখ?)।',
        'demo_eng': '🎧 Audio: "My number is 07742... oh wait, sorry, it\'s 07856 391204."\n✅ Answer: 07856 391204 — The speaker CORRECTED the number. This is a classic IELTS distractor trap!',
        'demo_bn': '🎧 অডিও: "আমার নম্বর 07742... ওহ দাঁড়ান, সেটা 07856 391204।"\n✅ উত্তর: 07856 391204 — বক্তা নম্বরটি সংশোধন করেছেন। এটি IELTS-এর ক্লাসিক distractor trap!',
        'tips': ['Self-correction শুনলে সবসময় দ্বিতীয় (সংশোধিত) তথ্য নাও', 'শোনার আগে ফর্মের gap দেখে predict করো কী ধরনের তথ্য আসবে', 'Spelling শুনলে প্রতিটি letter মনোযোগ দিয়ে লেখো']
    },

    'Note Completion': {
        'rule_eng': 'Listen and complete notes with key details. Notes are typically in bullet or outline format. Focus on names, dates, specific facts. Words must be EXACTLY as heard (respecting word limits).',
        'rule_bn': 'শুনে মূল তথ্য দিয়ে notes পূরণ করো। Notes সাধারণত bullet বা outline format-এ থাকে। নাম, তারিখ, নির্দিষ্ট তথ্যে ফোকাস করো।',
        'demo_eng': '🎧 "My name is Priya Chakraborty. That\'s C-H-A-K-R-A-B-O-R-T-Y."\n✅ Answer: Chakraborty — spelled out letter by letter.',
        'demo_bn': '🎧 "আমার নাম প্রিয়া চক্রবর্তী। C-H-A-K-R-A-B-O-R-T-Y।"\n✅ উত্তর: Chakraborty',
        'tips': ['Spelling শোনার সময় প্রতিটি letter লিখে যাও', 'Common confusing letters: M/N, B/V, A/E — context দিয়ে বুঝো']
    },

    'Map Labelling': {
        'rule_eng': 'Listen for directional language to identify locations on a map. Key phrases: "turn left/right", "opposite", "next to", "behind", "in front of", "at the end of the corridor", "second door on your right". Trace the route mentally as you listen.',
        'rule_bn': 'মানচিত্রে অবস্থান চিহ্নিত করতে দিকনির্দেশনামূলক ভাষা শোনো। মূল phrases: "বাঁয়ে/ডানে ঘোরো", "বিপরীতে", "পাশে", "পেছনে"। শোনার সময় মনে মনে পথ অনুসরণ করো।',
        'demo_eng': '🎧 "Turn left past the café, the Seminar Room B is the third door on your right."\n✅ Answer: B (Third door on right past café) — Follow the directions step by step.',
        'demo_bn': '🎧 "ক্যাফে পার হয়ে বাঁয়ে ঘোরো, সেমিনার রুম B হলো তোমার ডানদিকে তৃতীয় দরজা।"\n✅ উত্তর: B',
        'tips': ['শোনার আগে মানচিত্রে North/South/entrance চিহ্নিত করো', '"turn left", "past", "opposite" — এই শব্দগুলো direction-এর clue', 'মনে মনে হাঁটার মতো করে route follow করো']
    },

    'Multiple Choice — One Answer': {
        'rule_eng': 'Listen for the answer among distractors. The correct answer is often paraphrased — NOT the same words as in the audio. Speakers may mention all options but only CONFIRM one. Listen for self-corrections and emphasis.',
        'rule_bn': 'Distractor-এর মধ্য থেকে সঠিক উত্তর শোনো। সঠিক উত্তর প্রায়ই paraphrase করা থাকে — অডিওর হুবহু শব্দ নয়। বক্তা সব অপশন উল্লেখ করতে পারেন কিন্তু শুধু একটি নিশ্চিত করবেন।',
        'demo_eng': '🎧 "It was on the 15th... actually no, it was the 16th of March."\n✅ Answer: C) 16th of March — Self-correction! Always take the corrected answer.',
        'demo_bn': '🎧 "এটা ১৫ তারিখে হয়েছিল... আসলে না, ১৬ মার্চ।"\n✅ উত্তর: C) ১৬ মার্চ — Self-correction শুনলে সংশোধিত উত্তর নাও।',
        'tips': ['সব অপশন শোনার পর সিদ্ধান্ত নাও', '"actually", "I mean", "sorry, I meant" — self-correction শব্দ', 'প্রথম শোনা উত্তর সবসময় সঠিক নয়']
    },

    'Multiple Choice — More Than One Answer': {
        'rule_eng': 'Select TWO or MORE correct answers from the options. Listen carefully for which items are specifically recommended, agreed upon, or confirmed. Distractors will also be mentioned but rejected or not confirmed.',
        'rule_bn': 'অপশন থেকে দুই বা ততোধিক সঠিক উত্তর নির্বাচন করো। কোন বিষয়গুলো specifically সুপারিশ করা হয়েছে, একমত হওয়া হয়েছে বা নিশ্চিত করা হয়েছে সেটি মনোযোগ দিয়ে শোনো।',
        'demo_eng': '🎧 "The report recommends addressing vehicle emissions and industrial output first."\n✅ Answer: A, C — Only these two are specifically recommended.',
        'demo_bn': '🎧 "প্রতিবেদনটি প্রথমে যানবাহনের নিঃসরণ এবং শিল্প উৎপাদন মোকাবেলার সুপারিশ করে।"\n✅ উত্তর: A, C',
        'tips': ['কতগুলো উত্তর নির্বাচন করতে হবে সেটি প্রশ্নে দেওয়া থাকে', 'উল্লেখ করা ≠ সুপারিশ করা — শুধু confirmed/recommended items বাছো']
    },

    'Matching': {
        'rule_eng': 'Match items from two lists based on what you hear. Listen for the connection between items — which technique matches which benefit, which person matches which opinion. The answers follow the ORDER of the audio.',
        'rule_bn': 'যা শোনো তার ভিত্তিতে দুটি তালিকার items মেলাও। Items-এর মধ্যে সংযোগ শোনো — কোন কৌশল কোন সুবিধার সাথে মেলে।',
        'demo_eng': '🎧 "Using visual aids improves information retention."\n✅ Visual aids → Information retention',
        'demo_bn': '🎧 "ভিজ্যুয়াল এইড ব্যবহার তথ্য মনে রাখার ক্ষমতা বাড়ায়।"\n✅ ভিজ্যুয়াল এইড → তথ্য ধারণ',
        'tips': ['অডিওর ক্রম অনুসরণ করো', 'Synonym শোনো — exact word match নাও হতে পারে']
    },

    'Plan Labelling': {
        'rule_eng': 'Similar to Map Labelling but for building floor plans. Listen for room names, directions, and spatial relationships. Key words: "on the left", "at the end", "next to", "between", "ground/first/second floor".',
        'rule_bn': 'Map Labelling-এর মতো কিন্তু building-এর floor plan-এর জন্য। ঘরের নাম, দিকনির্দেশনা এবং স্থানিক সম্পর্ক শোনো।',
        'demo_eng': '🎧 "Go up the stairs and turn right — you\'ll find the Modern Art collection."\n✅ Modern Art = First floor, right from stairs',
        'demo_bn': '🎧 "সিঁড়ি দিয়ে ওপরে যাও এবং ডানে ঘোরো — Modern Art collection পাবে।"\n✅ Modern Art = প্রথম তলা, সিঁড়ি থেকে ডানে',
        'tips': ['Floor plan-এ entrance চিহ্নিত করো আগে', '"upstairs"/"downstairs" শুনলে তলা পরিবর্তন বুঝবে']
    },

    'Diagram Labelling': {
        'rule_eng': 'Label parts of a diagram (machine, process, biological structure) using words from the audio. The description usually follows the visual order (left to right, top to bottom, or step-by-step in a process).',
        'rule_bn': 'অডিও থেকে শব্দ দিয়ে diagram-এর অংশগুলো label করো (যন্ত্র, প্রক্রিয়া, জৈবিক গঠন)। বর্ণনা সাধারণত visual ক্রম অনুসরণ করে।',
        'demo_eng': '🎧 "The waste passes through a magnetic separator that extracts metals."\n✅ Magnetic separator → extracts metals',
        'demo_bn': '🎧 "বর্জ্য একটি চৌম্বকীয় বিভাজকের মধ্য দিয়ে যায় যা ধাতু আলাদা করে।"\n✅ চৌম্বকীয় বিভাজক → ধাতু আলাদা করে',
        'tips': ['Diagram-এ label number/arrow অনুসরণ করো', 'Process-এর ক্রম অডিওর ক্রমের সাথে মেলে']
    },

    'Table Completion': {
        'rule_eng': 'Complete a table by listening for specific data points. Read the column and row headers BEFORE listening. This tells you what type of information to listen for in each cell.',
        'rule_bn': 'নির্দিষ্ট তথ্য শুনে table পূরণ করো। শোনার আগে column ও row header পড়ো। এটা বলে দেবে প্রতিটি cell-এ কী ধরনের তথ্য শুনতে হবে।',
        'demo_eng': '🎧 "Professor Chen\'s session on machine learning starts at 2 PM in the Main Hall."\n✅ Venue for ML session: Main Hall',
        'demo_bn': '🎧 "অধ্যাপক চেনের মেশিন লার্নিং সেশন বিকাল ২টায় Main Hall-এ শুরু হবে।"\n✅ ML সেশনের ভেন্যু: Main Hall',
        'tips': ['Header থেকে predict করো কী তথ্য আসবে', 'সংখ্যা, সময়, স্থানের নাম — এগুলো সাধারণত table-এর উত্তর']
    },

    'Flow-chart Completion': {
        'rule_eng': 'Complete a flow-chart showing a sequence of steps. Listen for sequencing language: "first", "then", "after that", "next", "following this", "finally". The flow-chart mirrors the order of the audio.',
        'rule_bn': 'ধাপের ক্রম দেখানো flow-chart পূরণ করো। Sequencing ভাষা শোনো: "প্রথমে", "তারপর", "এরপর", "পরবর্তীতে", "শেষে"।',
        'demo_eng': '🎧 "First identify your research question. Then conduct a literature review. After that, design your methodology."\n✅ After literature review → methodology design',
        'demo_bn': '🎧 "প্রথমে গবেষণা প্রশ্ন চিহ্নিত করো। তারপর সাহিত্য পর্যালোচনা করো। এরপর পদ্ধতি নকশা করো।"\n✅ সাহিত্য পর্যালোচনার পর → পদ্ধতি নকশা',
        'tips': ['"then", "after that", "next" — এই শব্দগুলো ক্রম বুঝতে সাহায্য করে', 'Flow-chart-এর তীরচিহ্ন অনুসরণ করো']
    },

    'Summary Completion': {
        'rule_eng': 'Listen and complete a summary with key words. The summary paraphrases the audio. You may choose from a word list or write words from the audio. Focus on KEY CONTENT WORDS (nouns, adjectives).',
        'rule_bn': 'শুনে মূল শব্দ দিয়ে summary পূরণ করো। Summary অডিওর paraphrase করে। Word list থেকে বাছতে হতে পারে বা অডিও থেকে লিখতে হতে পারে।',
        'demo_eng': '🎧 "They feed almost exclusively on tiny creatures called krill."\n✅ Blue whales mainly eat: krill',
        'demo_bn': '🎧 "তারা প্রায় সম্পূর্ণভাবে ক্রিল নামক ক্ষুদ্র প্রাণীদের খায়।"\n✅ নীল তিমি প্রধানত খায়: ক্রিল',
        'tips': ['Summary-র gap-এর আগে-পরের শব্দ দিয়ে predict করো', 'Content words (noun/adjective) সাধারণত উত্তর হয়']
    },

    'Sentence Completion': {
        'rule_eng': 'Complete sentences using words from the audio. The sentence paraphrases what was said. Focus on the EXACT words from the audio that complete the meaning. Respect the word limit.',
        'rule_bn': 'অডিও থেকে শব্দ দিয়ে বাক্য পূরণ করো। বাক্যটি যা বলা হয়েছে তার paraphrase করে। অর্থ সম্পূর্ণ করে এমন অডিওর হুবহু শব্দে ফোকাস করো।',
        'demo_eng': '🎧 "The most basic are physiological needs such as food and water."\n✅ The most fundamental needs are _____ needs. → physiological',
        'demo_bn': '🎧 "সবচেয়ে মৌলিক হলো শারীরবৃত্তীয় চাহিদা যেমন খাদ্য ও পানি।"\n✅ সবচেয়ে মৌলিক চাহিদাগুলো হলো _____ চাহিদা। → physiological (শারীরবৃত্তীয়)',
        'tips': ['"most basic" → "most fundamental" — paraphrase চেনো', 'Grammar check: gap-এ adjective/noun কী লাগবে?']
    },

    'Short-answer Questions': {
        'rule_eng': 'Answer questions with SHORT answers (1-3 words) using words from the audio. Read the question BEFORE listening to know what to listen for. WH-questions tell you the answer type (when=time, where=place, how many=number).',
        'rule_bn': 'অডিও থেকে শব্দ দিয়ে সংক্ষেপে (১-৩ শব্দ) উত্তর দাও। কী শুনতে হবে জানতে শোনার আগে প্রশ্ন পড়ো।',
        'demo_eng': '❓ "How long has the patient had a headache?" 🎧 "for the past three days"\n✅ Answer: three days',
        'demo_bn': '❓ "রোগীর কতদিন ধরে মাথাব্যথা?" 🎧 "গত তিন দিন ধরে"\n✅ উত্তর: three days (তিন দিন)',
        'tips': ['WH-word দেখো: When=সময়, Where=স্থান, How many=সংখ্যা', 'Word limit মানো']
    },

    # ──── WRITING ────
    'Line Graph (Academic Task 1)': {
        'rule_eng': 'Describe TRENDS over time. Use trend vocabulary: "increased steadily", "rose sharply", "declined gradually", "remained stable", "fluctuated", "peaked at", "reached a low of". You MUST include an OVERVIEW paragraph identifying 2-3 key overall trends BEFORE describing specific data.',
        'rule_bn': 'সময়ের সাথে TRENDS বর্ণনা করো। Trend শব্দভাণ্ডার: "ধীরে ধীরে বৃদ্ধি পেয়েছে", "দ্রুত বেড়েছে", "ক্রমশ কমেছে", "স্থিতিশীল ছিল", "ওঠানামা করেছে"। নির্দিষ্ট তথ্যের আগে ২-৩টি মূল trend চিহ্নিত করে একটি OVERVIEW অনুচ্ছেদ অবশ্যই দিতে হবে।',
        'demo_eng': '✍️ "Overall, coal consumption declined steadily over the period, while renewable energy experienced significant growth, particularly after 2010." — This is a Band 7.5+ Overview.',
        'demo_bn': '✍️ "সামগ্রিকভাবে, পুরো সময়কালে কয়লার ব্যবহার ধীরে ধীরে কমেছে, যেখানে নবায়নযোগ্য শক্তি উল্লেখযোগ্য প্রবৃদ্ধি দেখিয়েছে, বিশেষ করে ২০১০-এর পর।"',
        'tips': ['Overview ছাড়া Band 7 পাওয়া প্রায় অসম্ভব', 'প্রতিটি trend-এ adverb যোগ করো: steadily, sharply, gradually', 'সংখ্যা দিয়ে data support করো কিন্তু সব সংখ্যা লেখার দরকার নেই']
    },

    'Bar Chart (Academic Task 1)': {
        'rule_eng': 'Compare categories or groups. Use comparison language: "significantly higher than", "approximately equal to", "twice as much as", "the highest/lowest figure". Group similar data together to show patterns.',
        'rule_bn': 'ক্যাটাগরি বা গ্রুপ তুলনা করো। তুলনামূলক ভাষা ব্যবহার করো: "উল্লেখযোগ্যভাবে বেশি", "প্রায় সমান", "দ্বিগুণ"।',
        'demo_eng': '✍️ "Asia had by far the highest number of internet users at 1.6 billion, which was more than double the figure for Europe."',
        'demo_bn': '✍️ "এশিয়ায় সর্বাধিক ১.৬ বিলিয়ন ইন্টারনেট ব্যবহারকারী ছিল, যা ইউরোপের দ্বিগুণেরও বেশি।"',
        'tips': ['সর্বোচ্চ ও সর্বনিম্ন আগে উল্লেখ করো', 'সাদৃশ্যপূর্ণ data একসাথে group করো', '"whereas", "while", "by contrast" — তুলনামূলক connectors ব্যবহার করো']
    },

    'Pie Chart (Academic Task 1)': {
        'rule_eng': 'Describe proportions and percentages. Use: "accounted for the largest proportion", "made up approximately a quarter", "represented a negligible share". Compare segments: "was three times larger than", "was roughly equivalent to".',
        'rule_bn': 'অনুপাত ও শতাংশ বর্ণনা করো। ব্যবহার করো: "সবচেয়ে বড় অংশ দখল করেছে", "প্রায় এক-চতুর্থাংশ ছিল"।',
        'demo_eng': '✍️ "Housing accounted for the largest proportion of expenditure at 35%, which was nearly double the share spent on food (20%)."',
        'demo_bn': '✍️ "আবাসন ব্যয়ের সবচেয়ে বড় অংশ (৩৫%) দখল করেছে, যা খাদ্যে ব্যয়ের (২০%) প্রায় দ্বিগুণ।"',
        'tips': ['শতাংশ ও ভগ্নাংশ দুভাবেই লেখার চর্চা করো (25% = a quarter)', 'ক্ষুদ্রতম অংশগুলো একসাথে group করো']
    },

    'Table (Academic Task 1)': {
        'rule_eng': 'Synthesize data from rows and columns. Identify patterns: which category has the highest/lowest values, any trends across time periods. Do NOT describe every single number — select KEY data.',
        'rule_bn': 'Row ও column থেকে তথ্য সংশ্লেষণ করো। প্যাটার্ন চিহ্নিত করো: কোন ক্যাটাগরিতে সর্বোচ্চ/সর্বনিম্ন মান, সময়কাল জুড়ে কোনো trend আছে কিনা।',
        'demo_eng': '✍️ "Engineering saw the largest increase in enrollment from 450 in 2019 to 620 in 2021, while Arts declined slightly from 380 to 350."',
        'demo_bn': '✍️ "ইঞ্জিনিয়ারিং-এ ভর্তি সবচেয়ে বেশি বৃদ্ধি পেয়েছে ২০১৯-এর ৪৫০ থেকে ২০২১-এ ৬২০, যেখানে আর্টস সামান্য কমেছে ৩৮০ থেকে ৩৫০।"',
        'tips': ['সব সংখ্যা লেখো না — key data নির্বাচন করো', 'Row-wise এবং column-wise দুভাবেই pattern দেখো']
    },

    'Process Diagram (Academic Task 1)': {
        'rule_eng': 'Describe a process step by step using PASSIVE VOICE and SEQUENCING LANGUAGE. Example: "First, raw materials are collected." → "Next, they are processed." → "Finally, the product is packaged." Identify how many stages exist and whether the process is linear or cyclical.',
        'rule_bn': 'PASSIVE VOICE ও SEQUENCING LANGUAGE ব্যবহার করে ধাপে ধাপে প্রক্রিয়া বর্ণনা করো। উদাহরণ: "প্রথমে, কাঁচামাল সংগ্রহ করা হয়।" → "এরপর, সেগুলো প্রক্রিয়াজাত করা হয়।"',
        'demo_eng': '✍️ "The cement manufacturing process consists of five main stages. First, limestone and clay are crushed into small pieces. These materials are then heated in a rotating kiln at 1400°C..."',
        'demo_bn': '✍️ "সিমেন্ট উৎপাদন প্রক্রিয়ায় পাঁচটি মূল ধাপ রয়েছে। প্রথমে, চুনাপাথর ও মাটি ছোট টুকরোতে চূর্ণ করা হয়।"',
        'tips': ['Passive voice ব্যবহার করো: "is crushed", "are heated", "is mixed"', '"First → Then → Next → After that → Finally" — sequencing language', 'কতগুলো ধাপ আছে Overview-তে বলো']
    },

    'Map (Academic Task 1)': {
        'rule_eng': 'Compare TWO maps showing changes over time. Use language of change: "was replaced by", "was converted into", "was demolished and replaced with", "was constructed/built", "has been extended". Include spatial references: "to the north of", "adjacent to", "in the southeast corner".',
        'rule_bn': 'সময়ের সাথে পরিবর্তন দেখানো দুটি মানচিত্র তুলনা করো। পরিবর্তনের ভাষা ব্যবহার করো: "প্রতিস্থাপিত হয়েছে", "রূপান্তরিত হয়েছে", "ভেঙে ফেলা হয়েছে"।',
        'demo_eng': '✍️ "By 2020, the farmland to the west of the town had been replaced by a large shopping centre, and the fishing port had been converted into a modern marina."',
        'demo_bn': '✍️ "২০২০-এর মধ্যে, শহরের পশ্চিমে কৃষিজমি একটি বড় শপিং সেন্টার দ্বারা প্রতিস্থাপিত হয়েছে এবং মাছ ধরার বন্দরটি আধুনিক মারিনায় রূপান্তরিত হয়েছে।"',
        'tips': ['Past perfect passive ব্যবহার করো: "had been replaced", "had been built"', 'দিকনির্দেশ উল্লেখ করো: north, south, east, west']
    },

    'Formal Letter (GT Task 1)': {
        'rule_eng': 'Use formal register throughout. Start with "Dear Sir/Madam" (unknown recipient) or "Dear Mr/Ms [Name]". State your purpose clearly in the first paragraph. End with "Yours faithfully" (unknown) or "Yours sincerely" (known name). NO contractions, NO informal language.',
        'rule_bn': 'সম্পূর্ণ আনুষ্ঠানিক ভাষা ব্যবহার করো। "Dear Sir/Madam" দিয়ে শুরু করো (অজানা প্রাপক)। প্রথম অনুচ্ছেদে উদ্দেশ্য পরিষ্কার বলো। "Yours faithfully" দিয়ে শেষ করো।',
        'demo_eng': '✍️ "Dear Sir/Madam,\nI am writing to formally complain about the excessive noise from construction work above my apartment (Unit 4B). The noise begins at 7 AM and continues until late evening..."',
        'demo_bn': '✍️ "Dear Sir/Madam,\nআমি আমার অ্যাপার্টমেন্টের (ইউনিট 4B) ওপরের তলায় নির্মাণ কাজের অত্যধিক শব্দ সম্পর্কে আনুষ্ঠানিকভাবে অভিযোগ করতে লিখছি..."',
        'tips': ['Contraction ব্যবহার করো না: "I am" লেখো, "I\'m" নয়', '3 bullet point cover করো: সমস্যা + প্রভাব + সমাধান', '"I would appreciate it if you could..." — formal request structure']
    },

    'Semi-formal Letter (GT Task 1)': {
        'rule_eng': 'Semi-formal is for someone you know professionally but not personally (teacher, boss, colleague). Use "Dear Professor/Mr [Name]" and "Yours sincerely". Tone: respectful but not stiff. Can use polite requests.',
        'rule_bn': 'Semi-formal হলো পেশাগতভাবে পরিচিত কিন্তু ব্যক্তিগতভাবে নয় (শিক্ষক, বস)। "Dear Professor [Name]" ব্যবহার করো। সুর: সম্মানজনক কিন্তু শক্ত নয়।',
        'demo_eng': '✍️ "Dear Professor Johnson,\nI hope this email finds you well. I was a student in your Advanced Economics class during 2022-2023, and I am writing to request a reference letter..."',
        'demo_bn': '✍️ "Dear Professor Johnson,\nআশা করি আপনি ভালো আছেন। আমি ২০২২-২০২৩ সালে আপনার Advanced Economics ক্লাসের ছাত্র ছিলাম এবং একটি রেফারেন্স লেটার অনুরোধ করতে লিখছি..."',
        'tips': ['"I hope this finds you well" — ভালো opening', 'Formal + friendly = semi-formal tone', '"Yours sincerely" দিয়ে শেষ করো (নাম জানা থাকলে)']
    },

    'Informal Letter (GT Task 1)': {
        'rule_eng': 'For friends and family. Use casual greeting: "Hi/Hey [Name]", "Dear [Name]". Contractions OK ("I\'m", "don\'t"). Conversational tone. End with "Take care", "Cheers", "See you soon". Use exclamation marks and casual expressions.',
        'rule_bn': 'বন্ধু ও পরিবারের জন্য। Casual greeting ব্যবহার করো: "Hi/Hey [Name]"। Contraction ব্যবহার করা যায়। কথোপকথনমূলক সুর। "Take care", "Cheers" দিয়ে শেষ করো।',
        'demo_eng': '✍️ "Hey Sarah!\nGuess what — I\'m planning a surprise birthday party for Tom next Saturday! It\'s going to be at the new restaurant on Baker Street..."',
        'demo_bn': '✍️ "Hey Sarah!\nজানো কী — আমি পরের শনিবার টমের জন্য একটি সারপ্রাইজ বার্থডে পার্টি প্ল্যান করছি!"',
        'tips': ['Exclamation mark ব্যবহার করো enthusiasm দেখাতে', 'Idioms ও casual phrases: "Guess what", "By the way", "Can\'t wait"', '"Take care" বা "Cheers" দিয়ে শেষ করো']
    },

    'Opinion Essay (Task 2)': {
        'rule_eng': 'State your CLEAR POSITION in the introduction thesis. Support with 2-3 body paragraphs, each with: Topic Sentence → Explanation → Example → Link back to thesis. Conclusion restates position and summarizes key arguments. Stay CONSISTENT — don\'t change your opinion mid-essay.',
        'rule_bn': 'Introduction-এ thesis-এ তোমার স্পষ্ট অবস্থান জানাও। ২-৩টি body paragraph দিয়ে support করো, প্রতিটিতে: Topic Sentence → ব্যাখ্যা → উদাহরণ → thesis-এ ফিরে আসা। Conclusion-এ অবস্থান পুনরায় বলো।',
        'demo_eng': '✍️ Thesis: "While I acknowledge the financial burden on governments, I firmly believe that free university education promotes social mobility and drives long-term economic growth."',
        'demo_bn': '✍️ Thesis: "সরকারের আর্থিক চাপ স্বীকার করেও, আমি দৃঢ়ভাবে বিশ্বাস করি যে বিনামূল্যে বিশ্ববিদ্যালয় শিক্ষা সামাজিক গতিশীলতা ও দীর্ঘমেয়াদী অর্থনৈতিক প্রবৃদ্ধি বাড়ায়।"',
        'tips': ['Thesis-এ "I firmly believe", "In my view" ব্যবহার করো', 'প্রতিটি body paragraph-এ একটিই মূল argument রাখো', 'পুরো essay জুড়ে একই অবস্থান বজায় রাখো']
    },

    'Agree / Disagree Essay (Task 2)': {
        'rule_eng': 'Similar to Opinion Essay but the prompt asks specifically "To what extent do you agree or disagree?" You can: fully agree, fully disagree, OR partially agree. Make your DEGREE of agreement clear in the thesis.',
        'rule_bn': 'Opinion Essay-এর মতো কিন্তু prompt নির্দিষ্টভাবে জিজ্ঞেস করে "তুমি কতটা একমত বা দ্বিমত?" তুমি পারো: সম্পূর্ণ একমত, সম্পূর্ণ দ্বিমত, বা আংশিক একমত হতে।',
        'demo_eng': '✍️ "I partially agree that technology has reduced face-to-face interaction; however, its benefits for global connectivity far outweigh the drawbacks."',
        'demo_bn': '✍️ "আমি আংশিকভাবে একমত যে প্রযুক্তি মুখোমুখি যোগাযোগ কমিয়েছে; তবে, বৈশ্বিক সংযোগের জন্য এর সুবিধা অসুবিধার চেয়ে অনেক বেশি।"',
        'tips': ['"To what extent" → পুরোপুরি একমত/দ্বিমত হওয়া বাধ্যতামূলক নয়', '"Partially agree" একটি শক্তিশালী নুয়ান্সড অবস্থান', 'Concession দেখাও: "While I accept that..., I nevertheless believe..."']
    },

    'Discussion Essay (Task 2)': {
        'rule_eng': 'Discuss BOTH VIEWS equally before giving YOUR opinion (usually in the conclusion). Body 1: View A + support. Body 2: View B + support. Conclusion: Your own position with justification. Balance is key.',
        'rule_bn': 'তোমার মতামত দেওয়ার আগে দুটি মতামতই সমানভাবে আলোচনা করো। Body 1: মত A + সমর্থন। Body 2: মত B + সমর্থন। Conclusion: তোমার নিজের অবস্থান।',
        'demo_eng': '✍️ Body 1: "On the one hand, working from home offers flexibility and eliminates commuting time..." Body 2: "On the other hand, remote work can lead to social isolation..."',
        'demo_bn': '✍️ Body 1: "একদিকে, বাড়ি থেকে কাজ নমনীয়তা দেয়..." Body 2: "অন্যদিকে, দূরবর্তী কাজ সামাজিক বিচ্ছিন্নতা তৈরি করতে পারে..."',
        'tips': ['"On the one hand... On the other hand..." — classic discussion structure', 'দুটি view-কে সমান গুরুত্ব দাও', 'নিজের মতামত conclusion-এ দাও']
    },

    'Advantages / Disadvantages Essay (Task 2)': {
        'rule_eng': 'If the prompt asks "Do advantages outweigh disadvantages?", you MUST give a clear answer. Body 1: Advantages with examples. Body 2: Disadvantages with examples. Conclusion: Clear judgment on which outweighs.',
        'rule_bn': '"সুবিধা কি অসুবিধার চেয়ে বেশি?" জিজ্ঞেস করলে, তোমাকে স্পষ্ট উত্তর দিতে হবে। Body 1: সুবিধা + উদাহরণ। Body 2: অসুবিধা + উদাহরণ। Conclusion: কোনটি বেশি তার স্পষ্ট রায়।',
        'demo_eng': '✍️ "In conclusion, although international tourism can cause environmental damage and cultural erosion, the economic benefits and cross-cultural understanding it generates clearly outweigh these drawbacks."',
        'demo_bn': '✍️ "উপসংহারে, যদিও আন্তর্জাতিক পর্যটন পরিবেশগত ক্ষতি করতে পারে, এটি যে অর্থনৈতিক সুবিধা ও আন্তঃসাংস্কৃতিক বোঝাপড়া তৈরি করে তা এই অসুবিধাগুলোকে ছাড়িয়ে যায়।"',
        'tips': ['"outweigh" প্রশ্নে অবশ্যই clear judgment দাও', 'শুধু list করো না — প্রতিটি advantage/disadvantage explain করো']
    },

    'Problem / Solution Essay (Task 2)': {
        'rule_eng': 'Body 1: Identify the CAUSES/PROBLEMS with examples. Body 2: Propose SOLUTIONS with practical details. Each problem ideally has a corresponding solution. Be specific — avoid vague suggestions.',
        'rule_bn': 'Body 1: কারণ/সমস্যা চিহ্নিত করো উদাহরণসহ। Body 2: সমাধান প্রস্তাব করো ব্যবহারিক বিবরণসহ। প্রতিটি সমস্যার সাথে সংশ্লিষ্ট সমাধান থাকা ভালো।',
        'demo_eng': '✍️ "One major cause of urban traffic congestion is the increasing number of private vehicles. To address this, governments could invest heavily in affordable public transportation networks."',
        'demo_bn': '✍️ "শহুরে ট্রাফিক জ্যামের একটি প্রধান কারণ ব্যক্তিগত গাড়ির ক্রমবর্ধমান সংখ্যা। এটি মোকাবেলায়, সরকার সাশ্রয়ী গণপরিবহন নেটওয়ার্কে বিনিয়োগ করতে পারে।"',
        'tips': ['প্রতিটি cause-এর জন্য একটি solution match করো', 'Solution specific রাখো — "the government should..." বলে থেমো না']
    },

    'Two-Part Question Essay (Task 2)': {
        'rule_eng': 'The prompt contains TWO separate questions. You MUST answer BOTH. Dedicate one body paragraph to each question. Missing one question = losing marks for Task Achievement.',
        'rule_bn': 'Prompt-এ দুটি আলাদা প্রশ্ন থাকে। তোমাকে দুটিরই উত্তর দিতে হবে। প্রতিটি প্রশ্নের জন্য একটি করে body paragraph বরাদ্দ করো।',
        'demo_eng': '✍️ Q1: "Why do children spend so much time on screens?" → Body 1\nQ2: "Is this a positive or negative development?" → Body 2',
        'demo_bn': '✍️ Q1: "শিশুরা কেন এত বেশি সময় স্ক্রিনে কাটায়?" → Body 1\nQ2: "এটি কি ইতিবাচক না নেতিবাচক?" → Body 2',
        'tips': ['দুটি প্রশ্নই underline করো', 'প্রতিটি প্রশ্নের জন্য আলাদা body paragraph লেখো', 'একটি প্রশ্ন miss করলে Task Achievement marks কমে যাবে']
    },

    # ──── SPEAKING ────
    'Part 1 Personal Questions': {
        'rule_eng': 'Part 1 is about FAMILIAR TOPICS (home, work, study, hobbies). Answers should be 2-3 sentences — NOT too short, NOT too long. Use the A-R-E-E formula: Answer → Reason → Example → Extra detail. Speak naturally, don\'t sound rehearsed.',
        'rule_bn': 'Part 1 হলো পরিচিত বিষয়ে (বাড়ি, কাজ, পড়াশোনা, শখ)। উত্তর ২-৩ বাক্যের হওয়া উচিত — খুব সংক্ষিপ্ত বা দীর্ঘ নয়। A-R-E-E সূত্র ব্যবহার করো: উত্তর → কারণ → উদাহরণ → অতিরিক্ত তথ্য।',
        'demo_eng': '❓ "What do you like about your hometown?"\n✅ "I particularly enjoy the riverside area (Answer) because it\'s incredibly peaceful (Reason). For instance, every weekend I take a walk along the banks (Example). It really helps me unwind after a busy week (Extra)."',
        'demo_bn': '❓ "তোমার শহরের কী ভালো লাগে?"\n✅ "আমার বিশেষভাবে নদীর ধার ভালো লাগে (উত্তর) কারণ এটা অবিশ্বাস্য শান্তিপূর্ণ (কারণ)। যেমন, প্রতি সপ্তাহান্তে আমি নদীর পাড়ে হাঁটতে যাই (উদাহরণ)।"',
        'tips': ['A-R-E-E: Answer → Reason → Example → Extra', 'শুধু "Yes" বা "No" বলো না — extend করো', 'মুখস্থ শোনালে marks কমবে — natural থাকো']
    },

    'Part 2 Cue Card': {
        'rule_eng': 'You get 1 minute to prepare and must speak for 1-2 MINUTES continuously. Use the preparation time to write brief notes for EACH bullet point on the card. Structure: Introduction (who/what/when) → Details → Experience/Story → Feeling/Impact. Practice the 2-minute monologue technique.',
        'rule_bn': 'তোমার ১ মিনিট প্রস্তুতি আছে এবং ১-২ মিনিট একটানা কথা বলতে হবে। প্রস্তুতির সময় কার্ডের প্রতিটি bullet point-এর জন্য সংক্ষিপ্ত নোট লেখো। গঠন: ভূমিকা → বিবরণ → অভিজ্ঞতা/গল্প → অনুভূতি/প্রভাব।',
        'demo_eng': '🎤 Cue Card: "Describe a teacher who influenced you."\n\n✅ "I\'d like to talk about my high school physics teacher, Mr. Rahman. (WHO) He taught us for three years. (DETAILS) What made him special was his ability to explain complex concepts using everyday examples... (EXPERIENCE) To this day, his passion for teaching inspires me to keep learning. (FEELING)"',
        'demo_bn': '🎤 Cue Card: "তোমাকে প্রভাবিত করেছেন এমন একজন শিক্ষক বর্ণনা করো।"\n\n✅ "আমি আমার হাই স্কুলের পদার্থবিদ্যার শিক্ষক রহমান স্যারের কথা বলতে চাই। (কে) তিনি তিন বছর আমাদের পড়িয়েছেন। (বিবরণ) তাঁকে বিশেষ করে তুলেছিল দৈনন্দিন উদাহরণ দিয়ে জটিল ধারণা ব্যাখ্যা করার ক্ষমতা... (অভিজ্ঞতা)"',
        'tips': ['প্রস্তুতির ১ মিনিটে প্রতিটি bullet-এর জন্য ২-৩ শব্দ নোট করো', '2 মিনিটের আগে থামলে marks কমবে — সময় পূরণ করো', 'গল্প বলার মতো করে বলো — list পড়ার মতো নয়']
    },

    'Part 3 Opinion & Discussion': {
        'rule_eng': 'Part 3 requires ABSTRACT, ANALYTICAL responses about society-level topics. Extend answers to 4-6 sentences. Use hedging: "I\'d argue that...", "It depends on...", "While some may think...". Give examples from general knowledge. Show ability to discuss ideas, not just personal experience.',
        'rule_bn': 'Part 3-এ সমাজ-স্তরের বিষয়ে বিমূর্ত, বিশ্লেষণমূলক উত্তর দিতে হয়। ৪-৬ বাক্যে উত্তর extend করো। Hedging ব্যবহার করো: "আমি মনে করি...", "এটা নির্ভর করে...", "কেউ কেউ ভাবতে পারে..."।',
        'demo_eng': '❓ "Do you think education is better today?"\n✅ "That\'s an interesting question. I\'d say that in many ways education has improved, particularly in terms of access and technology. However, I think we\'ve lost something in terms of personal mentorship. For instance, online learning provides flexibility but can lack the depth of face-to-face interaction."',
        'demo_bn': '❓ "তুমি কি মনে করো আজকের শিক্ষা ভালো?"\n✅ "এটা একটা চিন্তার বিষয়। আমি বলব অনেক দিক থেকে শিক্ষার উন্নতি হয়েছে, বিশেষত প্রবেশাধিকার ও প্রযুক্তির ক্ষেত্রে। তবে, আমি মনে করি ব্যক্তিগত পরামর্শের দিকটা কমে গেছে।"',
        'tips': ['"I\'d argue", "It seems to me", "On balance" — advanced hedging phrases', 'ব্যক্তিগত অভিজ্ঞতা + সাধারণ জ্ঞান দুটোই ব্যবহার করো', 'Both sides দেখানোর চেষ্টা করো — nuanced thinking marks বাড়ায়']
    },

    'Part 3 Comparison': {
        'rule_eng': 'Compare past and present, or different perspectives. Use comparison structures: "Whereas... used to..., nowadays...", "Unlike in the past...", "One of the biggest changes is that...", "Compared to [X], [Y] is...". Show ability to analyze CHANGE over time.',
        'rule_bn': 'অতীত ও বর্তমান, বা ভিন্ন দৃষ্টিভঙ্গি তুলনা করো। তুলনামূলক structure ব্যবহার করো: "যেখানে আগে... হতো, এখন...", "অতীতের মতো নয়..."। সময়ের সাথে পরিবর্তন বিশ্লেষণ করার ক্ষমতা দেখাও।',
        'demo_eng': '❓ "How has city living changed compared to 50 years ago?"\n✅ "Whereas cities used to be relatively compact and community-oriented, nowadays they tend to be sprawling and more individualistic. Unlike in the past, people today often don\'t even know their neighbours."',
        'demo_bn': '❓ "৫০ বছর আগের তুলনায় শহুরে জীবন কীভাবে পরিবর্তিত হয়েছে?"\n✅ "যেখানে শহরগুলো আগে তুলনামূলক ছোট ও সম্প্রদায়-কেন্দ্রিক ছিল, এখন সেগুলো ছড়িয়ে পড়া ও ব্যক্তিকেন্দ্রিক।"',
        'tips': ['"used to vs now", "whereas/while", "compared to/in contrast with"', '"One of the biggest changes is..." — excellent opening', 'অতীত + বর্তমান + তোমার মূল্যায়ন — এই ৩ অংশে সাজাও']
    },

    'Part 3 Prediction': {
        'rule_eng': 'Speculate about the FUTURE. Use future speculation language: "I think it\'s likely that...", "There\'s a good chance that...", "I wouldn\'t be surprised if...", "In all probability...", "It\'s hard to predict, but...". Avoid simple "will" — use modal verbs for higher bands.',
        'rule_bn': 'ভবিষ্যৎ সম্পর্কে অনুমান করো। ভবিষ্যৎ অনুমানের ভাষা ব্যবহার করো: "আমি মনে করি সম্ভবত...", "ভালো সম্ভাবনা আছে যে...", "আমি অবাক হব না যদি..."। সহজ "will" এড়াও — উচ্চতর band-এর জন্য modal verb ব্যবহার করো।',
        'demo_eng': '❓ "How will jobs change in the next 20 years?"\n✅ "I think it\'s highly likely that AI and automation will transform many industries. There\'s a good chance that repetitive jobs will be replaced, but I believe new roles in technology and creative fields will emerge."',
        'demo_bn': '❓ "আগামী ২০ বছরে চাকরি কীভাবে বদলাবে?"\n✅ "আমি মনে করি অত্যন্ত সম্ভব যে AI ও অটোমেশন অনেক শিল্পকে রূপান্তরিত করবে। ভালো সম্ভাবনা আছে যে পুনরাবৃত্তিমূলক কাজ প্রতিস্থাপিত হবে, তবে প্রযুক্তি ও সৃজনশীল ক্ষেত্রে নতুন ভূমিকা তৈরি হবে।"',
        'tips': ['"likely", "probably", "might", "could" — modal verbs ব্যবহার করো', 'শুধু "will" বললে Band 6 — "is likely to", "may well" বললে Band 7+', 'Positive + negative দুটো possibility দেখাও']
    }
}


class AICourseMasterEngine:
    """Master AI Human Teacher Engine with Complete IELTS Taxonomy."""

    @classmethod
    def get_taxonomy_tree(cls) -> Dict[str, Any]:
        """Return the complete IELTS taxonomy for frontend rendering."""
        return MASTER_TAXONOMY

    @staticmethod
    def process_teacher_lesson(
        topic_key: str = "True / False / Not Given",
        sub_tag: Optional[str] = None,
        user_answer: Optional[str] = None,
        lang_pref: str = "English + Mother Language",
        user_id: int = 1
    ) -> Dict[str, Any]:
        """Generate interactive Socratic human teacher lesson cards with DB-backed questions."""

        # 1. Get lesson content (static rich data)
        lesson = LESSON_CONTENT.get(topic_key)
        if not lesson:
            # Try partial match
            for key in LESSON_CONTENT:
                if topic_key.lower() in key.lower() or key.lower() in topic_key.lower():
                    lesson = LESSON_CONTENT[key]
                    break
        if not lesson:
            lesson = LESSON_CONTENT['True / False / Not Given']

        # 2. Query database for matching question
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM questions WHERE question_type = ? ORDER BY RANDOM() LIMIT 1",
            (topic_key,)
        )
        q_row = cursor.fetchone()

        if not q_row:
            cursor.execute(
                "SELECT * FROM questions WHERE question_type LIKE ? ORDER BY RANDOM() LIMIT 1",
                (f"%{topic_key}%",)
            )
            q_row = cursor.fetchone()
        conn.close()

        if q_row:
            q_data = dict(q_row)
            skill = q_data["skill"]
            test_type = q_data.get("test_type", "Academic")
            title = f"{skill} ({test_type}): {q_data['title']}"
            q_text = q_data["question_text"]
            opts = json.loads(q_data["options_json"]) if q_data.get("options_json") else []
            corr_ans = q_data["answer_key"]
            explanation = q_data.get("explanation", "")
            tag = q_data.get("sub_type_tag") or sub_tag or "IELTS Strategy"
            passage = q_data.get("passage_or_context", "")
        else:
            skill = "Reading"
            test_type = "Academic"
            title = f"IELTS {topic_key} Strategy Lesson"
            q_text = f"Apply the {topic_key} strategy to answer this question."
            opts = ["Option A: Band 7.5 Strategy", "Option B: Detail Trap"]
            corr_ans = "Option A: Band 7.5 Strategy"
            explanation = "Focus on the main concept rather than getting trapped by specific details."
            tag = sub_tag or "Strategy"
            passage = ""

        # 3. Handle EVALUATION (user submitted an answer)
        if user_answer:
            user_lower = user_answer.strip().lower()
            correct_lower = corr_ans.strip().lower()

            is_correct = (
                user_lower == correct_lower or
                correct_lower in user_lower or
                user_lower in correct_lower or
                (len(correct_lower) <= 3 and correct_lower == user_lower[:len(correct_lower)])
            )

            if is_correct:
                eng_eval = f"🎉 <strong>Excellent!</strong> You selected '<em>{user_answer}</em>' — that is correct!\n\n<strong>Why this is right:</strong> {explanation}\n\n<strong>Sub-Skill Mastered:</strong> {tag} ✅\n\nYou're demonstrating Band 7.5+ accuracy. Keep it up!"
                bn_eval = f"🎉 <strong>চমৎকার!</strong> তুমি '<em>{user_answer}</em>' নির্বাচন করেছ — সঠিক!\n\n<strong>কেন এটি সঠিক:</strong> {explanation}\n\n<strong>সাব-স্কিল আয়ত্ত:</strong> {tag} ✅\n\nতুমি ব্যান্ড ৭.৫+ নির্ভুলতা দেখাচ্ছ!"
            else:
                eng_eval = f"💡 <strong>Let's analyze:</strong> You selected '<em>{user_answer}</em>', but the correct answer is '<strong>{corr_ans}</strong>'.\n\n<strong>Explanation:</strong> {explanation}\n\n<strong>Common Trap:</strong> Many students fall for this because they match single words instead of understanding the overall meaning. Focus on the Sub-Skill: <strong>{tag}</strong>.\n\n<strong>Strategy Tip:</strong> {lesson['tips'][0] if lesson.get('tips') else 'Re-read the passage carefully.'}"
                bn_eval = f"💡 <strong>বিশ্লেষণ করি:</strong> তুমি '<em>{user_answer}</em>' নির্বাচন করেছ, কিন্তু সঠিক উত্তর হলো '<strong>{corr_ans}</strong>'।\n\n<strong>ব্যাখ্যা:</strong> {explanation}\n\n<strong>সাধারণ ফাঁদ:</strong> অনেক ছাত্র এই ভুল করে কারণ তারা সামগ্রিক অর্থ না বুঝে একটি শব্দ মেলায়। সাব-স্কিল: <strong>{tag}</strong>-এ ফোকাস করো।"

            speech_text = eng_eval.replace('<strong>', '').replace('</strong>', '').replace('<em>', '').replace('</em>', '').replace('\n', ' ')
            bengali_speech = bn_eval.replace('<strong>', '').replace('</strong>', '').replace('<em>', '').replace('</em>', '').replace('\n', ' ')

            return {
                "type": "evaluation",
                "is_correct": is_correct,
                "eng_eval": eng_eval,
                "bn_eval": bn_eval,
                "correct_answer": corr_ans,
                "explanation": explanation,
                "speech_text": speech_text,
                "bengali_speech_text": bengali_speech,
                "lang_pref": lang_pref
            }

        # 4. Return LESSON data (Step 1-3)
        tips = lesson.get('tips', [])

        # Build speech based on language preference
        if lang_pref == "English Only":
            speech = f"Welcome to the lesson on {topic_key}. {lesson['rule_eng']}"
            bn_speech = ""
        elif lang_pref == "Mother Language Only":
            speech = lesson['rule_bn']
            bn_speech = lesson['rule_bn']
        else:
            speech = f"Welcome to {topic_key}. {lesson['rule_eng']}"
            bn_speech = lesson['rule_bn']

        # Include passage context in question text if available
        full_question_text = q_text
        if passage:
            full_question_text = f"📄 Context: {passage}\n\n❓ {q_text}"

        return {
            "type": "lesson",
            "skill": skill,
            "test_type": test_type,
            "title": title,
            "sub_type_tag": tag,
            "step1_eng": lesson['rule_eng'],
            "step1_bn": lesson['rule_bn'],
            "step2_eng": lesson['demo_eng'],
            "step2_bn": lesson['demo_bn'],
            "tips": tips,
            "question": {
                "text": full_question_text,
                "options": opts,
                "correct_option": corr_ans
            },
            "speech_text": speech,
            "bengali_speech_text": bn_speech,
            "lang_pref": lang_pref
        }
