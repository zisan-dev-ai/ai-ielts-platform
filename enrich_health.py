# -*- coding: utf-8 -*-
"""
Exhaustive Band 8.0-9.0 Academic Lexicon for 'health'
Updates health.json with authentic synonyms and antonyms.
"""
import json
import os

PLATFORM_DIR = os.path.dirname(os.path.abspath(__file__))
HEALTH_FILE = os.path.join(PLATFORM_DIR, "ai_engine", "vocab_db", "health.json")

HEALTH_LEXICON = {
    "Sedentary lifestyle": {
        "synonyms": ["inactive physical routine", "physically idle habit", "prolonged sitting pattern"],
        "antonyms": ["active lifestyle", "physically vigorous regimen"]
    },
    "Preventative healthcare": {
        "synonyms": ["prophylactic medical care", "disease prevention strategy", "early health intervention"],
        "antonyms": ["reactive medical treatment", "curative acute care"]
    },
    "Mental health stigma": {
        "synonyms": ["psychological shame", "prejudice against psychiatric illness", "taboo surrounding mental distress"],
        "antonyms": ["mental health acceptance", "psychological open-mindedness"]
    },
    "Nutritional deficiency": {
        "synonyms": ["dietary insufficiency", "micronutrient malnourishment", "vitamin deficit"],
        "antonyms": ["nutritional adequacy", "dietary abundance"]
    },
    "Cardiovascular disease": {
        "synonyms": ["heart and circulatory disorder", "cardiac pathology", "arterial illness"],
        "antonyms": ["cardiovascular fitness", "arterial vitality"]
    },
    "Chronic illness management": {
        "synonyms": ["long-term condition care", "persistent disease oversight", "chronic pathology control"],
        "antonyms": ["acute illness eradication", "disease resolution"]
    },
    "Universal healthcare access": {
        "synonyms": ["comprehensive medical coverage", "equitable clinical provision", "nationwide healthcare entitlement"],
        "antonyms": ["privatized healthcare exclusion", "stratified medical availability"]
    },
    "Antibiotic resistance crisis": {
        "synonyms": ["antimicrobial immunity threat", "superbug proliferation hazard", "bacterial drug recalcitrance"],
        "antonyms": ["antibiotic susceptibility", "antimicrobial efficacy"]
    },
    "Subsidized pharmaceutical drug": {
        "synonyms": ["state-funded medication", "price-controlled prescription therapy", "rebated therapeutic drug"],
        "antonyms": ["full-market price medication", "unsubsidized proprietary drug"]
    },
    "Obesity epidemic": {
        "synonyms": ["severe adiposity crisis", "widespread corpulence surge", "metabolic weight emergency"],
        "antonyms": ["optimal body composition", "population metabolic fitness"]
    },
    "Life expectancy projection": {
        "synonyms": ["projected longevity estimate", "survival horizon forecast", "actuarial life expectancy"],
        "antonyms": ["premature mortality rate", "contracted life expectancy"]
    },
    "Public health initiative": {
        "synonyms": ["community wellness campaign", "statutory health program", "epidemiological prevention drive"],
        "antonyms": ["health deregulation", "commercial neglect of health"]
    },
    "Dietary supplement reliance": {
        "synonyms": ["micronutrient pill dependency", "synthetic vitamin dependence", "exogenous nutrient reliance"],
        "antonyms": ["whole-food nutritional sufficiency", "natural dietary nourishment"]
    },
    "Holistic therapeutic approach": {
        "synonyms": ["integrative wellness methodology", "comprehensive whole-person care", "multidimensional health strategy"],
        "antonyms": ["reductionist symptom treatment", "fragmented clinical care"]
    },
    "Palliative hospice care": {
        "synonyms": ["end-of-life comfort care", "terminal compassionate management", "hospice pain alleviation"],
        "antonyms": ["aggressive curative intervention", "invasive life prolongation"]
    },
    "Processed food consumption": {
        "synonyms": ["ultra-processed dietary intake", "industrialized food ingestion", "refined food intake"],
        "antonyms": ["whole-food nutrition", "unprocessed organic diet"]
    },
    "Immunization coverage rate": {
        "synonyms": ["vaccination uptake percentage", "herd immunity inoculation proportion", "vaccine compliance level"],
        "antonyms": ["vaccine hesitancy proportion", "unvaccinated population ratio"]
    },
    "Psychological resilience": {
        "synonyms": ["mental fortitude", "emotional bounce-back capability", "psychic endurance"],
        "antonyms": ["emotional vulnerability", "psychological fragility"]
    },
    "Substance abuse rehabilitation": {
        "synonyms": ["chemical addiction treatment", "dependency recovery therapy", "substance detox program"],
        "antonyms": ["unmanaged chronic addiction", "relapse into substance abuse"]
    },
    "Epidemiological surveillance": {
        "synonyms": ["pathogen tracking", "disease outbreak monitoring", "infectious disease vigilance"],
        "antonyms": ["epidemiological blind spot", "unmonitored disease transmission"]
    },
    "Metabolic syndrome disorder": {
        "synonyms": ["insulin resistance constellation", "cardiometabolic cluster", "metabolic dysfunction"],
        "antonyms": ["metabolic homeostasis", "optimal endocrine health"]
    },
    "Organ transplantation list": {
        "synonyms": ["donor tissue recipient registry", "transplant waiting roster", "graft allocation queue"],
        "antonyms": ["organ donation refusal", "transplant ineligibility"]
    },
    "Maternal and infant mortality": {
        "synonyms": ["perinatal maternal fatality", "childbirth maternal and neonatal death", "obstetric casualty rates"],
        "antonyms": ["safe maternal delivery", "neonatal vitality and survival"]
    },
    "Genetic predisposition": {
        "synonyms": ["hereditary susceptibility", "innate biological propensity", "inherited genetic risk"],
        "antonyms": ["genetic resistance", "environmental health immunity"]
    },
    "Alternative medicine modality": {
        "synonyms": ["complementary therapeutic practice", "unconventional healing paradigm", "nontraditional remedy"],
        "antonyms": ["orthodox allopathic medicine", "evidence-based clinical intervention"]
    },
    "Healthcare infrastructure deficit": {
        "synonyms": ["clinical resource inadequacy", "medical facility shortage", "hospital systemic shortfall"],
        "antonyms": ["robust clinical capacity", "comprehensive hospital readiness"]
    },
    "Sleep deprivation consequence": {
        "synonyms": ["chronic insomnia fallout", "sleep deficit impairment", "nocturnal restlessness penalty"],
        "antonyms": ["rejuvenating restorative sleep", "optimal circadian rest"]
    },
    "Communicable disease outbreak": {
        "synonyms": ["contagious pathogen emergence", "infectious disease flare-up", "epidemic contagion surge"],
        "antonyms": ["disease eradication", "pathogen suppression"]
    },
    "Sedentary desk job": {
        "synonyms": ["desk-bound clerical role", "physically inactive office position", "seated workstation occupation"],
        "antonyms": ["physically demanding manual labor", "active outdoor vocation"]
    },
    "Organic produce diet": {
        "synonyms": ["chemical-free whole-food regimen", "pesticide-free food intake", "naturally cultivated produce nutrition"],
        "antonyms": ["pesticide-treated food diet", "synthetic processed nutrition"]
    },
    "Hypertension management": {
        "synonyms": ["blood pressure regulation", "arterial tension control", "antihypertensive therapy"],
        "antonyms": ["uncontrolled high blood pressure", "hypertensive crisis neglect"]
    },
    "Clinical trial phase": {
        "synonyms": ["therapeutic experimental evaluation", "biomedical study stage", "drug safety efficacy trial"],
        "antonyms": ["untested pharmaceutical distribution", "unverified clinical application"]
    },
    "Burnout exhaustion symptom": {
        "synonyms": ["severe occupational fatigue", "chronic workplace enervation", "adrenal stress collapse"],
        "antonyms": ["vocational vigor", "professional rejuvenation"]
    },
    "Nutritional value enhancement": {
        "synonyms": ["dietary fortification", "nutrient density boost", "bioavailability optimization"],
        "antonyms": ["nutrient depletion", "dietary degradation"]
    },
    "Public sanitation standard": {
        "synonyms": ["municipal hygiene benchmark", "public waste control norms", "civic cleanliness protocol"],
        "antonyms": ["unsanitary squalor", "public hygiene deterioration"]
    },
    "Primary healthcare clinic": {
        "synonyms": ["first-line outpatient medical center", "general practice surgery", "community triage clinic"],
        "antonyms": ["quaternary specialized hospital", "emergency tertiary center"]
    },
    "Ergonomic workstation setup": {
        "synonyms": ["biomechanically optimized desk", "posture-aligned workspace", "musculoskeletal-friendly office setup"],
        "antonyms": ["malaligned awkward desk arrangement", "posturally hazardous workspace"]
    },
    "Cardiorespiratory endurance": {
        "synonyms": ["aerobic stamina", "cardiovascular fitness capacity", "pulmonary endurance"],
        "antonyms": ["cardiorespiratory sluggishness", "aerobic exhaustion"]
    },
    "Hospital bed capacity": {
        "synonyms": ["inpatient accommodation volume", "clinical ward bed quota", "acute care occupancy capacity"],
        "antonyms": ["hospital overcrowding", "ward bed deficit"]
    },
    "Nutritional awareness curriculum": {
        "synonyms": ["dietary literacy education", "healthy nutrition schooling", "food wellness education"],
        "antonyms": ["nutritional misinformation", "dietary ignorance"]
    },
    "Pharmaceutical patent monopoly": {
        "synonyms": ["drug manufacturer patent exclusivity", "proprietary medicine monopoly", "pharmaceutical exclusive licensing"],
        "antonyms": ["open-access generic production", "generic medication competition"]
    },
    "Diagnostic medical imaging": {
        "synonyms": ["radiological examination", "clinical scanning radiography", "diagnostic sonography and tomography"],
        "antonyms": ["exploratory invasive surgery", "blind clinical guesswork"]
    },
    "Mental well-being counselor": {
        "synonyms": ["psychological therapist", "licensed psychotherapist", "clinical mental health adviser"],
        "antonyms": ["untrained confidant", "skeptical layman"]
    },
    "Childhood immunization program": {
        "synonyms": ["pediatric vaccination schedule", "youth inoculation drive", "childhood disease protection regimen"],
        "antonyms": ["pediatric vaccine refusal", "childhood immunization neglect"]
    },
    "Dietary fiber intake": {
        "synonyms": ["roughage consumption", "digestible plant fiber ingestion", "gastrointestinal fiber volume"],
        "antonyms": ["fiber-deficient refined diet", "low-roughage processed intake"]
    },
    "Health insurance premium": {
        "synonyms": ["medical policy contribution", "healthcare coverage fee", "clinical indemnity cost"],
        "antonyms": ["uninsured out-of-pocket expenditure", "state-funded cost-free coverage"]
    },
    "Musculoskeletal injury prevention": {
        "synonyms": ["orthopedic harm mitigation", "skeletal-muscular protection", "biomechanical strain prevention"],
        "antonyms": ["repetitive strain injury negligence", "musculoskeletal trauma"]
    },
    "Preventative medical screening": {
        "synonyms": ["early diagnostic checkup", "proactive health examination", "asymptomatic clinical evaluation"],
        "antonyms": ["late-stage symptomatic diagnosis", "delayed pathology detection"]
    },
    "Medical malpractice lawsuit": {
        "synonyms": ["clinical negligence litigation", "physician tort claim", "medical error lawsuit"],
        "antonyms": ["exemplary medical standard of care", "physician exoneration"]
    },
    "Physical inactivity hazard": {
        "synonyms": ["sedentary health peril", "exercise deficiency danger", "immobility morbidity risk"],
        "antonyms": ["regular athletic vitality", "daily exercise benefit"]
    },
    "Emergency medical technician": {
        "synonyms": ["paramedic responder", "urgent care clinician", "pre-hospital trauma responder"],
        "antonyms": ["untrained bystander", "hospitalized specialist physician"]
    },
    "Life-saving surgical procedure": {
        "synonyms": ["critical operative intervention", "vital surgical excision", "acute emergency operation"],
        "antonyms": ["elective cosmetic procedure", "non-urgent minor surgery"]
    },
    "Nutrient-dense whole food": {
        "synonyms": ["micronutrient-rich unprocessed food", "nourishing unrefined foodstuff", "wholesome natural produce"],
        "antonyms": ["empty-calorie processed junk food", "nutrient-poor refined food"]
    },
    "Over-the-counter medication": {
        "synonyms": ["non-prescription pharmaceutical", "unrestricted retail medicine", "direct-purchase pharmacy drug"],
        "antonyms": ["prescription-only controlled substance", "strictly regulated hospital medication"]
    },
    "Sanitary living condition": {
        "synonyms": ["hygienic domestic environment", "clean living quarters", "aseptic household surroundings"],
        "antonyms": ["squalid unhygienic tenement", "filthy living condition"]
    },
    "Cognitive decline prevention": {
        "synonyms": ["dementia mitigation", "neurocognitive protection", "cerebral acuity maintenance"],
        "antonyms": ["accelerated neurodegeneration", "uninhibited cognitive deterioration"]
    },
    "Inpatient hospital admission": {
        "synonyms": ["hospitalization entry", "clinical ward admission", "formal patient intake"],
        "antonyms": ["outpatient discharge", "ambulatory same-day consultation"]
    },
    "Post-operative recovery period": {
        "synonyms": ["surgical convalescence phase", "post-surgical healing timeline", "rehabilitation recuperation"],
        "antonyms": ["intraoperative stage", "acute surgical trauma phase"]
    },
    "Nutritional labeling regulation": {
        "synonyms": ["food packaging disclosure mandate", "dietary ingredients law", "macronutrient declaration statute"],
        "antonyms": ["misleading food packaging", "unregulated food marketing"]
    },
    "Pediatric healthcare specialist": {
        "synonyms": ["child health physician", "pediatrician clinician", "infant medical consultant"],
        "antonyms": ["geriatrician", "adult health clinician"]
    },
    "Public health quarantine": {
        "synonyms": ["epidemic isolation protocol", "sanitary cordon sanitaire", "contagion confinement order"],
        "antonyms": ["unrestricted public congregation", "quarantine lifted free movement"]
    },
    "Physical fitness regimen": {
        "synonyms": ["structured exercise routine", "conditioning program", "athletic training schedule"],
        "antonyms": ["sedentary habits", "physical lethargy"]
    },
    "Dietary cholesterol intake": {
        "synonyms": ["lipid dietary consumption", "sterol food ingestion", "arterial plaque dietary precursor"],
        "antonyms": ["cholesterol-free plant nutrition", "statin-controlled lipid profile"]
    },
    "Medical research endowment": {
        "synonyms": ["biomedical research grant", "clinical research fellowship funding", "pathology research foundation"],
        "antonyms": ["medical funding cut", "research budget austerity"]
    },
    "Health literacy deficit": {
        "synonyms": ["medical comprehension gap", "wellness ignorance", "clinical information deficiency"],
        "antonyms": ["health literacy proficiency", "comprehensive medical awareness"]
    },
    "Rehabilitative physical therapy": {
        "synonyms": ["restorative physiotherapy", "functional motor rehabilitation", "post-injury therapeutic exercise"],
        "antonyms": ["immobility muscle atrophy", "untreated physical disability"]
    },
    "Subsidized gym membership": {
        "synonyms": ["incentivized fitness subscription", "workplace-sponsored gym access", "state-supported recreation pass"],
        "antonyms": ["prohibitive fitness club tariff", "unsupported fitness expense"]
    },
    "Medical equipment sterilizer": {
        "synonyms": ["autoclave sanitizing apparatus", "surgical instrument germicide unit", "pathogen decontamination device"],
        "antonyms": ["contaminated surgical vector", "unsterilized medical tool"]
    },
    "Infectious disease transmission": {
        "synonyms": ["pathogen propagation", "contagion vector dissemination", "communicable illness spread"],
        "antonyms": ["contagion containment", "disease transmission barrier"]
    },
    "Geriatric healthcare facility": {
        "synonyms": ["elderly care sanatorium", "nursing home clinical center", "gerontology residence"],
        "antonyms": ["pediatric clinic", "youth health facility"]
    },
    "Blood glucose regulation": {
        "synonyms": ["glycemic control", "insulin homeostasis", "blood sugar moderation"],
        "antonyms": ["uncontrolled hyperglycemia", "diabetic glycemic volatility"]
    },
    "Mental healthcare coverage": {
        "synonyms": ["psychiatric insurance indemnity", "psychological benefits parity", "mental well-being coverage"],
        "antonyms": ["psychiatric insurance exclusion", "uncovered mental health therapy"]
    },
    "Medical record confidentiality": {
        "synonyms": ["patient chart privacy", "clinical data secrecy", "physician-patient privilege"],
        "antonyms": ["unauthorized health data breach", "medical privacy infringement"]
    },
    "Balanced macro-nutrient ratio": {
        "synonyms": ["optimal dietary macro distribution", "harmonious protein-fat-carbohydrate balance", "equitable macronutrient intake"],
        "antonyms": ["macronutrient imbalance", "malnourished dietary skew"]
    },
    "Community wellness center": {
        "synonyms": ["civic health hub", "neighborhood fitness facility", "municipal wellness collective"],
        "antonyms": ["commercial private health club", "isolated medical institution"]
    },
    "Palliative pain management": {
        "synonyms": ["analgesic comfort therapy", "terminal pain alleviation", "palliative symptomatic relief"],
        "antonyms": ["uncontrolled intractable agony", "withheld analgesic care"]
    },
    "Health surveillance protocol": {
        "synonyms": ["epidemiological tracking regimen", "statutory disease monitoring code", "pathology detection system"],
        "antonyms": ["neglected disease monitoring", "untracked viral outbreak"]
    },
    "Compulsory health screening": {
        "synonyms": ["mandatory medical examination", "statutory health checkup", "obligatory clinical vetting"],
        "antonyms": ["voluntary health inspection", "opt-out diagnostic check"]
    },
    "Substance abuse intervention": {
        "synonyms": ["addiction counseling confrontation", "chemical dependency mediation", "therapeutic addiction intervention"],
        "antonyms": ["addiction enabling", "passive tolerance of substance abuse"]
    },
    "Nutrient absorption capacity": {
        "synonyms": ["gastrointestinal assimilation efficiency", "digestive nutrient uptake rate", "intestinal bioavailability factor"],
        "antonyms": ["intestinal malabsorption syndrome", "impaired nutrient uptake"]
    },
    "Alleviate": {
        "synonyms": ["mitigate", "assuage", "palliate", "relieve"],
        "antonyms": ["exacerbate", "aggravate", "intensify"]
    },
    "Prescribe": {
        "synonyms": ["order therapeutically", "stipulate medically", "authorize pharmacologically"],
        "antonyms": ["proscribe", "contraindicate", "forbid"]
    },
    "Rehabilitate": {
        "synonyms": ["restore", "reform", "reintegrate", "recuperate"],
        "antonyms": ["deteriorate", "debilitate", "worsen"]
    },
    "Inoculate": {
        "synonyms": ["immunize", "vaccinate", "ingraft pathogen resistance"],
        "antonyms": ["expose to infection", "leave vulnerable to contagion"]
    },
    "Combating": {
        "synonyms": ["contending against", "counteracting", "opposing tenaciously"],
        "antonyms": ["succumbing to", "tolerating", "yielding to"]
    },
    "Sustain": {
        "synonyms": ["maintain", "nourish", "uphold", "prolong"],
        "antonyms": ["relinquish", "undermine", "terminate"]
    },
    "Manifest": {
        "synonyms": ["evince", "display symptomatically", "demonstrate", "exhibit"],
        "antonyms": ["mask", "conceal", "suppress"]
    },
    "Hamper": {
        "synonyms": ["impede", "hinder", "thwart", "obstruct"],
        "antonyms": ["facilitate", "accelerate", "promote"]
    },
    "Reinforce": {
        "synonyms": ["fortify", "bolster", "strengthen", "augment"],
        "antonyms": ["attenuate", "weaken", "enfeeble"]
    },
    "Endure": {
        "synonyms": ["withstand", "tolerate resiliently", "bear stoically"],
        "antonyms": ["collapse", "capitulate", "succumb"]
    },
    "Impart": {
        "synonyms": ["convey", "bestow", "transmit", "disclose"],
        "antonyms": ["withhold", "conceal", "suppress"]
    },
    "Plummet": {
        "synonyms": ["collapse", "drop precipitously", "nosedive", "tumble"],
        "antonyms": ["surge", "rebound", "skyrocket"]
    },
    "Diagnose": {
        "synonyms": ["identify pathologically", "discern clinically", "pinpoint condition"],
        "antonyms": ["misidentify", "overlook", "misdiagnose"]
    },
    "Undertake": {
        "synonyms": ["commence", "initiate", "embark upon", "execute"],
        "antonyms": ["abandon", "forgo", "neglect"]
    },
    "Overhaul": {
        "synonyms": ["revamp", "reconstruct comprehensively", "modernize radically"],
        "antonyms": ["preserve untouched", "leave neglected"]
    },
    "Exert": {
        "synonyms": ["apply forcefully", "wield", "exercise", "bring to bear"],
        "antonyms": ["relax", "withhold", "abstain from"]
    },
    "Demystify": {
        "synonyms": ["elucidate", "clarify", "illuminate", "deconstruct"],
        "antonyms": ["obfuscate", "cloud", "confound"]
    },
    "Inculcate": {
        "synonyms": ["instill persistently", "ingrain", "implant deeply"],
        "antonyms": ["eradicate", "uproot", "dislodge"]
    },
    "Compromise": {
        "synonyms": ["jeopardize", "undermine", "endanger", "weaken"],
        "antonyms": ["safeguard", "fortify", "preserve"]
    },
    "Spearhead": {
        "synonyms": ["lead decisively", "champion", "pioneer", "inaugurate"],
        "antonyms": ["follow passively", "hinder", "retard"]
    },
    "Enhance": {
        "synonyms": ["augment", "elevate", "optimize", "enrich"],
        "antonyms": ["diminish", "impair", "detract from"]
    },
    "Cardiovascular": {
        "synonyms": ["circulatory", "cardiac", "arteriovascular"],
        "antonyms": ["non-circulatory", "respiratory-isolated"]
    },
    "Chronic": {
        "synonyms": ["persistent", "long-standing", "incurable and recurring", "enduring"],
        "antonyms": ["acute", "transient", "fleeting"]
    },
    "Preventative": {
        "synonyms": ["prophylactic", "precautionary", "protective", "anticipatory"],
        "antonyms": ["curative", "reactive", "remedial"]
    },
    "Nutritional": {
        "synonyms": ["dietary", "nourishing", "alimentary", "nutritive"],
        "antonyms": ["unwholesome", "deleterious", "malnourishing"]
    },
    "Invaluable": {
        "synonyms": ["priceless", "indispensable", "inestimable", "crucial"],
        "antonyms": ["worthless", "redundant", "dispensable"]
    },
    "Vital": {
        "synonyms": ["essential", "imperative", "cardinal", "indispensable"],
        "antonyms": ["superfluous", "optional", "trivial"]
    },
    "Catastrophic": {
        "synonyms": ["calamitous", "fatal", "ruinous", "devastating"],
        "antonyms": ["benign", "salutary", "fortunate"]
    },
    "Palliative": {
        "synonyms": ["soothing", "pain-relieving", "assuasive", "alleviative"],
        "antonyms": ["curative", "invasive", "exacerbating"]
    },
    "Epidemic": {
        "synonyms": ["widespread", "rampant", "pestilential", "contagious"],
        "antonyms": ["sporadic", "contained", "localized"]
    },
    "Holistic": {
        "synonyms": ["comprehensive", "integrative", "all-encompassing", "whole-person"],
        "antonyms": ["atomistic", "reductionist", "fragmentary"]
    },
    "Severe": {
        "synonyms": ["acute", "grave", "critical", "grievous"],
        "antonyms": ["mild", "minor", "moderate"]
    },
    "Insurmountable": {
        "synonyms": ["invincible", "unconquerable", "impossible", "overwhelming"],
        "antonyms": ["surmountable", "tractable", "manageable"]
    },
    "Rigorous": {
        "synonyms": ["stringent", "meticulous", "exacting", "uncompromising"],
        "antonyms": ["lax", "haphazard", "careless"]
    },
    "Substandard": {
        "synonyms": ["inferior", "deficient", "inadequate", "shoddy"],
        "antonyms": ["optimal", "superior", "benchmark"]
    },
    "Congenital": {
        "synonyms": ["innate", "inborn", "hereditary", "constitutional"],
        "antonyms": ["acquired", "contracted", "developed"]
    },
    "Terminal": {
        "synonyms": ["incurable and fatal", "end-stage", "moribund", "lethal"],
        "antonyms": ["curable", "treatable", "non-fatal"]
    },
    "Contagious": {
        "synonyms": ["infectious", "communicable", "transmissible", "catching"],
        "antonyms": ["non-communicable", "non-transmissible", "sterile"]
    },
    "Innate": {
        "synonyms": ["intrinsic", "inherent", "ingrained", "congenital"],
        "antonyms": ["acquired", "learned", "extraneous"]
    },
    "Immune": {
        "synonyms": ["resistant", "impervious", "exempt", "invulnerable"],
        "antonyms": ["susceptible", "vulnerable", "predisposed"]
    },
    "Acute": {
        "synonyms": ["sharp", "sudden and intense", "critical", "severe"],
        "antonyms": ["chronic", "mild", "dull"]
    },
    "Robust": {
        "synonyms": ["hardy", "vigorous", "sturdy", "resilient"],
        "antonyms": ["frail", "feeble", "delicate"]
    },
    "Psychological": {
        "synonyms": ["mental", "cerebral", "psychic", "cognitive"],
        "antonyms": ["physiological", "somatic", "corporeal"]
    },
    "Physiological": {
        "synonyms": ["somatic", "biological", "bodily", "anatomical"],
        "antonyms": ["psychological", "mental", "spiritual"]
    },
    "Strenuous": {
        "synonyms": ["arduous", "laborious", "taxing", "exertive"],
        "antonyms": ["effortless", "sedentary", "light"]
    },
    "Wholesome": {
        "synonyms": ["salubrious", "nourishing", "healthful", "beneficial"],
        "antonyms": ["insalubrious", "toxic", "unwholesome"]
    },
    "Beneficial": {
        "synonyms": ["advantageous", "salutary", "conducive to health", "helpful"],
        "antonyms": ["detrimental", "harmful", "pernicious"]
    },
    "Malignant": {
        "synonyms": ["cancerous", "virulent", "pernicious", "destructive"],
        "antonyms": ["benign", "harmless", "non-invasive"]
    },
    "Benign": {
        "synonyms": ["non-cancerous", "harmless", "innocuous", "mild"],
        "antonyms": ["malignant", "virulent", "fatal"]
    },
    "Incurable": {
        "synonyms": ["untreatable", "irremediable", "terminal", "hopeless"],
        "antonyms": ["curable", "treatable", "remediable"]
    },
    "Debilitating": {
        "synonyms": ["enervating", "incapacitating", "weakening", "crippling"],
        "antonyms": ["invigorating", "rehabilitative", "strengthening"]
    },
    "Hazardous": {
        "synonyms": ["perilous", "deleterious", "precarious", "risky"],
        "antonyms": ["safe", "innocuous", "secure"]
    },
    "Take a heavy toll on": {
        "synonyms": ["inflict grave harm upon", "exact a severe price from", "severely impair"],
        "antonyms": ["invigorate and fortify", "nurture and revitalise"]
    },
    "Lead a sedentary lifestyle": {
        "synonyms": ["maintain an inactive physical routine", "engage in prolonged sitting habits", "remain physically idle"],
        "antonyms": ["maintain an active regimen", "lead a vigorous active lifestyle"]
    },
    "Nip the problem in the bud": {
        "synonyms": ["halt an issue early", "prevent escalation at inception", "curtail early development"],
        "antonyms": ["allow an illness to fester", "ignore symptoms until critical"]
    },
    "Strike a balance between rest and work": {
        "synonyms": ["harmonize labor and recuperation", "maintain circadian work-rest equilibrium", "equitably apportion activity and recovery"],
        "antonyms": ["overwork to burnout", "surrender to relentless fatigue"]
    },
    "Pave the way for a healthy life": {
        "synonyms": ["lay the foundation for longevity", "facilitate sustained physical vitality", "enable long-term wellness"],
        "antonyms": ["engender chronic pathology", "hasten premature physical decay"]
    },
    "Pose a grave threat to health": {
        "synonyms": ["jeopardize physical well-being critically", "menace human health", "imperil physiological integrity"],
        "antonyms": ["bolster constitutional health", "safeguard bodily vitality"]
    },
    "Bear fruit in physical vitality": {
        "synonyms": ["yield tangible health rewards", "manifest in peak physical energy", "result in robust vitality"],
        "antonyms": ["culminate in chronic fatigue", "produce zero physical improvement"]
    },
    "Fall prey to chronic illness": {
        "synonyms": ["succumb to persistent pathology", "contract lingering disease", "become afflicted with long-term sickness"],
        "antonyms": ["fend off disease successfully", "maintain robust resistance"]
    },
    "At the expense of physical health": {
        "synonyms": ["sacrificing bodily well-being", "to the detriment of somatic wellness", "compromising physiological integrity"],
        "antonyms": ["preserving bodily vigor", "prioritizing physical wellness"]
    },
    "Reap the rewards of clean living": {
        "synonyms": ["harvest benefits of a healthy lifestyle", "enjoy fruits of wholesome habits", "gain vitality from clean nutrition"],
        "antonyms": ["suffer consequences of toxic habits", "pay the penalty of intemperance"]
    },
    "Exert immense pressure on hospitals": {
        "synonyms": ["severely strain clinical facilities", "overburden healthcare institutions", "tax hospital bed capacities"],
        "antonyms": ["relieve clinical burden", "ease strain on medical infrastructure"]
    },
    "Shed light on mental health": {
        "synonyms": ["illuminate psychiatric challenges", "clarify psychological well-being", "demystify emotional disorders"],
        "antonyms": ["obscure mental distress", "reinforce psychiatric stigma"]
    },
    "Draw a line between": {
        "synonyms": ["differentiate rigorously between", "demarcate clearly between", "distinguish precisely between"],
        "antonyms": ["conflate carelessly", "blur distinctions between"]
    },
    "Sound the alarm over obesity": {
        "synonyms": ["warn urgently against rising adiposity", "alert the public to metabolic risks", "issue warnings regarding weight gain"],
        "antonyms": ["trivialize the weight epidemic", "ignore metabolic danger signs"]
    },
    "Hold pharmaceutical firms accountable": {
        "synonyms": ["enforce corporate liability on drug companies", "compel pharmacological transparency", "penalize drug maker malpractice"],
        "antonyms": ["grant drug firms absolute indemnity", "overlook pharmaceutical abuses"]
    },
    "Set a benchmark for hygiene": {
        "synonyms": ["establish exemplary cleanliness standards", "institute rigorous sanitary criteria", "define optimal hygiene guidelines"],
        "antonyms": ["lower sanitation standards", "tolerate squalid conditions"]
    },
    "Overcome physical hurdles": {
        "synonyms": ["conquer somatic limitations", "surmount bodily impediments", "transcend physiological barriers"],
        "antonyms": ["surrender to physical limitations", "succumb to bodily infirmity"]
    },
    "Adhere to strict nutritional guidelines": {
        "synonyms": ["strictly observe dietary prescriptions", "faithfully comply with nutritional rules", "abide by dietary standards"],
        "antonyms": ["abandon all dietary restraint", "consume unmonitored junk food"]
    },
    "In the prime of one's life": {
        "synonyms": ["at the peak of vitality", "in one's physical zenith", "during one's golden adult vigor"],
        "antonyms": ["in one's twilight years", "during dotage and decrepitude"]
    },
    "Turn a blind eye to symptoms": {
        "synonyms": ["deliberately ignore warning signs", "willfully disregard pathological signals", "neglect early illness indicators"],
        "antonyms": ["heed medical warning signs", "seek immediate diagnostic evaluation"]
    },
    "Keep body and soul together": {
        "synonyms": ["sustain bare physical existence", "maintain minimal subsistence", "survive against hardship"],
        "antonyms": ["thrive in luxurious comfort", "succumb to deprivation"]
    },
    "Clean bill of health": {
        "synonyms": ["medical certificate of complete fitness", "unblemished health clearance", "flawless clinical evaluation"],
        "antonyms": ["adverse medical diagnosis", "poor prognosis"]
    },
    "Under the weather": {
        "synonyms": ["indisposed", "slightly unwell", "ailing mildly", "below par"],
        "antonyms": ["in the peak of health", "thoroughly invigorated"]
    },
    "Fit as a fiddle": {
        "synonyms": ["in prime physical condition", "exceptionally healthy", "bursting with vitality"],
        "antonyms": ["infirm and ailing", "moribund and bedridden"]
    },
    "Alive and kicking": {
        "synonyms": ["vigorous and active", "full of buoyant life", "flourishing dynamically"],
        "antonyms": ["moribund", "ailing and bedridden"]
    },
    "Bite the bullet": {
        "synonyms": ["face painful treatment bravely", "endure necessary medical discomfort", "accept grim clinical reality"],
        "antonyms": ["shrink from painful therapy", "evade necessary medical action"]
    },
    "Cast aside unhealthy habits": {
        "synonyms": ["abandon deleterious behaviors", "relinquish harmful lifestyle patterns", "repudiate detrimental habits"],
        "antonyms": ["cling stubbornly to vice", "indulge unhealthful impulses"]
    },
    "Incur enormous healthcare bills": {
        "synonyms": ["amass crippling medical expenses", "run up massive clinical debts", "suffer exorbitant hospitalization fees"],
        "antonyms": ["receive fully covered free care", "enjoy zero out-of-pocket healthcare costs"]
    },
    "Champion the cause of public health": {
        "synonyms": ["spearhead community wellness advocacy", "crusade for epidemiological safety", "zealously promote hygiene"],
        "antonyms": ["lobby against public health measures", "oppose health regulations"]
    },
    "Trigger irreversible bodily harm": {
        "synonyms": ["inflict permanent physical damage", "cause irremediable somatic injury", "induce lasting physiological lesions"],
        "antonyms": ["facilitate complete physical recovery", "heal bodily trauma"]
    },
    "Back on one's feet": {
        "synonyms": ["recuperated", "fully recovered from illness", "physically convalescent"],
        "antonyms": ["bedridden and incapacitated", "relapsing into illness"]
    },
    "Under the knife": {
        "synonyms": ["undergoing surgery", "in the operating theater", "subject to surgical intervention"],
        "antonyms": ["treated conservatively with medication", "undergoing non-invasive therapy"]
    },
    "Just what the doctor ordered": {
        "synonyms": ["ideally beneficial remedy", "perfect therapeutic antidote", "precisely what is required for recovery"],
        "antonyms": ["severely contraindicated treatment", "detrimental remedy"]
    },
    "Break down": {
        "synonyms": ["collapse emotionally or physically", "succumb to nervous prostration", "founder biologically"],
        "antonyms": ["rally resiliently", "regain composure"]
    },
    "Pass out": {
        "synonyms": ["lose consciousness", "swoon", "faint abruptly"],
        "antonyms": ["regain consciousness", "revive and awaken"]
    },
    "Fight off": {
        "synonyms": ["repel an infection", "resist a pathogen", "fend off an illness"],
        "antonyms": ["succumb to a virus", "catch an infection"]
    },
    "Come down with": {
        "synonyms": ["contract an illness", "fall sick with", "become infected with"],
        "antonyms": ["recover fully from", "shake off an infection"]
    },
    "Cut down on": {
        "synonyms": ["curtail dietary intake of", "reduce consumption of", "scale back ingestion of"],
        "antonyms": ["indulge excessively in", "escalate consumption of"]
    },
    "Build up": {
        "synonyms": ["cultivate physical stamina", "fortify bodily immunity", "augment strength incrementally"],
        "antonyms": ["dissipate vitality", "enfeeble physical reserves"]
    },
    "Shake off": {
        "synonyms": ["dispensate with an illness", "overcome a sickness", "rid oneself of a mild infection"],
        "antonyms": ["linger in illness", "succumb to chronic disease"]
    },
    "Taper off": {
        "synonyms": ["decrease dosage incrementally", "wean off gradually", "diminish medication slowly"],
        "antonyms": ["escalate dosage abruptly", "increase intake sharply"]
    },
    "Worn out": {
        "synonyms": ["physically exhausted", "enervated", "thoroughly drained of energy"],
        "antonyms": ["invigorated", "rejuvenated", "refreshed"]
    },
    "Take one's breath away": {
        "synonyms": ["induce temporary dyspnea", "astonish to speechlessness", "overwhelm profoundly"],
        "antonyms": ["leave completely unaffected", "induce calm steady respiration"]
    },
    "Get over": {
        "synonyms": ["recover from pathology", "recuperate from an illness", "conquer physical malaise"],
        "antonyms": ["succumb permanently to", "relapse into illness"]
    },
    "Challengingly": {
        "synonyms": ["demanding utmost resilience", "arduously", "with formidable difficulty"],
        "antonyms": ["effortlessly", "trivially", "facilely"]
    },
    "Chronically": {
        "synonyms": ["persistently", "lingeringly over time", "inveterately"],
        "antonyms": ["transiently", "temporarily", "fleetingly"]
    },
    "Severely": {
        "synonyms": ["gravely", "critically", "acutely", "drastically"],
        "antonyms": ["mildly", "moderately", "superficially"]
    },
    "Invariably": {
        "synonyms": ["consistently", "unfailingly", "inevitably"],
        "antonyms": ["erratically", "sporadically", "unpredictably"]
    },
    "Radically": {
        "synonyms": ["profoundly", "fundamentally", "sweepingly"],
        "antonyms": ["marginally", "incrementally", "superficially"]
    },
    "Preventatively": {
        "synonyms": ["prophylactically", "as a precautionary measure", "preventively"],
        "antonyms": ["reactively", "retrospectively", "curatively"]
    },
    "Beneficially": {
        "synonyms": ["salubriously", "advantageously", "healthfully"],
        "antonyms": ["detrimentally", "perniciously", "noxiously"]
    },
    "Physiologically": {
        "synonyms": ["somatically", "biologically", "bodily"],
        "antonyms": ["psychologically", "conceptually", "immaterially"]
    },
    "Disproportionately": {
        "synonyms": ["asymmetrically", "inequitably", "inordinately"],
        "antonyms": ["proportionately", "equitably", "evenly"]
    }
}

def update_health():
    with open(HEALTH_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    updated = 0
    words = data.get("words", [])
    for w in words:
        name = w.get("word")
        if name in HEALTH_LEXICON:
            w["synonyms"] = HEALTH_LEXICON[name]["synonyms"]
            w["antonyms"] = HEALTH_LEXICON[name]["antonyms"]
            updated += 1
            
    with open(HEALTH_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully updated {updated} words in health.json!")
    return updated

if __name__ == "__main__":
    update_health()
