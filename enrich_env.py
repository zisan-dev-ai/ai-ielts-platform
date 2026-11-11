# -*- coding: utf-8 -*-
"""
Exhaustive Band 8.0-9.0 Academic Lexicon for 'environment'
Updates environment.json with authentic synonyms and antonyms.
"""
import json
import os

PLATFORM_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(PLATFORM_DIR, "ai_engine", "vocab_db", "environment.json")

ENV_LEXICON = {
    "Ecological footprint": {
        "synonyms": ["environmental impact", "carbon and resource burden", "biophysical demand"],
        "antonyms": ["ecological sustainability", "neutral environmental impact"]
    },
    "Carbon neutrality": {
        "synonyms": ["net-zero carbon emissions", "climate neutrality", "zero-carbon balance"],
        "antonyms": ["carbon-intensive emissions", "positive net carbon output"]
    },
    "Biodiversity depletion": {
        "synonyms": ["species loss", "biological impoverishment", "ecosystem defaunation"],
        "antonyms": ["biodiversity conservation", "ecological replenishment"]
    },
    "Renewable energy infrastructure": {
        "synonyms": ["clean power grid", "sustainable energy installations", "green utility network"],
        "antonyms": ["fossil-fuel infrastructure", "coal-fired power network"]
    },
    "Greenhouse gas emissions": {
        "synonyms": ["atmospheric heat-trapping discharges", "carbon effluent", "climate-warming gases"],
        "antonyms": ["zero-emission output", "atmospheric carbon sequestration"]
    },
    "Environmental degradation": {
        "synonyms": ["ecological deterioration", "habitat decay", "biosphere decline"],
        "antonyms": ["ecological restoration", "environmental remediation"]
    },
    "Anthropogenic climate change": {
        "synonyms": ["human-induced global warming", "man-made climate disruption", "artificial atmospheric warming"],
        "antonyms": ["natural climatic variability", "solar-driven climate variation"]
    },
    "Sustainable agriculture practice": {
        "synonyms": ["regenerative farming", "agroecological stewardship", "eco-friendly cultivation"],
        "antonyms": ["intensive industrial agriculture", "monoculture farming"]
    },
    "Extreme weather event": {
        "synonyms": ["meteorological anomaly", "severe climatic aberration", "violent weather catastrophe"],
        "antonyms": ["temperate climatic stability", "equable seasonal weather"]
    },
    "Ozone layer depletion": {
        "synonyms": ["stratospheric ozone thinning", "ozonosphere exhaustion", "shield rarefaction"],
        "antonyms": ["ozone layer recovery", "stratospheric ozone regeneration"]
    },
    "Deforestation rate": {
        "synonyms": ["forest clearance pace", "canopy loss velocity", "tree clearance rate"],
        "antonyms": ["afforestation pace", "reforestation rate"]
    },
    "Non-biodegradable waste": {
        "synonyms": ["persistent refuse", "indestructible synthetic debris", "non-decomposable trash"],
        "antonyms": ["compostable material", "biodegradable matter"]
    },
    "Marine ecosystem conservation": {
        "synonyms": ["oceanic habitat preservation", "pelagic biodiversity stewardship", "marine sanctuary protection"],
        "antonyms": ["oceanic exploitation", "marine habitat destruction"]
    },
    "Fossil fuel dependency": {
        "synonyms": ["hydrocarbon reliance", "petrochemical addiction", "carbon energy dependence"],
        "antonyms": ["renewable energy self-sufficiency", "decarbonized energy reliance"]
    },
    "Urban heat island effect": {
        "synonyms": ["metropolitan thermal anomaly", "urban microclimate warming", "city heat accumulation"],
        "antonyms": ["rural cooling effect", "urban green canopy cooling"]
    },
    "Water scarcity crisis": {
        "synonyms": ["acute freshwater deficit", "hydrological stress", "water emergency"],
        "antonyms": ["aquatic abundance", "hydrological surplus"]
    },
    "Glacial retreat": {
        "synonyms": ["ice-mass recession", "cryospheric melting", "glacier contraction"],
        "antonyms": ["glacial advance", "ice sheet expansion"]
    },
    "Air quality index": {
        "synonyms": ["atmospheric purity metric", "pollution level indicator", "air pollution grading"],
        "antonyms": ["unregulated pollution exposure", "unmonitored air toxins"]
    },
    "Afforestation campaign": {
        "synonyms": ["tree-planting initiative", "woodland expansion project", "canopy replenishment drive"],
        "antonyms": ["logging deforestation", "woodland clearing operation"]
    },
    "Hazardous industrial effluent": {
        "synonyms": ["toxic factory wastewater", "chemical industrial discharge", "lethal manufacturing runoff"],
        "antonyms": ["purified wastewater outflow", "treated neutral discharge"]
    },
    "Desertification process": {
        "synonyms": ["arid land degradation", "fertile soil desiccation", "dryland expansion"],
        "antonyms": ["land rehabilitation", "vegetative reclamation"]
    },
    "Ecosystem equilibrium": {
        "synonyms": ["ecological balance", "biosphere stability", "environmental homeostasis"],
        "antonyms": ["ecological disequilibrium", "ecosystem disruption"]
    },
    "Carbon sequestration project": {
        "synonyms": ["atmospheric carbon trapping", "carbon capture and storage scheme", "biological sink enhancement"],
        "antonyms": ["atmospheric carbon venting", "carbon release activity"]
    },
    "Single-use plastic restriction": {
        "synonyms": ["disposable plastic ban", "single-use packaging embargo", "throwaway polymer phase-out"],
        "antonyms": ["unregulated plastic distribution", "disposable packaging deregulation"]
    },
    "Toxic chemical runoff": {
        "synonyms": ["poisonous agricultural drainage", "chemical contaminant leaching", "toxic pesticide outflow"],
        "antonyms": ["uncontaminated groundwater filtration", "pure surface runoff"]
    },
    "Permafrost thaw": {
        "synonyms": ["cryotic soil degradation", "frozen ground liquefaction", "arctic permafrost decay"],
        "antonyms": ["cryospheric refreezing", "permafrost stabilization"]
    },
    "Soil erosion risk": {
        "synonyms": ["topsoil depletion hazard", "soil washing vulnerability", "arable land degradation threat"],
        "antonyms": ["soil stabilization security", "terraced erosion prevention"]
    },
    "Endangered wildlife sanctuary": {
        "synonyms": ["threatened species refuge", "faunal nature reserve", "biodiversity reserve"],
        "antonyms": ["hunting zone", "poaching concession"]
    },
    "Subsidized solar panel": {
        "synonyms": ["incentivized photovoltaic module", "state-supported solar installation", "rebated clean power array"],
        "antonyms": ["unsubsidized tariff system", "fossil energy taxation exemption"]
    },
    "Circular economic model": {
        "synonyms": ["closed-loop resource system", "regenerative economic paradigm", "waste-free cycle"],
        "antonyms": ["linear throwaway economy", "extractive consumption paradigm"]
    },
    "Atmospheric warming trend": {
        "synonyms": ["climatic heating trajectory", "global thermal escalation", "long-term warming pattern"],
        "antonyms": ["planetary cooling trend", "climatic stabilization"]
    },
    "Habitat fragmentation": {
        "synonyms": ["landscape dissection", "ecosystem compartmentalization", "patch isolation"],
        "antonyms": ["ecological corridors", "contiguous habitat preservation"]
    },
    "Ocean acidification impact": {
        "synonyms": ["pelagic calcification impairment", "marine pH reduction fallout", "acidic seawater consequence"],
        "antonyms": ["oceanic alkaline equilibrium", "marine pH stabilization"]
    },
    "Ecological restoration effort": {
        "synonyms": ["habitat re-wilding initiative", "ecosystem rehabilitation project", "environmental remediation"],
        "antonyms": ["environmental destruction", "industrial land degradation"]
    },
    "Sustainable resource stewardship": {
        "synonyms": ["responsible conservation management", "prudent environmental custodianship", "ecological guardianship"],
        "antonyms": ["reckless resource exploitation", "predatory resource extraction"]
    },
    "Waste diversion rate": {
        "synonyms": ["landfill reduction percentage", "recycling diversion efficiency", "salvaged refuse ratio"],
        "antonyms": ["landfill disposal volume", "direct waste dumping rate"]
    },
    "Geothermal energy facility": {
        "synonyms": ["subterranean heat power station", "geothermal generating plant", "thermal earth-energy facility"],
        "antonyms": ["coal-powered thermal station", "oil combustion facility"]
    },
    "Species extinction vulnerability": {
        "synonyms": ["endangerment susceptibility", "demise probability", "faunal fragility"],
        "antonyms": ["species adaptability", "population resilience"]
    },
    "Ecological catastrophe": {
        "synonyms": ["environmental calamity", "biospheric disaster", "cataclysmic ecological collapse"],
        "antonyms": ["ecological flourishing", "environmental triumph"]
    },
    "Zero-emission public transport": {
        "synonyms": ["green mass transit", "clean electric conveyance", "decarbonized communal transit"],
        "antonyms": ["fossil-fueled transit fleet", "high-emission bus service"]
    },
    "Microplastic contamination": {
        "synonyms": ["synthetic micro-debris presence", "particulate plastic pollution", "polymer contaminant accumulation"],
        "antonyms": ["pristine unpolluted waterways", "microparticle-free filtration"]
    },
    "Environmental sustainability index": {
        "synonyms": ["ecological health benchmark", "green performance metric", "sustainability assessment matrix"],
        "antonyms": ["unregulated resource depletion index", "environmental negligence scorecard"]
    },
    "Land reclamation initiative": {
        "synonyms": ["soil rehabilitation project", "terrain restoration scheme", "brownfield redevelopment"],
        "antonyms": ["land abandonment", "industrial land ruination"]
    },
    "Clean energy grid": {
        "synonyms": ["renewable transmission network", "decarbonized electrical system", "green power infrastructure"],
        "antonyms": ["coal-reliant grid network", "fossil-fueled power conduit"]
    },
    "Flora and fauna preservation": {
        "synonyms": ["plant and animal conservation", "wildlife safeguarding", "biodiversity protection"],
        "antonyms": ["biological extermination", "wholesale habitat destruction"]
    },
    "Smog formation alert": {
        "synonyms": ["atmospheric smog warning", "particulate haze bulletin", "photochemical smoke alert"],
        "antonyms": ["clear skies advisory", "pristine air announcement"]
    },
    "Reforestation subsidy": {
        "synonyms": ["woodland restoration grant", "afforestation financial incentive", "canopy revival subvention"],
        "antonyms": ["timber clearance royalty", "logging concession tax-break"]
    },
    "Rainwater harvesting system": {
        "synonyms": ["stormwater catchment setup", "precipitation collection apparatus", "rainwater reservoir installation"],
        "antonyms": ["unintercepted runoff discharge", "stormwater wastage"]
    },
    "Pesticide leaching hazard": {
        "synonyms": ["agrochemical seepage threat", "pesticide percolation risk", "subsurface toxic chemical migration"],
        "antonyms": ["organic soil purity", "chemical-free agricultural runoff"]
    },
    "Ecological resilience": {
        "synonyms": ["ecosystem robustness", "environmental bounce-back capacity", "biological adaptability"],
        "antonyms": ["ecological fragility", "vulnerability to collapse"]
    },
    "Green urban planning": {
        "synonyms": ["sustainable metropolitan design", "eco-friendly civic layout", "climate-resilient town development"],
        "antonyms": ["uncontrolled urban sprawl", "concrete-dominated urban development"]
    },
    "Environmental compliance audit": {
        "synonyms": ["ecological regulatory inspection", "environmental statutory review", "pollution standards check"],
        "antonyms": ["regulatory circumvention", "environmental non-compliance oversight"]
    },
    "Polluter pays principle": {
        "synonyms": ["polluter liability doctrine", "externalized damage accountability", "contamination restitution rule"],
        "antonyms": ["taxpayer-funded cleanup subsidy", "corporate environmental impunity"]
    },
    "Energy conservation campaign": {
        "synonyms": ["power-saving initiative", "energy curtailment drive", "efficiency promotion program"],
        "antonyms": ["profligate energy consumption", "wasteful electrical overconsumption"]
    },
    "Ozone depleting substance": {
        "synonyms": ["stratospheric ozone destroyer", "ozone-depleting halocarbon", "aerosol propellant toxin"],
        "antonyms": ["ozone-safe alternative", "benign refrigerant"]
    },
    "Renewable resource allocation": {
        "synonyms": ["sustainable resource distribution", "clean asset apportionment", "green capital deployment"],
        "antonyms": ["depleting resource squandering", "fossil fuel subsidization"]
    },
    "Carbon credit trading": {
        "synonyms": ["emissions allowance exchange", "cap-and-trade system", "carbon offset commerce"],
        "antonyms": ["unregulated greenhouse dumping", "punitive non-tradable bans"]
    },
    "E-waste disposal protocol": {
        "synonyms": ["electronic scrap processing guideline", "digital hardware recycling code", "WEEE management policy"],
        "antonyms": ["illicit e-waste dumping", "landfill electronics incineration"]
    },
    "Riparian buffer zone": {
        "synonyms": ["riverbank vegetative corridor", "waterway filter strip", "riverine conservation belt"],
        "antonyms": ["deforested riverbank", "unbuffered agricultural waterfront"]
    },
    "Endangered species legislation": {
        "synonyms": ["wildlife preservation act", "threatened species statutory protection", "faunal conservation charter"],
        "antonyms": ["hunting deregulation", "poaching impunity policies"]
    },
    "Industrial carbon tax": {
        "synonyms": ["manufacturing emissions levy", "fossil fuel effluent duty", "corporate carbon tariff"],
        "antonyms": ["carbon subsidy", "polluter tax shelter"]
    },
    "Wildfire containment strategy": {
        "synonyms": ["bushfire suppression protocol", "forest fire mitigation plan", "wildfire control regimen"],
        "antonyms": ["uncontrolled blaze propagation", "wildfire negligence"]
    },
    "Aquifer depletion": {
        "synonyms": ["groundwater overextraction", "water table exhaustion", "subsurface reservoir draining"],
        "antonyms": ["aquifer replenishment", "groundwater recharge"]
    },
    "Global climate accord": {
        "synonyms": ["multilateral environmental treaty", "international climate compact", "intergovernmental emissions pact"],
        "antonyms": ["unilateral environmental withdrawal", "climate treaty abandonment"]
    },
    "Plastic recycling quota": {
        "synonyms": ["polymer reclamation target", "statutory plastic re-processing mandate", "circular plastic benchmark"],
        "antonyms": ["unrestricted virgin plastic reliance", "plastic waste incineration reliance"]
    },
    "Environmental whistle-blowing": {
        "synonyms": ["ecological malpractice reporting", "corporate pollution disclosure", "green misconduct reporting"],
        "antonyms": ["environmental collusion", "pollution cover-up"]
    },
    "Renewable energy storage": {
        "synonyms": ["clean power grid battery", "renewable accumulation capacity", "green energy reserve"],
        "antonyms": ["real-time power waste", "curtailed clean generation"]
    },
    "Coral bleaching event": {
        "synonyms": ["thermal reef expulsion", "zooxanthellae loss episode", "reef whitening crisis"],
        "antonyms": ["coral reef thriving", "symbiotic reef calcification"]
    },
    "Sustainable forestry management": {
        "synonyms": ["responsible timber silviculture", "controlled canopy husbandry", "sustainable wood harvesting"],
        "antonyms": ["indiscriminate clear-cutting", "predatory logging"]
    },
    "Clean air legislation": {
        "synonyms": ["atmospheric quality statute", "anti-smog statutory act", "emissions control legal framework"],
        "antonyms": ["air pollution deregulation", "unrestricted chimney venting laws"]
    },
    "Waste incineration facility": {
        "synonyms": ["thermal refuse disposal plant", "waste-to-energy combustor", "municipal incinerator"],
        "antonyms": ["zero-waste composting unit", "recycling sorting depot"]
    },
    "Ecological balance restoration": {
        "synonyms": ["biosphere equilibrium recovery", "ecosystem harmony reinstatement", "biodiversity balance re-establishment"],
        "antonyms": ["ecological disruption", "ecosystem destabilization"]
    },
    "Topsoil preservation": {
        "synonyms": ["fertile loam retention", "humus layer conservation", "arable soil safeguarding"],
        "antonyms": ["topsoil erosion", "humus layer stripping"]
    },
    "Sustainable consumerism": {
        "synonyms": ["eco-conscious purchasing", "ethical retail acquisition", "responsible resource consumption"],
        "antonyms": ["conspicuous hyper-consumerism", "disposable throwaway culture"]
    },
    "Biodegradable packaging alternative": {
        "synonyms": ["compostable wrapper substitute", "plant-based packaging option", "organic container solution"],
        "antonyms": ["single-use non-biodegradable polymer", "indestructible plastic packaging"]
    },
    "Environmental impact assessment": {
        "synonyms": ["ecological consequence appraisal", "pre-development environmental audit", "biospheric scrutiny report"],
        "antonyms": ["unvetted commercial expansion", "unscrutinized industrial development"]
    },
    "Renewable energy pioneer": {
        "synonyms": ["clean tech trailblazer", "sustainable power innovator", "green energy vanguard"],
        "antonyms": ["fossil fuel advocate", "petrochemical traditionalist"]
    },
    "Overfishing moratorium": {
        "synonyms": ["commercial fishing ban", "marine harvest embargo", "fish stock replenishment closure"],
        "antonyms": ["unregulated high-seas trawling", "unlimited fishery extraction"]
    },
    "Zero-waste lifestyle": {
        "synonyms": ["waste-free living", "circular home routine", "minimalist refuse approach"],
        "antonyms": ["throwaway consumerism", "waste-intensive living"]
    },
    "Wetland reclamation safeguard": {
        "synonyms": ["marshland preservation barrier", "estuary conservation guarantee", "swamp protection standard"],
        "antonyms": ["wetland drainage", "estuarine destruction"]
    },
    "Degrade": {
        "synonyms": ["deteriorate", "impoverish", "debase", "corrupt"],
        "antonyms": ["ameliorate", "rejuvenate", "restore"]
    },
    "Contaminate": {
        "synonyms": ["pollute", "taint", "adulterate", "befoul"],
        "antonyms": ["purify", "decontaminate", "cleanse"]
    },
    "Dismantle": {
        "synonyms": ["deconstruct", "demolish", "disassemble", "strip down"],
        "antonyms": ["construct", "assemble", "erect"]
    },
    "Conserve": {
        "synonyms": ["preserve", "safeguard", "husband", "protect"],
        "antonyms": ["squander", "dissipate", "exhaust"]
    },
    "Endanger": {
        "synonyms": ["imperil", "jeopardize", "compromise", "threaten"],
        "antonyms": ["shield", "protect", "safeguard"]
    },
    "Harness": {
        "synonyms": ["utilize", "exploit", "channel", "leverage"],
        "antonyms": ["misuse", "forfeit", "waste"]
    },
    "Phase out": {
        "synonyms": ["eliminate gradually", "discontinue incrementally", "decommission", "sunset"],
        "antonyms": ["introduce", "instate", "scale up"]
    },
    "Stem": {
        "synonyms": ["curtail", "halt", "check", "staunch"],
        "antonyms": ["unleash", "accelerate", "aggravate"]
    },
    "Remediate": {
        "synonyms": ["rectify", "rehabilitate", "cleanse", "redress"],
        "antonyms": ["contaminate", "worsen", "aggravate"]
    },
    "Decouple": {
        "synonyms": ["disentangle", "sever", "dissociate", "disconnect"],
        "antonyms": ["integrate", "correlate", "intertwine"]
    },
    "Pave the way for": {
        "synonyms": ["facilitate", "lay the groundwork for", "expedite", "catalyze"],
        "antonyms": ["impede", "thwart", "obstruct"]
    },
    "Infringe upon": {
        "synonyms": ["encroach on", "transgress", "violate", "trespass"],
        "antonyms": ["respect", "honor", "uphold"]
    },
    "Overconsume": {
        "synonyms": ["squander", "deplete excessively", "binge on", "overindulge in"],
        "antonyms": ["conserve", "ration", "husband"]
    },
    "Offset": {
        "synonyms": ["counterbalance", "compensate for", "neutralize", "redress"],
        "antonyms": ["exacerbate", "compound", "skew"]
    },
    "Plummet": {
        "synonyms": ["plummet", "drop steeply", "nosedive", "tumble"],
        "antonyms": ["surge", "soar", "escalate"]
    },
    "Discharge": {
        "synonyms": ["emit", "eject", "release", "vent"],
        "antonyms": ["absorb", "retain", "capture"]
    },
    "Spearhead": {
        "synonyms": ["champion", "pioneer", "lead", "instigate"],
        "antonyms": ["trail", "impede", "follow passively"]
    },
    "Subsume": {
        "synonyms": ["incorporate", "assimilate", "encompass", "integrate"],
        "antonyms": ["segregate", "exclude", "isolate"]
    },
    "Overharvest": {
        "synonyms": ["overextract", "overexploit", "deplete by harvesting", "strip bare"],
        "antonyms": ["replenish", "propagate", "nurture"]
    },
    "Promulgate": {
        "synonyms": ["enact officially", "proclaim", "institute legislatively", "disseminate"],
        "antonyms": ["repeal", "rescind", "suppress"]
    },
    "Stave off": {
        "synonyms": ["ward off", "fend off", "avert", "forestall"],
        "antonyms": ["precipitate", "accelerate", "invite"]
    },
    "Exert": {
        "synonyms": ["wield", "apply", "inflict", "exercise"],
        "antonyms": ["withhold", "suspend", "relax"]
    },
    "Incentivize": {
        "synonyms": ["stimulate", "encourage", "spur", "motivate"],
        "antonyms": ["discourage", "deter", "penalize"]
    },
    "Exhaust": {
        "synonyms": ["deplete", "drain", "spend completely", "hollow out"],
        "antonyms": ["replenish", "restore", "augment"]
    },
    "Encroach": {
        "synonyms": ["intrude", "infringe", "trespass", "advance stealthily"],
        "antonyms": ["retreat", "recede", "withdraw"]
    },
    "Mandate": {
        "synonyms": ["command legally", "decree", "compel", "stipulate"],
        "antonyms": ["prohibit", "exempt", "deregulate"]
    },
    "Catastrophic": {
        "synonyms": ["calamitous", "disastrous", "devastating", "ruinous"],
        "antonyms": ["auspicious", "beneficial", "fortuitous"]
    },
    "Irreversible": {
        "synonyms": ["irrevocable", "unalterable", "permanent", "irremediable"],
        "antonyms": ["reversible", "mutable", "salvageable"]
    },
    "Biodegradable": {
        "synonyms": ["compostable", "decomposable", "ecologically degradable"],
        "antonyms": ["non-biodegradable", "synthetic", "persistent"]
    },
    "Finite": {
        "synonyms": ["limited", "exhaustible", "circumscribed", "restricted"],
        "antonyms": ["infinite", "inexhaustible", "boundless"]
    },
    "Insurmountable": {
        "synonyms": ["invincible", "unconquerable", "impassable", "formidable"],
        "antonyms": ["surmountable", "manageable", "tractable"]
    },
    "Pristine": {
        "synonyms": ["untouched", "unspoiled", "immaculate", "virgin"],
        "antonyms": ["defiled", "contaminated", "blighted"]
    },
    "Hazardous": {
        "synonyms": ["perilous", "deleterious", "precarious", "dangerous"],
        "antonyms": ["harmless", "benign", "safe"]
    },
    "Toxic": {
        "synonyms": ["venomous", "poisonous", "noxious", "virulent"],
        "antonyms": ["non-toxic", "wholesome", "therapeutic"]
    },
    "Ephemeral": {
        "synonyms": ["fleeting", "transitory", "evanescent", "short-lived"],
        "antonyms": ["enduring", "perpetual", "eternal"]
    },
    "Alarming": {
        "synonyms": ["disquieting", "distressing", "ominous", "worrisome"],
        "antonyms": ["reassuring", "comforting", "soothing"]
    },
    "Invaluable": {
        "synonyms": ["priceless", "inestimable", "crucial", "irreplaceable"],
        "antonyms": ["worthless", "expendable", "trivial"]
    },
    "Ecological": {
        "synonyms": ["environmental", "ecosystemic", "biological", "natural"],
        "antonyms": ["artificial", "industrial", "synthetic"]
    },
    "Persistent": {
        "synonyms": ["tenacious", "unyielding", "durable", "lingering"],
        "antonyms": ["transient", "fleeting", "intermittent"]
    },
    "Renewable": {
        "synonyms": ["inexhaustible", "sustainable", "regenerative", "replenishable"],
        "antonyms": ["exhaustible", "finite", "non-renewable"]
    },
    "Severe": {
        "synonyms": ["drastic", "stringent", "acute", "grave"],
        "antonyms": ["mild", "moderate", "lenient"]
    },
    "Exhaustible": {
        "synonyms": ["depletable", "consumable", "finite", "limited"],
        "antonyms": ["inexhaustible", "everlasting", "boundless"]
    },
    "Imperiled": {
        "synonyms": ["jeopardized", "endangered", "vulnerable", "threatened"],
        "antonyms": ["protected", "secure", "safeguarded"]
    },
    "Abundant": {
        "synonyms": ["plentiful", "copious", "bountiful", "profuse"],
        "antonyms": ["scarce", "scant", "deficient"]
    },
    "Stagnant": {
        "synonyms": ["sluggish", "motionless", "moribund", "static"],
        "antonyms": ["flowing", "dynamic", "vibrant"]
    },
    "Adverse": {
        "synonyms": ["unfavorable", "detrimental", "hostile", "deleterious"],
        "antonyms": ["advantageous", "favorable", "propitious"]
    },
    "Fragile": {
        "synonyms": ["delicate", "vulnerable", "precarious", "susceptible"],
        "antonyms": ["resilient", "robust", "durable"]
    },
    "Defiled": {
        "synonyms": ["polluted", "corrupted", "sullied", "desecrated"],
        "antonyms": ["purified", "sanctified", "unblemished"]
    },
    "Mitigatory": {
        "synonyms": ["alleviative", "palliative", "assuasive", "moderating"],
        "antonyms": ["exacerbating", "aggravating", "intensifying"]
    },
    "Drastic": {
        "synonyms": ["radical", "sweeping", "rigorous", "extreme"],
        "antonyms": ["gradual", "moderate", "piecemeal"]
    },
    "Exorbitant": {
        "synonyms": ["extravagant", "excessive", "inordinate", "disproportionate"],
        "antonyms": ["reasonable", "modest", "moderate"]
    },
    "Harmful": {
        "synonyms": ["detrimental", "damaging", "pernicious", "noxious"],
        "antonyms": ["beneficial", "salubrious", "harmless"]
    },
    "Green": {
        "synonyms": ["sustainable", "eco-friendly", "environmentally responsible", "low-carbon"],
        "antonyms": ["polluting", "carbon-heavy", "destructive"]
    },
    "Bear the brunt of": {
        "synonyms": ["absorb the primary impact of", "suffer the worst shock of", "take the full force of"],
        "antonyms": ["escape unscathed from", "avoid consequences of"]
    },
    "Sound the alarm over": {
        "synonyms": ["ring warning bells regarding", "alert the public to", "call attention urgently to"],
        "antonyms": ["downplay the danger of", "conceal threats of"]
    },
    "Wreak havoc on": {
        "synonyms": ["inflict severe damage upon", "devastate", "cause widespread ruin to"],
        "antonyms": ["nurture and restore", "protect from harm"]
    },
    "At the expense of the environment": {
        "synonyms": ["to the detriment of nature", "sacrificing ecological integrity", "compromising environmental health"],
        "antonyms": ["in harmony with ecology", "prioritizing environmental sustainability"]
    },
    "Strike an ecological balance": {
        "synonyms": ["establish biospheric equilibrium", "harmonize environmental demands", "achieve ecosystem sustainability"],
        "antonyms": ["destabilize nature", "induce environmental chaos"]
    },
    "Shift toward renewable energy": {
        "synonyms": ["transition to green power", "pivot to clean energy sources", "decarbonize the power mix"],
        "antonyms": ["revert to fossil hydrocarbons", "deepen coal dependence"]
    },
    "Curb carbon emissions": {
        "synonyms": ["curtail greenhouse discharges", "abate carbon output", "constrain atmospheric effluent"],
        "antonyms": ["amplify emissions", "proliferate greenhouse output"]
    },
    "Pose an existential threat to": {
        "synonyms": ["endanger the survival of", "jeopardize the continuity of", "menace the fundamental existence of"],
        "antonyms": ["bolster the longevity of", "guarantee security for"]
    },
    "Deplete natural resources": {
        "synonyms": ["exhaust raw reserves", "drain biosphere assets", "hollow out ecological wealth"],
        "antonyms": ["replenish natural capital", "conserve environmental assets"]
    },
    "Face impending disaster": {
        "synonyms": ["stand before imminent catastrophe", "confront looming calamity", "teeter on disaster"],
        "antonyms": ["enjoy secure stability", "rest in safe sanctuary"]
    },
    "In the wake of catastrophe": {
        "synonyms": ["following severe calamity", "in the aftermath of ruin", "subsequent to devastation"],
        "antonyms": ["prior to any hazard", "anticipating peace"]
    },
    "Pave the pathway for green growth": {
        "synonyms": ["enable sustainable economic expansion", "facilitate eco-friendly prosperity", "foster circular development"],
        "antonyms": ["lock in dirty industrial growth", "block environmental progress"]
    },
    "Exert catastrophic pressure on": {
        "synonyms": ["strain critically", "impose overwhelming burden upon", "tax past breaking point"],
        "antonyms": ["relieve pressure from", "unburden"]
    },
    "Fall into disrepair": {
        "synonyms": ["deteriorate gradually", "decay through neglect", "degenerate into dilapidation"],
        "antonyms": ["undergo diligent maintenance", "flourish under care"]
    },
    "Set an ambitious target": {
        "synonyms": ["establish lofty benchmarks", "aim for rigorous objectives", "pledge demanding goals"],
        "antonyms": ["lower performance expectations", "settle for complacent milestones"]
    },
    "Hold corporations accountable for": {
        "synonyms": ["impose corporate liability regarding", "enforce statutory responsibility on firms for", "penalize enterprise negligence regarding"],
        "antonyms": ["grant commercial immunity for", "absolve enterprises from liability"]
    },
    "Run counter to conservation": {
        "synonyms": ["conflict with preservation goals", "undermine environmental protection", "contravene eco-stewardship"],
        "antonyms": ["align with ecological preservation", "bolster environmental conservation"]
    },
    "Ring alarm bells for humanity": {
        "synonyms": ["signal grave peril for civilization", "alert humanity to mortal danger", "provide an urgent wake-up call"],
        "antonyms": ["lull into false complacency", "soothe public anxiety"]
    },
    "At the tipping point": {
        "synonyms": ["on the verge of critical change", "at the environmental threshold", "at the point of no return"],
        "antonyms": ["in a state of secure equilibrium", "far from critical danger"]
    },
    "Leave an indelible mark on nature": {
        "synonyms": ["inflict permanent ecological scars", "alter the natural world permanently", "imprint irreversible changes on the biosphere"],
        "antonyms": ["tread lightly on the earth", "leave zero environmental imprint"]
    },
    "Tip the delicate balance of nature": {
        "synonyms": ["destabilize ecological harmony", "upset biospheric equilibrium", "derange natural systems"],
        "antonyms": ["reinforce ecological stability", "sustain natural balance"]
    },
    "Pay the price for neglect": {
        "synonyms": ["suffer the fallout of negligence", "bear consequences of inaction", "reap the costs of indifference"],
        "antonyms": ["reap rewards of stewardship", "benefit from proactive care"]
    },
    "Reap the environmental dividend": {
        "synonyms": ["enjoy benefits of green investments", "gain ecological rewards", "harvest returns on conservation"],
        "antonyms": ["suffer the costs of ecological devastation", "incur environmental bankruptcy"]
    },
    "Clean up contaminated sites": {
        "synonyms": ["remediate polluted brownfields", "decontaminate industrial land", "restore toxic locations"],
        "antonyms": ["desecrate virgin lands", "pollute pristine grounds"]
    },
    "Comply with emissions benchmarks": {
        "synonyms": ["meet statutory pollution limits", "adhere to clean air standards", "abide by carbon caps"],
        "antonyms": ["violate environmental thresholds", "breach statutory emissions ceilings"]
    },
    "Act in concert with nature": {
        "synonyms": ["operate in ecological harmony", "align practices with natural cycles", "work symbiotically with the biosphere"],
        "antonyms": ["exploit natural systems ruthlessly", "wreak havoc on natural processes"]
    },
    "Turn a blind eye to pollution": {
        "synonyms": ["willfully overlook contamination", "ignore environmental infractions", "disregard toxic dumping"],
        "antonyms": ["crack down on environmental violations", "prosecute corporate polluters"]
    },
    "Champion the cause of conservation": {
        "synonyms": ["spearhead preservation initiatives", "advocate passionately for wildlife", "crusade for ecological integrity"],
        "antonyms": ["lobby for predatory exploitation", "undermine environmental treaties"]
    },
    "Trigger irreversible consequences": {
        "synonyms": ["induce unalterable fallout", "instigate permanent environmental harm", "set off irrevocable damage"],
        "antonyms": ["induce transient reversible shifts", "maintain manageable conditions"]
    },
    "Live in harmony with the ecosystem": {
        "synonyms": ["coexist symbiotically with nature", "lead a balanced ecological existence", "abide within planetary boundaries"],
        "antonyms": ["dominate and plunder natural ecosystems", "exploit nature destructively"]
    },
    "Drop in the ocean": {
        "synonyms": ["negligible contribution", "infinitesimal fraction", "trivial measure in context"],
        "antonyms": ["monumental impact", "decisive tipping factor"]
    },
    "Tip of the iceberg": {
        "synonyms": ["superficial fraction of an issue", "glimpse of a deeper crisis", "visible trace of vast trouble"],
        "antonyms": ["exhaustive totality", "full manifestation"]
    },
    "Double-edged sword": {
        "synonyms": ["mixed blessing", "paradoxical dilemma", "two-sided challenge"],
        "antonyms": ["unequivocal asset", "unmitigated boon"]
    },
    "Die out": {
        "synonyms": ["become extinct", "vanish permanently", "perish completely"],
        "antonyms": ["proliferate", "thrive", "flourish"]
    },
    "Wipe out": {
        "synonyms": ["eradicate", "obliterate", "annihilate", "decimate"],
        "antonyms": ["conserve", "cultivate", "shield"]
    },
    "Dry up": {
        "synonyms": ["desiccate", "evaporate completely", "run dry"],
        "antonyms": ["overflow", "flood", "replenish"]
    },
    "Clear out": {
        "synonyms": ["evacuate", "disgorge", "empty comprehensively"],
        "antonyms": ["clutter", "occupy", "fill"]
    },
    "Rely on": {
        "synonyms": ["depend upon", "lean upon", "be contingent on"],
        "antonyms": ["be self-reliant", "operate independently of"]
    },
    "Cut down on": {
        "synonyms": ["curtail consumption of", "scale back on", "diminish intake of"],
        "antonyms": ["expand consumption of", "escalate use of"]
    },
    "Burn up": {
        "synonyms": ["incinerate completely", "combust", "consume by fire"],
        "antonyms": ["extinguish", "quench", "smolder"]
    },
    "Run out of": {
        "synonyms": ["exhaust reserves of", "deplete supply of", "drain completely"],
        "antonyms": ["possess an abundance of", "replenish"]
    },
    "Foul up": {
        "synonyms": ["pollute badly", "bungle ecologically", "befoul carelessly"],
        "antonyms": ["sanitize", "rectify", "purify"]
    },
    "Scale back": {
        "synonyms": ["reduce incrementally", "taper off", "downsize operations"],
        "antonyms": ["ramp up", "accelerate", "expand"]
    },
    "Play with fire": {
        "synonyms": ["court ecological catastrophe", "gamble recklessly with nature", "take untenable risks"],
        "antonyms": ["exercise utmost caution", "act with prudent foresight"]
    },
    "Call for action": {
        "synonyms": ["demand intervention", "appeal for immediate measures", "exhort urgent reform"],
        "antonyms": ["counsel complacency", "advocate passive acquiescence"]
    },
    "Alarmingly": {
        "synonyms": ["disturbingly", "at a terrifying pace", "frighteningly"],
        "antonyms": ["reassuringly", "comfortingly", "tranquilly"]
    },
    "Disproportionately": {
        "synonyms": ["unevenly", "asymmetrically", "inordinately"],
        "antonyms": ["proportionately", "equitably", "evenly"]
    },
    "Irrevocably": {
        "synonyms": ["permanently", "irreversibly", "beyond recovery"],
        "antonyms": ["reversibly", "temporarily", "mutably"]
    },
    "Invariably": {
        "synonyms": ["consistently", "unfailingly", "without exception"],
        "antonyms": ["sporadically", "erratically", "infrequently"]
    },
    "Radically": {
        "synonyms": ["fundamentally", "profoundly", "drastically"],
        "antonyms": ["superficially", "marginally", "incrementally"]
    },
    "Catastrophically": {
        "synonyms": ["disastrously", "ruinously", "calamitously"],
        "antonyms": ["auspiciously", "constructively", "harmlessly"]
    },
    "Sustainably": {
        "synonyms": ["renewably", "without depleting resources", "ecologically"],
        "antonyms": ["unsustainably", "destructively", "wastefully"]
    },
    "Severely": {
        "synonyms": ["acutely", "gravely", "harshly", "drastically"],
        "antonyms": ["mildly", "moderately", "gently"]
    }
}

def update_environment():
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    updated = 0
    words = data.get("words", [])
    for w in words:
        name = w.get("word")
        if name in ENV_LEXICON:
            w["synonyms"] = ENV_LEXICON[name]["synonyms"]
            w["antonyms"] = ENV_LEXICON[name]["antonyms"]
            updated += 1
            
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully updated {updated} words in environment.json!")
    return updated

if __name__ == "__main__":
    update_environment()
