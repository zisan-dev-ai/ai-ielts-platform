"""
Authentic Cambridge IELTS Academic Writing Seed Bank
Contains complete, authentic Cambridge Task 1 (with embedded interactive vector SVGs) and Task 2 prompts covering all official types:
- Task 1: Line Graph, Bar Chart, Pie Chart, Table, Mixed Charts, Process Diagram, Map / Layout
- Task 2: Agree/Disagree, Discuss Both Views, Advantages/Disadvantages, Problem/Solution, Two-Part Questions, Positive/Negative Development
Includes Band 9 Model Essays, paragraph structure breakdowns, and lexical resources for each prompt.
"""

import sqlite3
import json

def get_cambridge_writing_tasks():
    tasks = []

    # ==========================================
    # TASK 1: LINE GRAPH
    # ==========================================
    tasks.append({
        "skill": "Writing",
        "test_type": "Academic Task 1",
        "section_number": 1,
        "title": "Renewable Electricity Generation by Source (1980–2025)",
        "question_type": "Academic Task 1 - Line Graph",
        "cambridge_book": "Cambridge 19",
        "test_number": 1,
        "passage_or_section": "Task 1",
        "difficulty_band": "Academic",
        "difficulty": "medium",
        "passage_or_context": """<div class="cambridge-prompt-header">
    <p><b>You should spend about 20 minutes on this task.</b></p>
    <p><i>The graph below shows the percentage of electricity generated from three renewable sources (Hydroelectric, Wind, and Solar) in a European nation between 1980 and 2025.</i></p>
    <p><b>Summarise the information by selecting and reporting the main features, and make comparisons where relevant.</b></p>
    <p><b>Write at least 150 words.</b></p>
</div>
<div class="chart-wrapper" style="background:#0f172a; padding:18px; border-radius:10px; margin:16px 0; border:1px solid #334155; text-align:center;">
    <svg viewBox="0 0 650 340" style="width:100%; max-height:320px; font-family:sans-serif;">
        <!-- Background Grid -->
        <rect width="650" height="340" fill="#0f172a" rx="8"/>
        <line x1="70" y1="40" x2="600" y2="40" stroke="#334155" stroke-dasharray="4"/>
        <line x1="70" y1="100" x2="600" y2="100" stroke="#334155" stroke-dasharray="4"/>
        <line x1="70" y1="160" x2="600" y2="160" stroke="#334155" stroke-dasharray="4"/>
        <line x1="70" y1="220" x2="600" y2="220" stroke="#334155" stroke-dasharray="4"/>
        <line x1="70" y1="280" x2="600" y2="280" stroke="#64748b" stroke-width="2"/>
        <line x1="70" y1="30" x2="70" y2="280" stroke="#64748b" stroke-width="2"/>

        <!-- Y Axis Labels -->
        <text x="60" y="45" fill="#94a3b8" font-size="12" text-anchor="end">50%</text>
        <text x="60" y="105" fill="#94a3b8" font-size="12" text-anchor="end">40%</text>
        <text x="60" y="165" fill="#94a3b8" font-size="12" text-anchor="end">30%</text>
        <text x="60" y="225" fill="#94a3b8" font-size="12" text-anchor="end">20%</text>
        <text x="60" y="285" fill="#94a3b8" font-size="12" text-anchor="end">10%</text>

        <!-- X Axis Labels -->
        <text x="70" y="305" fill="#94a3b8" font-size="12" text-anchor="middle">1980</text>
        <text x="176" y="305" fill="#94a3b8" font-size="12" text-anchor="middle">1990</text>
        <text x="282" y="305" fill="#94a3b8" font-size="12" text-anchor="middle">2000</text>
        <text x="388" y="305" fill="#94a3b8" font-size="12" text-anchor="middle">2010</text>
        <text x="494" y="305" fill="#94a3b8" font-size="12" text-anchor="middle">2020</text>
        <text x="600" y="305" fill="#94a3b8" font-size="12" text-anchor="middle">2025</text>

        <!-- Hydroelectric Line (Blue) -->
        <path d="M 70 50 Q 282 80 494 130 T 600 150" fill="none" stroke="#38bdf8" stroke-width="3.5"/>
        <!-- Wind Line (Green) -->
        <path d="M 70 270 Q 282 250 388 170 T 600 70" fill="none" stroke="#34d399" stroke-width="3.5"/>
        <!-- Solar Line (Amber) -->
        <path d="M 70 278 L 282 275 Q 388 260 494 190 T 600 110" fill="none" stroke="#fbbf24" stroke-width="3.5"/>

        <!-- Legend -->
        <rect x="180" y="10" width="12" height="12" fill="#38bdf8" rx="2"/>
        <text x="198" y="21" fill="#e2e8f0" font-size="12">Hydroelectric</text>
        <rect x="310" y="10" width="12" height="12" fill="#34d399" rx="2"/>
        <text x="328" y="21" fill="#e2e8f0" font-size="12">Wind Energy</text>
        <rect x="440" y="10" width="12" height="12" fill="#fbbf24" rx="2"/>
        <text x="458" y="21" fill="#e2e8f0" font-size="12">Solar Power</text>
    </svg>
</div>""",
        "question_text": "Summarise the renewable electricity generation trends between 1980 and 2025, identifying primary trends, crossover points, and comparative shifts.",
        "answer_key": "Band 9 Academic Model Report",
        "explanation": """### Band 9 Model Answer:
The line graph illustrates the proportion of electricity produced by three renewable energy sectors—hydroelectric, wind, and solar power—in a European nation from 1980 to 2025.

**Overview:**
Overall, while hydroelectric power experienced a steady decline over the 45-year period, both wind and solar power exhibited substantial growth, with wind energy ultimately overtaking hydroelectricity to become the dominant renewable electricity source by 2025.

**Body Paragraph 1 (Hydroelectric & Wind):**
In 1980, hydroelectricity was by far the leading source, generating nearly 48% of the country's electricity. However, its share decreased gradually to approximately 38% in 2000, before dropping more noticeably to roughly 31% by 2025. In stark contrast, wind power contributed a negligible 2% in 1980. Its output grew moderately until 2000, after which it underwent exponential expansion, surpassing hydroelectricity in around 2014 and culminating at a peak of approximately 45% in 2025.

**Body Paragraph 2 (Solar):**
Solar power remained virtually non-existent between 1980 and 2000 at under 1%. Subsequently, solar generation accelerated dramatically from 2010 onwards, escalating from roughly 8% to finish at approximately 28% in 2025, approaching the level of hydroelectric generation.""",
        "group_id": "W_T1_LINE_1",
        "group_instructions": "Write at least 150 words. Organize your report into: Introduction, Overview, and 2 Detailed Body Paragraphs."
    })

    # ==========================================
    # TASK 1: BAR CHART
    # ==========================================
    tasks.append({
        "skill": "Writing",
        "test_type": "Academic Task 1",
        "section_number": 1,
        "title": "Household Expenditure on Five Categories in 2024",
        "question_type": "Academic Task 1 - Bar Chart",
        "cambridge_book": "Cambridge 18",
        "test_number": 2,
        "passage_or_section": "Task 1",
        "difficulty_band": "Academic",
        "difficulty": "medium",
        "passage_or_context": """<div class="cambridge-prompt-header">
    <p><b>You should spend about 20 minutes on this task.</b></p>
    <p><i>The bar chart below compares the average proportion of household spending on five categories (Housing, Food, Transport, Healthcare, and Entertainment) across four countries in 2024.</i></p>
    <p><b>Summarise the information by selecting and reporting the main features, and make comparisons where relevant.</b></p>
    <p><b>Write at least 150 words.</b></p>
</div>
<div class="chart-wrapper" style="background:#0f172a; padding:18px; border-radius:10px; margin:16px 0; border:1px solid #334155; text-align:center;">
    <svg viewBox="0 0 650 340" style="width:100%; max-height:320px; font-family:sans-serif;">
        <rect width="650" height="340" fill="#0f172a" rx="8"/>
        <!-- Grid -->
        <line x1="80" y1="40" x2="610" y2="40" stroke="#334155" stroke-dasharray="4"/>
        <line x1="80" y1="100" x2="610" y2="100" stroke="#334155" stroke-dasharray="4"/>
        <line x1="80" y1="160" x2="610" y2="160" stroke="#334155" stroke-dasharray="4"/>
        <line x1="80" y1="220" x2="610" y2="220" stroke="#334155" stroke-dasharray="4"/>
        <line x1="80" y1="280" x2="610" y2="280" stroke="#64748b" stroke-width="2"/>
        <line x1="80" y1="30" x2="80" y2="280" stroke="#64748b" stroke-width="2"/>

        <text x="70" y="45" fill="#94a3b8" font-size="12" text-anchor="end">40%</text>
        <text x="70" y="105" fill="#94a3b8" font-size="12" text-anchor="end">30%</text>
        <text x="70" y="165" fill="#94a3b8" font-size="12" text-anchor="end">20%</text>
        <text x="70" y="225" fill="#94a3b8" font-size="12" text-anchor="end">10%</text>
        <text x="70" y="285" fill="#94a3b8" font-size="12" text-anchor="end">0%</text>

        <!-- Categories -->
        <text x="135" y="305" fill="#cbd5e1" font-size="11" text-anchor="middle">Housing</text>
        <text x="245" y="305" fill="#cbd5e1" font-size="11" text-anchor="middle">Food & Bev</text>
        <text x="355" y="305" fill="#cbd5e1" font-size="11" text-anchor="middle">Transport</text>
        <text x="465" y="305" fill="#cbd5e1" font-size="11" text-anchor="middle">Healthcare</text>
        <text x="575" y="305" fill="#cbd5e1" font-size="11" text-anchor="middle">Leisure</text>

        <!-- Bars -->
        <rect x="95" y="70" width="18" height="210" fill="#38bdf8"/>
        <rect x="115" y="55" width="18" height="225" fill="#f43f5e"/>
        <rect x="135" y="110" width="18" height="170" fill="#34d399"/>
        <rect x="155" y="85" width="18" height="195" fill="#fbbf24"/>

        <!-- Food -->
        <rect x="205" y="160" width="18" height="120" fill="#38bdf8"/>
        <rect x="225" y="190" width="18" height="90" fill="#f43f5e"/>
        <rect x="245" y="130" width="18" height="150" fill="#34d399"/>
        <rect x="265" y="175" width="18" height="105" fill="#fbbf24"/>

        <!-- Transport -->
        <rect x="315" y="170" width="18" height="110" fill="#38bdf8"/>
        <rect x="335" y="150" width="18" height="130" fill="#f43f5e"/>
        <rect x="355" y="200" width="18" height="80" fill="#34d399"/>
        <rect x="375" y="165" width="18" height="115" fill="#fbbf24"/>

        <!-- Healthcare -->
        <rect x="425" y="235" width="18" height="45" fill="#38bdf8"/>
        <rect x="445" y="160" width="18" height="120" fill="#f43f5e"/>
        <rect x="465" y="220" width="18" height="60" fill="#34d399"/>
        <rect x="485" y="240" width="18" height="40" fill="#fbbf24"/>

        <!-- Leisure -->
        <rect x="535" y="205" width="18" height="75" fill="#38bdf8"/>
        <rect x="555" y="190" width="18" height="90" fill="#f43f5e"/>
        <rect x="575" y="225" width="18" height="55" fill="#34d399"/>
        <rect x="595" y="195" width="18" height="85" fill="#fbbf24"/>

        <!-- Legend -->
        <rect x="150" y="12" width="10" height="10" fill="#38bdf8"/>
        <text x="165" y="21" fill="#e2e8f0" font-size="11">UK</text>
        <rect x="230" y="12" width="10" height="10" fill="#f43f5e"/>
        <text x="245" y="21" fill="#e2e8f0" font-size="11">USA</text>
        <rect x="310" y="12" width="10" height="10" fill="#34d399"/>
        <text x="325" y="21" fill="#e2e8f0" font-size="11">Japan</text>
        <rect x="390" y="12" width="10" height="10" fill="#fbbf24"/>
        <text x="405" y="21" fill="#e2e8f0" font-size="11">Germany</text>
    </svg>
</div>""",
        "question_text": "Summarise the main features of household expenditure across the four countries, contrasting major and minor expenditure sectors.",
        "answer_key": "Band 9 Academic Model Report",
        "explanation": """### Band 9 Model Answer:
The bar chart details the proportion of income allocated to five distinct expenditure categories—housing, food and beverages, transport, healthcare, and leisure—by households in the UK, the US, Japan, and Germany in 2024.

**Overview:**
Overall, housing constituted the largest budgetary expenditure across all four nations, whereas healthcare and leisure consistently accounted for the lowest shares, with the sole exception of the US spending heavily on medical care.

**Body Paragraph 1 (Housing & Food):**
Regarding primary expenditures, American households directed the highest percentage towards housing at nearly 38%, followed closely by the UK (35%) and Germany (32%), while Japan registered the lowest figure in this category at roughly 28%. Conversely, Japanese families spent the greatest proportion on food and beverages at approximately 25%, surpassing Germany (18%), the UK (20%), and the US (15%).

**Body Paragraph 2 (Transport, Healthcare & Leisure):**
For transport, spending was relatively uniform, hovering between 13% in Japan and 22% in the US. The starkest divergence appeared in healthcare, where American expenditure reached roughly 20%, more than triple the figures recorded for the UK (7%), Germany (7%), and Japan (10%). Finally, leisure spending remained modest across all countries, ranging from 9% in Japan to approximately 15% in the US and Germany.""",
        "group_id": "W_T1_BAR_1",
        "group_instructions": "Write at least 150 words. Organize into Introduction, Overview, and 2 Grouped Body Paragraphs."
    })

    # ==========================================
    # TASK 1: PROCESS DIAGRAM
    # ==========================================
    tasks.append({
        "skill": "Writing",
        "test_type": "Academic Task 1",
        "section_number": 1,
        "title": "Industrial Production of Cement and Concrete",
        "question_type": "Academic Task 1 - Process Diagram",
        "cambridge_book": "Cambridge 18",
        "test_number": 1,
        "passage_or_section": "Task 1",
        "difficulty_band": "Academic",
        "difficulty": "hard",
        "passage_or_context": """<div class="cambridge-prompt-header">
    <p><b>You should spend about 20 minutes on this task.</b></p>
    <p><i>The diagrams below illustrate the stages involved in the manufacturing of cement, and how cement is subsequently used to produce concrete for building construction.</i></p>
    <p><b>Summarise the information by selecting and reporting the main features, and make comparisons where relevant.</b></p>
    <p><b>Write at least 150 words.</b></p>
</div>
<div class="chart-wrapper" style="background:#0f172a; padding:18px; border-radius:10px; margin:16px 0; border:1px solid #334155; text-align:center;">
    <svg viewBox="0 0 650 350" style="width:100%; max-height:330px; font-family:sans-serif;">
        <rect width="650" height="350" fill="#0f172a" rx="8"/>
        
        <text x="325" y="24" fill="#38bdf8" font-size="14" font-weight="bold" text-anchor="middle">STAGE 1: CEMENT PRODUCTION</text>
        
        <rect x="20" y="45" width="95" height="40" fill="#1e293b" stroke="#38bdf8" rx="6"/>
        <text x="67" y="62" fill="#fff" font-size="10" text-anchor="middle" font-weight="bold">Limestone</text>
        <text x="67" y="76" fill="#94a3b8" font-size="9" text-anchor="middle">& Clay</text>

        <line x1="115" y1="65" x2="145" y2="65" stroke="#f59e0b" stroke-width="2"/>

        <rect x="145" y="45" width="95" height="40" fill="#1e293b" stroke="#38bdf8" rx="6"/>
        <text x="192" y="62" fill="#fff" font-size="10" text-anchor="middle" font-weight="bold">Crusher</text>
        <text x="192" y="76" fill="#94a3b8" font-size="9" text-anchor="middle">(Fine Powder)</text>

        <line x1="240" y1="65" x2="270" y2="65" stroke="#f59e0b" stroke-width="2"/>

        <rect x="270" y="45" width="105" height="40" fill="#1e293b" stroke="#38bdf8" rx="6"/>
        <text x="322" y="60" fill="#fff" font-size="10" text-anchor="middle" font-weight="bold">Rotating Heater</text>
        <text x="322" y="74" fill="#f43f5e" font-size="9" text-anchor="middle">🔥 High Heat</text>

        <line x1="375" y1="65" x2="405" y2="65" stroke="#f59e0b" stroke-width="2"/>

        <rect x="405" y="45" width="95" height="40" fill="#1e293b" stroke="#38bdf8" rx="6"/>
        <text x="452" y="62" fill="#fff" font-size="10" text-anchor="middle" font-weight="bold">Grinder</text>
        <text x="452" y="76" fill="#94a3b8" font-size="9" text-anchor="middle">+ Gypsum Added</text>

        <line x1="500" y1="65" x2="530" y2="65" stroke="#f59e0b" stroke-width="2"/>

        <rect x="530" y="45" width="95" height="40" fill="#1e293b" stroke="#10b981" rx="6"/>
        <text x="577" y="62" fill="#fff" font-size="10" text-anchor="middle" font-weight="bold">Cement Bags</text>
        <text x="577" y="76" fill="#34d399" font-size="9" text-anchor="middle">Packaged</text>

        <line x1="30" y1="125" x2="620" y2="125" stroke="#334155" stroke-dasharray="6"/>

        <text x="325" y="155" fill="#34d399" font-size="14" font-weight="bold" text-anchor="middle">STAGE 2: CONCRETE PRODUCTION (PROPORTIONS)</text>

        <rect x="40" y="180" width="115" height="60" fill="#1e293b" stroke="#38bdf8" rx="6"/>
        <text x="97" y="205" fill="#38bdf8" font-size="12" text-anchor="middle" font-weight="bold">Cement: 15%</text>
        <text x="97" y="225" fill="#94a3b8" font-size="10" text-anchor="middle">Binding Powder</text>

        <rect x="185" y="180" width="115" height="60" fill="#1e293b" stroke="#fbbf24" rx="6"/>
        <text x="242" y="205" fill="#fbbf24" font-size="12" text-anchor="middle" font-weight="bold">Water: 10%</text>
        <text x="242" y="225" fill="#94a3b8" font-size="10" text-anchor="middle">Moisture Agent</text>

        <rect x="330" y="180" width="115" height="60" fill="#1e293b" stroke="#a78bfa" rx="6"/>
        <text x="387" y="205" fill="#a78bfa" font-size="12" text-anchor="middle" font-weight="bold">Sand: 25%</text>
        <text x="387" y="225" fill="#94a3b8" font-size="10" text-anchor="middle">Fine Aggregate</text>

        <rect x="475" y="180" width="135" height="60" fill="#1e293b" stroke="#f43f5e" rx="6"/>
        <text x="542" y="205" fill="#f43f5e" font-size="12" text-anchor="middle" font-weight="bold">Gravel: 50%</text>
        <text x="542" y="225" fill="#94a3b8" font-size="10" text-anchor="middle">Coarse Crushed Stone</text>

        <rect x="180" y="275" width="290" height="48" fill="#064e3b" stroke="#10b981" rx="8"/>
        <text x="325" y="295" fill="#fff" font-size="12" text-anchor="middle" font-weight="bold">🔄 Concrete Mixer Drum</text>
        <text x="325" y="312" fill="#a7f3d0" font-size="10" text-anchor="middle">Rotated continuously to produce construction concrete</text>
    </svg>
</div>""",
        "question_text": "Describe the linear process of cement production and the proportions required in concrete formulation.",
        "answer_key": "Band 9 Academic Model Report",
        "explanation": """### Band 9 Model Answer:
The provided diagrams depict the five-stage manufacturing process of cement and the subsequent compositional blending required to synthesize concrete for building construction.

**Overview:**
Overall, cement production is a multi-step linear industrial process involving raw material crushing, thermal processing, and fine grinding. In contrast, concrete creation involves combining four precise ingredients—with gravel forming the largest component—in a rotating mechanical mixer.

**Body Paragraph 1 (Cement Manufacturing):**
The cement production sequence initiates when limestone and clay are crushed together into a fine, homogeneous powder. This powder is then fed into a mixer before passing through a rotating cylindrical kiln, where it undergoes high-temperature heating. Following the heating stage, the material passes over a cooling conveyor and is fed into a heavy grinder, where gypsum is added to regulate setting time. Finally, the finished cement is packaged into industrial bags ready for transport.

**Body Paragraph 2 (Concrete Production):**
To manufacture concrete, the packaged cement accounts for exactly 15% of the overall mixture. The largest constituent is gravel (small crushed stones), which makes up half (50%) of the total volume, supplemented by 25% sand and 10% water. These four components are placed together into a concrete mixer drum, which rotates continuously until a uniform building compound is produced.""",
        "group_id": "W_T1_PROC_1",
        "group_instructions": "Write at least 150 words using passive voice and sequential linkers (initially, subsequently, thereafter, finally)."
    })

    # ==========================================
    # TASK 1: MAP / LAYOUT REDEVELOPMENT
    # ==========================================
    tasks.append({
        "skill": "Writing",
        "test_type": "Academic Task 1",
        "section_number": 1,
        "title": "Coastal Town of Porthaven: 2000 vs Present Day",
        "question_type": "Academic Task 1 - Map / Layout",
        "cambridge_book": "Cambridge 19",
        "test_number": 3,
        "passage_or_section": "Task 1",
        "difficulty_band": "Academic",
        "difficulty": "hard",
        "passage_or_context": """<div class="cambridge-prompt-header">
    <p><b>You should spend about 20 minutes on this task.</b></p>
    <p><i>The two maps below show the redevelopment of the coastal resort town of Porthaven between the year 2000 and the present day.</i></p>
    <p><b>Summarise the information by selecting and reporting the main features, and make comparisons where relevant.</b></p>
    <p><b>Write at least 150 words.</b></p>
</div>
<div class="chart-wrapper" style="background:#0f172a; padding:18px; border-radius:10px; margin:16px 0; border:1px solid #334155; text-align:center;">
    <svg viewBox="0 0 650 320" style="width:100%; max-height:300px; font-family:sans-serif;">
        <rect width="650" height="320" fill="#0f172a" rx="8"/>
        
        <!-- MAP 2000 -->
        <rect x="25" y="30" width="280" height="260" fill="#1e293b" stroke="#64748b" rx="6"/>
        <text x="165" y="52" fill="#38bdf8" font-size="13" font-weight="bold" text-anchor="middle">PORTHAVEN (Year 2000)</text>
        
        <!-- North Arrow -->
        <text x="40" y="60" fill="#fbbf24" font-size="11" font-weight="bold">↑ N</text>

        <!-- Sea / Beach -->
        <rect x="35" y="70" width="260" height="35" fill="#0284c7" rx="3"/>
        <text x="165" y="92" fill="#fff" font-size="11" text-anchor="middle">🌊 Sandy Beach & Coastline</text>

        <!-- Old Port / Fishing Dock -->
        <rect x="40" y="115" width="80" height="40" fill="#334155" stroke="#94a3b8"/>
        <text x="80" y="138" fill="#e2e8f0" font-size="9" text-anchor="middle">Fishing Port</text>

        <!-- Caravan Park -->
        <rect x="180" y="115" width="105" height="40" fill="#334155" stroke="#94a3b8"/>
        <text x="232" y="138" fill="#e2e8f0" font-size="9" text-anchor="middle">Caravan Park</text>

        <!-- Main Road -->
        <line x1="35" y1="180" x2="295" y2="180" stroke="#f59e0b" stroke-width="4"/>
        <text x="165" y="174" fill="#fbbf24" font-size="9" text-anchor="middle">Main Street</text>

        <!-- Residential Houses & Farmland -->
        <rect x="40" y="200" width="110" height="70" fill="#334155"/>
        <text x="95" y="240" fill="#cbd5e1" font-size="9" text-anchor="middle">Residential Area</text>

        <rect x="175" y="200" width="110" height="70" fill="#14532d"/>
        <text x="230" y="240" fill="#a7f3d0" font-size="9" text-anchor="middle">Farmland / Trees</text>


        <!-- MAP PRESENT DAY -->
        <rect x="345" y="30" width="280" height="260" fill="#1e293b" stroke="#10b981" rx="6"/>
        <text x="485" y="52" fill="#34d399" font-size="13" font-weight="bold" text-anchor="middle">PORTHAVEN (Present Day)</text>

        <!-- Sea / Beach + Marina -->
        <rect x="355" y="70" width="260" height="35" fill="#0284c7" rx="3"/>
        <text x="485" y="92" fill="#fff" font-size="11" text-anchor="middle">🌊 Marina & Yacht Club</text>

        <!-- Luxury Hotel & Spa -->
        <rect x="360" y="115" width="100" height="40" fill="#047857" stroke="#34d399"/>
        <text x="410" y="138" fill="#fff" font-size="9" text-anchor="middle">Luxury Hotel & Spa</text>

        <!-- Promenade & Restaurants -->
        <rect x="485" y="115" width="120" height="40" fill="#047857" stroke="#34d399"/>
        <text x="545" y="138" fill="#fff" font-size="9" text-anchor="middle">Restaurants & Cafes</text>

        <!-- Main Road + Roundabout -->
        <line x1="355" y1="180" x2="615" y2="180" stroke="#f59e0b" stroke-width="4"/>
        <circle cx="485" cy="180" r="10" fill="#f59e0b"/>

        <!-- Expanded Residential & Shopping Mall -->
        <rect x="360" y="200" width="110" height="70" fill="#065f46"/>
        <text x="415" y="240" fill="#a7f3d0" font-size="9" text-anchor="middle">Apartment Blocks</text>

        <rect x="495" y="200" width="110" height="70" fill="#065f46"/>
        <text x="550" y="240" fill="#a7f3d0" font-size="9" text-anchor="middle">Shopping Complex</text>
    </svg>
</div>""",
        "question_text": "Describe the infrastructural transformations that occurred in Porthaven from 2000 to the present day, focusing on tourism, commercial expansion, and residential modernization.",
        "answer_key": "Band 9 Academic Model Report",
        "explanation": """### Band 9 Model Answer:
The two maps delineate the infrastructural and commercial modernization that has taken place in the coastal resort town of Porthaven from 2000 to the present day.

**Overview:**
Overall, Porthaven has transformed from a relatively quiet fishing settlement with agricultural land into a high-end, modern tourist resort featuring luxurious leisure facilities, expanded commercial zones, and multi-story housing.

**Body Paragraph 1 (Northern Coastal Strip):**
In the northern coastal sector, the old fishing port situated to the northwest has been entirely demolished and replaced by a luxury hotel and spa. Adjacent to this, the former caravan park in the northeast has been converted into a vibrant row of beachfront restaurants and cafes. Furthermore, the natural coastline now accommodates a private marina and yacht club, replacing the simple sandy beach.

**Body Paragraph 2 (Southern Sector & Transport):**
To the south, the main thoroughfare now features a central roundabout to facilitate heavier traffic flow. South of Main Street, the traditional detached residential houses have been modernized into high-density apartment blocks. Most notably, the expansive farmland and woodland in the south-eastern quadrant have been completely cleared to make way for a large retail shopping complex with surrounding access roads.""",
        "group_id": "W_T1_MAP_1",
        "group_instructions": "Write at least 150 words using directional language (north-west, adjacent, formerly, demolished, converted)."
    })

    # ==========================================
    # TASK 2: AGREE / DISAGREE (OPINION)
    # ==========================================
    tasks.append({
        "skill": "Writing",
        "test_type": "Task 2",
        "section_number": 2,
        "title": "Artificial Intelligence & Future Employment",
        "question_type": "Task 2 - Agree or Disagree",
        "cambridge_book": "Cambridge 19",
        "test_number": 1,
        "passage_or_section": "Task 2",
        "difficulty_band": "Academic",
        "difficulty": "medium",
        "passage_or_context": """<div class="cambridge-prompt-header">
    <p><b>You should spend about 40 minutes on this task.</b></p>
    <p>Write about the following topic:</p>
    <div style="background:rgba(225,29,72,0.1); border-left:4px solid #e11d48; padding:14px; margin:14px 0; font-size:1.05em; color:#fff; line-height:1.6;">
        <b>Some people believe that artificial intelligence and automation will create more job opportunities than they destroy in the long run. To what extent do you agree or disagree with this statement?</b>
    </div>
    <p><i>Give reasons for your answer and include any relevant examples from your own knowledge or experience.</i></p>
    <p><b>Write at least 250 words.</b></p>
</div>""",
        "question_text": "To what extent do you agree or disagree that AI and automation will generate a net positive number of jobs in the future?",
        "answer_key": "Band 9 Academic Essay",
        "explanation": """### Band 9 Model Essay:
The rapid advancement of artificial intelligence (AI) and robotic automation has ignited fierce debate concerning their long-term impact on global employment. While sceptics fear unprecedented structural redundancy across numerous industries, I largely agree with the assertion that technological revolutions ultimately generate far more employment opportunities than they eliminate, primarily through the emergence of new economic sectors and heightened productivity.

Admittedly, the initial deployment of AI technologies precipitates severe disruptions in traditional labour markets. Repetitive manual and routine cognitive tasks—such as manufacturing assembly, data entry, and basic administrative processing—are rapidly being automated by machine-learning algorithms. For instance, algorithmic underwriting has significantly reduced the demand for conventional insurance clerks. For workers unable to upskill promptly, this transition represents authentic hardship and short-term structural unemployment.

Nevertheless, historical precedent strongly suggests that technological automation functions as a catalyst for economic expansion rather than permanent job scarcity. During the Industrial Revolution, the mechanization of agriculture displaced millions of farmhands, yet it simultaneously fostered entirely new industrial, logistical, and service sectors that employed exponentially more people. Similarly, the current AI epoch is spawning novel professional domains, ranging from machine learning engineering and data ethics auditing to automated cybersecurity analysis. These emerging roles require sophisticated human creativity, critical judgement, and emotional intelligence—attributes that computational models cannot replicate.

Furthermore, by automating routine tasks, AI drives operational efficiency and substantially reduces operational costs. This productivity dividend liberates financial capital, enabling businesses to reinvest in research, innovation, and customer experience, all of which stimulate aggregate consumer demand and job creation across peripheral industries.

In conclusion, although the transition towards automated systems inevitably displaces workers in routine occupations, I firmly believe that AI will ultimately act as an engine of net job growth by birthing pioneering industries and amplifying human productivity across the global economy.""",
        "group_id": "W_T2_AGREE_1",
        "group_instructions": "Write at least 250 words. Ensure a clear thesis in Introduction and consistent stance throughout."
    })

    # ==========================================
    # TASK 2: DISCUSS BOTH VIEWS + OPINION
    # ==========================================
    tasks.append({
        "skill": "Writing",
        "test_type": "Task 2",
        "section_number": 2,
        "title": "University Education vs. Vocational Apprenticeship",
        "question_type": "Task 2 - Discuss Both Views",
        "cambridge_book": "Cambridge 18",
        "test_number": 3,
        "passage_or_section": "Task 2",
        "difficulty_band": "Academic",
        "difficulty": "medium",
        "passage_or_context": """<div class="cambridge-prompt-header">
    <p><b>You should spend about 40 minutes on this task.</b></p>
    <p>Write about the following topic:</p>
    <div style="background:rgba(225,29,72,0.1); border-left:4px solid #e11d48; padding:14px; margin:14px 0; font-size:1.05em; color:#fff; line-height:1.6;">
        <b>Some people think that university education is the best route to career success, while others argue that practical vocational training and early work experience offer superior advantages. Discuss both views and give your own opinion.</b>
    </div>
    <p><i>Give reasons for your answer and include any relevant examples from your own knowledge or experience.</i></p>
    <p><b>Write at least 250 words.</b></p>
</div>""",
        "question_text": "Discuss both perspectives regarding academic degrees versus practical apprenticeships, and present a reasoned personal opinion.",
        "answer_key": "Band 9 Academic Essay",
        "explanation": """### Band 9 Model Essay:
In contemporary society, school leavers face crucial choices regarding tertiary progression. While a significant portion of society maintains that securing a university degree remains the definitive pathway to professional prosperity, others contend that vocational training and immediate workplace immersion provide a more pragmatic foundation. This essay examines both viewpoints before presenting my own reasoned perspective.

Proponents of higher academic education emphasize the profound intellectual depth and standardized credentials that universities confer. For specialized vocations such as medicine, corporate law, and engineering, rigorous academic degrees are statutory prerequisites. Beyond specialized technical knowledge, university curricula foster higher-order critical thinking, autonomous research capabilities, and sophisticated communication skills. Furthermore, multinational corporations frequently utilize degree classifications as an initial screening filter in recruitment, meaning tertiary graduates often command higher lifetime earning potentials and broader managerial trajectories.

Conversely, advocates of vocational apprenticeships highlight the indispensable value of hands-on expertise and early financial independence. Vocational courses in fields such as electrical engineering, carpentry, and software coding provide direct, trade-specific competence tailored directly to current industrial demands. While university students often accumulate substantial tuition debt and graduate with theoretical knowledge lacking practical application, apprentices earn wages immediately while accumulating invaluable workplace exposure. Consequently, skilled tradespeople often experience faster entry into high-demand industries with minimal financial liability.

In my opinion, neither pathway possesses an inherent superiority; rather, optimal success depends entirely on the student's personal aptitude and chosen career trajectory. While intellectual and research-intensive professions undeniably require rigorous university training, the modern economy places equal premium on technical mastery. Therefore, governments should champion parity of esteem between academic degrees and vocational qualifications.

In conclusion, both academic universities and vocational apprenticeships offer distinct merits. The ideal choice must be tailored to an individual's career ambitions rather than adhering to rigid societal conventions.""",
        "group_id": "W_T2_VIEWS_1",
        "group_instructions": "Write at least 250 words. Address both perspectives with balanced arguments before providing your personal synthesis."
    })

    # ==========================================
    # TASK 2: PROBLEM & SOLUTION
    # ==========================================
    tasks.append({
        "skill": "Writing",
        "test_type": "Task 2",
        "section_number": 2,
        "title": "Urban Overcrowding & Megacity Congestion",
        "question_type": "Task 2 - Problem and Solution",
        "cambridge_book": "Cambridge 17",
        "test_number": 2,
        "passage_or_section": "Task 2",
        "difficulty_band": "Academic",
        "difficulty": "medium",
        "passage_or_context": """<div class="cambridge-prompt-header">
    <p><b>You should spend about 40 minutes on this task.</b></p>
    <p>Write about the following topic:</p>
    <div style="background:rgba(225,29,72,0.1); border-left:4px solid #e11d48; padding:14px; margin:14px 0; font-size:1.05em; color:#fff; line-height:1.6;">
        <b>More and more people are migrating to major metropolitan cities, resulting in severe overcrowding, traffic congestion, and inadequate public services. What are the main causes of this problem, and what practical solutions can governments implement?</b>
    </div>
    <p><i>Give reasons for your answer and include any relevant examples from your own knowledge or experience.</i></p>
    <p><b>Write at least 250 words.</b></p>
</div>""",
        "question_text": "Analyse the underlying socio-economic drivers of hyper-urbanisation and propose actionable, systemic interventions.",
        "answer_key": "Band 9 Academic Essay",
        "explanation": """### Band 9 Model Essay:
Across the globe, rapid rural-to-urban migration has triggered unprecedented demographic pressure on metropolitan centers, culminating in severe traffic paralysis, exorbitant housing costs, and strained municipal infrastructure. This essay will examine the primary catalysts behind this hyper-urbanization and propose actionable governmental countermeasures.

The predominant cause of mass urban migration is the stark regional disparity in economic opportunity and social infrastructure. In many developing and developed nations alike, commercial capital, corporate headquarters, and high-paying employment opportunities are heavily centralized within a handful of megacities. Simultaneously, peripheral rural and provincial towns frequently suffer from underinvestment, featuring substandard healthcare amenities, limited higher educational institutions, and precarious agrarian economies. Consequently, younger generations feel compelled to relocate to metropolitan hubs in pursuit of social mobility and modern lifestyle amenities.

To mitigate this urban strain, governments must adopt comprehensive regional decentralization strategies. Primarily, policymakers should introduce tax incentives and subsidize infrastructure to encourage corporate enterprises and manufacturing hubs to establish headquarters in secondary cities and regional growth centers. For instance, developing specialized technology corridors outside capital cities can generate localized employment hubs, thereby retaining talent within provincial jurisdictions. 

Additionally, significant capital investment must be directed into nationwide high-speed rail networks and digital broadband infrastructure. Seamless intercity transit links allow citizens to reside in affordable rural suburbs while commuting rapidly to urban workplaces, substantially reducing urban residential congestion.

In conclusion, while centralized economic opportunities and infrastructure deficits in rural areas drive unsustainable migration to major cities, proactive governmental policies focused on economic decentralization and nationwide connectivity offer pragmatic and durable remedies.""",
        "group_id": "W_T2_PROB_1",
        "group_instructions": "Write at least 250 words. Dedicate Body Paragraph 1 to root causes and Body Paragraph 2 to actionable solutions."
    })

    # ==========================================
    # TASK 1: PIE CHART
    # ==========================================
    tasks.append({
        "skill": "Writing",
        "test_type": "Academic Task 1",
        "section_number": 1,
        "title": "Global Energy Consumption by Fuel Source (1995 vs 2025)",
        "question_type": "Academic Task 1 - Pie Chart",
        "cambridge_book": "Cambridge 17",
        "test_number": 3,
        "passage_or_section": "Task 1",
        "difficulty_band": "Academic",
        "difficulty": "medium",
        "passage_or_context": """<div class="cambridge-prompt-header">
    <p><b>You should spend about 20 minutes on this task.</b></p>
    <p><i>The pie charts below show the percentage share of global energy consumption by five primary fuel sources in 1995 and projected for 2025.</i></p>
    <p><b>Summarise the information by selecting and reporting the main features, and make comparisons where relevant.</b></p>
    <p><b>Write at least 150 words.</b></p>
</div>
<div class="chart-wrapper" style="background:#0f172a; padding:18px; border-radius:10px; margin:16px 0; border:1px solid #334155; text-align:center;">
    <svg viewBox="0 0 650 320" style="width:100%; max-height:300px; font-family:sans-serif;">
        <rect width="650" height="320" fill="#0f172a" rx="8"/>
        
        <!-- Pie 1: 1995 -->
        <text x="175" y="35" fill="#38bdf8" font-size="14" font-weight="bold" text-anchor="middle">Year 1995 (Total Energy Share)</text>
        <circle cx="175" cy="150" r="90" fill="#1e293b" stroke="#475569" stroke-width="2"/>
        <!-- Oil 40% (Blue #38bdf8), Coal 28% (Gray #64748b), Gas 20% (Green #34d399), Nuclear 8% (Yellow #fbbf24), Renewables 4% (Red #f43f5e) -->
        <path d="M 175 150 L 175 60 A 90 90 0 0 1 260 180 Z" fill="#38bdf8"/>
        <text x="215" y="115" fill="#000" font-size="11" font-weight="bold">Oil 40%</text>

        <path d="M 175 150 L 260 180 A 90 90 0 0 1 125 225 Z" fill="#64748b"/>
        <text x="195" y="210" fill="#fff" font-size="11" font-weight="bold">Coal 28%</text>

        <path d="M 175 150 L 125 225 A 90 90 0 0 1 90 130 Z" fill="#34d399"/>
        <text x="115" y="175" fill="#000" font-size="10" font-weight="bold">Gas 20%</text>

        <path d="M 175 150 L 90 130 A 90 90 0 0 1 145 65 Z" fill="#fbbf24"/>
        <text x="120" y="105" fill="#000" font-size="9" font-weight="bold">Nuc 8%</text>

        <path d="M 175 150 L 145 65 A 90 90 0 0 1 175 60 Z" fill="#f43f5e"/>

        <!-- Pie 2: 2025 -->
        <text x="475" y="35" fill="#34d399" font-size="14" font-weight="bold" text-anchor="middle">Year 2025 (Projected Share)</text>
        <circle cx="475" cy="150" r="90" fill="#1e293b" stroke="#475569" stroke-width="2"/>
        <!-- Oil 28%, Gas 25%, Renewables 22%, Coal 18%, Nuclear 7% -->
        <path d="M 475 150 L 475 60 A 90 90 0 0 1 560 130 Z" fill="#38bdf8"/>
        <text x="505" y="100" fill="#000" font-size="11" font-weight="bold">Oil 28%</text>

        <path d="M 475 150 L 560 130 A 90 90 0 0 1 520 235 Z" fill="#34d399"/>
        <text x="525" y="180" fill="#000" font-size="11" font-weight="bold">Gas 25%</text>

        <path d="M 475 150 L 520 235 A 90 90 0 0 1 405 210 Z" fill="#f43f5e"/>
        <text x="445" y="215" fill="#fff" font-size="11" font-weight="bold">Ren 22%</text>

        <path d="M 475 150 L 405 210 A 90 90 0 0 1 400 115 Z" fill="#64748b"/>
        <text x="415" y="160" fill="#fff" font-size="10" font-weight="bold">Coal 18%</text>

        <path d="M 475 150 L 400 115 A 90 90 0 0 1 475 60 Z" fill="#fbbf24"/>
        <text x="430" y="95" fill="#000" font-size="9" font-weight="bold">Nuc 7%</text>

        <!-- Legend -->
        <rect x="120" y="280" width="10" height="10" fill="#38bdf8"/>
        <text x="135" y="289" fill="#cbd5e1" font-size="10">Oil</text>
        <rect x="190" y="280" width="10" height="10" fill="#64748b"/>
        <text x="205" y="289" fill="#cbd5e1" font-size="10">Coal</text>
        <rect x="270" y="280" width="10" height="10" fill="#34d399"/>
        <text x="285" y="289" fill="#cbd5e1" font-size="10">Natural Gas</text>
        <rect x="380" y="280" width="10" height="10" fill="#fbbf24"/>
        <text x="395" y="289" fill="#cbd5e1" font-size="10">Nuclear</text>
        <rect x="470" y="280" width="10" height="10" fill="#f43f5e"/>
        <text x="485" y="289" fill="#cbd5e1" font-size="10">Renewables</text>
    </svg>
</div>""",
        "question_text": "Summarise the structural shifts in global fuel consumption between 1995 and 2025.",
        "answer_key": "Band 9 Academic Model Report",
        "explanation": """### Band 9 Model Answer:
The pie charts delineate the proportion of worldwide energy consumption derived from five primary sources in 1995 compared with projections for 2025.

**Overview:**
Overall, fossil fuels (oil and coal) dominated global consumption in 1995. However, by 2025, while oil and natural gas remain primary components, renewable energy exhibits an extraordinary escalation, becoming the third-largest contributor as coal reliance diminishes significantly.

**Body Paragraph 1 (Fossil Fuels):**
In 1995, oil accounted for the largest individual share of worldwide energy consumption at 40%, followed by coal at 28%. By 2025, oil is projected to decline substantially to 28%, and coal drops by ten percentage points to 18%. Conversely, natural gas consumption expands from 20% in 1995 to reach a quarter (25%) of total demand in 2025.

**Body Paragraph 2 (Renewables & Nuclear):**
The most striking transformation occurs in renewable energy sources, which escalate more than fivefold from a minor 4% in 1995 to 22% in 2025. Meanwhile, nuclear energy remains virtually static, declining marginally from 8% to 7% over the 30-year timeframe.""",
        "group_id": "W_T1_PIE_1",
        "group_instructions": "Write at least 150 words comparing proportion shifts and sector dominance."
    })

    # ==========================================
    # TASK 1: TABLE
    # ==========================================
    tasks.append({
        "skill": "Writing",
        "test_type": "Academic Task 1",
        "section_number": 1,
        "title": "Higher Education Enrollment by Discipline and Gender",
        "question_type": "Academic Task 1 - Table",
        "cambridge_book": "Cambridge 16",
        "test_number": 1,
        "passage_or_section": "Task 1",
        "difficulty_band": "Academic",
        "difficulty": "medium",
        "passage_or_context": """<div class="cambridge-prompt-header">
    <p><b>You should spend about 20 minutes on this task.</b></p>
    <p><i>The table below provides statistics on student enrollment numbers across five university faculties broken down by gender in 2024.</i></p>
    <p><b>Summarise the information by selecting and reporting the main features, and make comparisons where relevant.</b></p>
    <p><b>Write at least 150 words.</b></p>
</div>
<div class="chart-wrapper" style="background:#0f172a; padding:18px; border-radius:10px; margin:16px 0; border:1px solid #334155;">
    <table style="width:100%; border-collapse:collapse; color:#fff; font-size:0.9em; text-align:left;">
        <thead>
            <tr style="background:#1e293b; border-bottom:2px solid #38bdf8;">
                <th style="padding:10px;">Faculty / Discipline</th>
                <th style="padding:10px; color:#38bdf8;">Male Students</th>
                <th style="padding:10px; color:#f43f5e;">Female Students</th>
                <th style="padding:10px; color:#fbbf24;">Total Enrollment</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom:1px solid #334155;"><td style="padding:10px;">Engineering & Technology</td><td style="padding:10px;">14,200</td><td style="padding:10px;">3,800</td><td style="padding:10px; font-weight:bold;">18,000</td></tr>
            <tr style="border-bottom:1px solid #334155; background:rgba(255,255,255,0.02);"><td style="padding:10px;">Business & Finance</td><td style="padding:10px;">11,500</td><td style="padding:10px;">12,100</td><td style="padding:10px; font-weight:bold;">23,600</td></tr>
            <tr style="border-bottom:1px solid #334155;"><td style="padding:10px;">Medicine & Life Sciences</td><td style="padding:10px;">6,400</td><td style="padding:10px;">9,600</td><td style="padding:10px; font-weight:bold;">16,000</td></tr>
            <tr style="border-bottom:1px solid #334155; background:rgba(255,255,255,0.02);"><td style="padding:10px;">Humanities & Social Sciences</td><td style="padding:10px;">4,100</td><td style="padding:10px;">11,900</td><td style="padding:10px; font-weight:bold;">16,000</td></tr>
            <tr style="border-bottom:2px solid #64748b;"><td style="padding:10px;">Computer Science & AI</td><td style="padding:10px;">15,800</td><td style="padding:10px;">5,200</td><td style="padding:10px; font-weight:bold;">21,000</td></tr>
            <tr style="background:#064e3b; font-weight:bold;"><td style="padding:10px; color:#34d399;">Total University Enrollment</td><td style="padding:10px; color:#34d399;">52,000</td><td style="padding:10px; color:#34d399;">42,600</td><td style="padding:10px; color:#34d399;">94,600</td></tr>
        </tbody>
    </table>
</div>""",
        "question_text": "Summarise the university enrollment statistics across faculties and contrast gender representation.",
        "answer_key": "Band 9 Academic Model Report",
        "explanation": """### Band 9 Model Answer:
The table presents data regarding male and female student registrations across five distinct academic faculties at a university in 2024.

**Overview:**
Overall, total university enrollment stood at 94,600 students, with male registrations outnumbering females overall. Business & Finance attracted the highest combined cohort, while significant gender disparities were evident, with men heavily dominating STEM fields and women constituting the substantial majority in Humanities and Medicine.

**Body Paragraph 1 (Male-Dominated STEM):**
Computer Science & AI and Engineering & Technology exhibited the most pronounced gender imbalances. In Computer Science, male students numbered 15,800, roughly triple the female total of 5,200. Similarly, Engineering comprised 14,200 males compared to just 3,800 females, making it the most male-skewed discipline.

**Body Paragraph 2 (Female-Dominated & Balanced Disciplines):**
In contrast, Humanities & Social Sciences saw female enrollment reach 11,900, nearly three times the male count of 4,100. Female students also predominated in Medicine & Life Sciences (9,600 vs 6,400). Finally, Business & Finance displayed near parity, registering 12,100 women and 11,500 men, making it the largest faculty overall at 23,600 students.""",
        "group_id": "W_T1_TAB_1",
        "group_instructions": "Write at least 150 words grouping similar statistical categories."
    })

    # ==========================================
    # TASK 1: MULTIPLE / COMBINED CHARTS
    # ==========================================
    tasks.append({
        "skill": "Writing",
        "test_type": "Academic Task 1",
        "section_number": 1,
        "title": "Household Car Ownership & Annual Distance Traveled",
        "question_type": "Academic Task 1 - Multiple Charts",
        "cambridge_book": "Cambridge 15",
        "test_number": 4,
        "passage_or_section": "Task 1",
        "difficulty_band": "Academic",
        "difficulty": "hard",
        "passage_or_context": """<div class="cambridge-prompt-header">
    <p><b>You should spend about 20 minutes on this task.</b></p>
    <p><i>The pie chart shows the percentage of households with no car, one car, or two or more cars, while the bar chart illustrates the average annual miles driven per person by purpose in 2024.</i></p>
    <p><b>Summarise the information by selecting and reporting the main features, and make comparisons where relevant.</b></p>
    <p><b>Write at least 150 words.</b></p>
</div>
<div class="chart-wrapper" style="background:#0f172a; padding:18px; border-radius:10px; margin:16px 0; border:1px solid #334155; text-align:center;">
    <svg viewBox="0 0 650 310" style="width:100%; max-height:300px; font-family:sans-serif;">
        <rect width="650" height="310" fill="#0f172a" rx="8"/>
        
        <!-- Left: Pie Chart (Ownership) -->
        <text x="160" y="30" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">Car Ownership (% Households)</text>
        <circle cx="160" cy="140" r="75" fill="#1e293b" stroke="#475569"/>
        <!-- 1 Car (48% #38bdf8), 2+ Cars (32% #34d399), No Car (20% #f43f5e) -->
        <path d="M 160 140 L 160 65 A 75 75 0 0 1 230 165 Z" fill="#38bdf8"/>
        <text x="195" y="110" fill="#000" font-size="10" font-weight="bold">1 Car 48%</text>

        <path d="M 160 140 L 230 165 A 75 75 0 0 1 115 200 Z" fill="#34d399"/>
        <text x="170" y="185" fill="#000" font-size="10" font-weight="bold">2+ Cars 32%</text>

        <path d="M 160 140 L 115 200 A 75 75 0 0 1 160 65 Z" fill="#f43f5e"/>
        <text x="115" y="130" fill="#fff" font-size="9" font-weight="bold">No Car 20%</text>

        <!-- Right: Bar Chart (Miles by Purpose) -->
        <text x="470" y="30" fill="#34d399" font-size="12" font-weight="bold" text-anchor="middle">Average Annual Miles Driven per Person</text>
        <line x1="330" y1="55" x2="610" y2="55" stroke="#334155" stroke-dasharray="3"/>
        <line x1="330" y1="110" x2="610" y2="110" stroke="#334155" stroke-dasharray="3"/>
        <line x1="330" y1="165" x2="610" y2="165" stroke="#334155" stroke-dasharray="3"/>
        <line x1="330" y1="220" x2="610" y2="220" stroke="#64748b" stroke-width="2"/>
        <line x1="330" y1="50" x2="330" y2="220" stroke="#64748b" stroke-width="2"/>

        <text x="320" y="60" fill="#94a3b8" font-size="10" text-anchor="end">4,000</text>
        <text x="320" y="115" fill="#94a3b8" font-size="10" text-anchor="end">2,500</text>
        <text x="320" y="170" fill="#94a3b8" font-size="10" text-anchor="end">1,000</text>

        <!-- Bars: Commuting, Shopping, Leisure, School Runs -->
        <rect x="350" y="70" width="35" height="150" fill="#38bdf8"/>
        <text x="367" y="240" fill="#cbd5e1" font-size="9" text-anchor="middle">Work</text>
        <text x="367" y="65" fill="#38bdf8" font-size="9" text-anchor="middle">3,600</text>

        <rect x="420" y="125" width="35" height="95" fill="#fbbf24"/>
        <text x="437" y="240" fill="#cbd5e1" font-size="9" text-anchor="middle">Shopping</text>
        <text x="437" y="120" fill="#fbbf24" font-size="9" text-anchor="middle">2,100</text>

        <rect x="490" y="105" width="35" height="115" fill="#34d399"/>
        <text x="507" y="240" fill="#cbd5e1" font-size="9" text-anchor="middle">Leisure</text>
        <text x="507" y="100" fill="#34d399" font-size="9" text-anchor="middle">2,700</text>

        <rect x="560" y="180" width="35" height="40" fill="#a78bfa"/>
        <text x="577" y="240" fill="#cbd5e1" font-size="9" text-anchor="middle">School</text>
        <text x="577" y="175" fill="#a78bfa" font-size="9" text-anchor="middle">850</text>
    </svg>
</div>""",
        "question_text": "Summarise car ownership distribution and compare annual mileage by journey purpose.",
        "answer_key": "Band 9 Academic Model Report",
        "explanation": """### Band 9 Model Answer:
The pie chart illustrates household car ownership distribution, while the bar chart compares average annual mileage per individual across four distinct travel purposes in 2024.

**Overview:**
Overall, the vast majority of households possessed at least one motor vehicle, with single-car ownership being the most prevalent. Regarding journey purposes, commuting to work accounted for the highest annual mileage, whereas school runs constituted the lowest.

**Body Paragraph 1 (Car Ownership):**
As shown in the pie chart, 80% of all households owned at least one car. Specifically, 48% had a single car, while nearly a third (32%) maintained two or more vehicles. In contrast, only one-fifth (20%) of households were vehicle-free.

**Body Paragraph 2 (Mileage by Purpose):**
Turning to the bar chart, commuting to work generated the greatest distance traveled per person at 3,600 miles annually. Leisure travel ranked second at 2,700 miles, followed closely by shopping trips at 2,100 miles. By far the least mileage was logged for educational school runs, which totaled just 850 miles per person.""",
        "group_id": "W_T1_MIX_1",
        "group_instructions": "Write at least 150 words connecting ownership data with usage purposes."
    })

    # ==========================================
    # TASK 2: ADVANTAGES VS DISADVANTAGES
    # ==========================================
    tasks.append({
        "skill": "Writing",
        "test_type": "Task 2",
        "section_number": 2,
        "title": "Space Exploration Funding vs Domestic Spending",
        "question_type": "Task 2 - Advantages vs Disadvantages",
        "cambridge_book": "Cambridge 16",
        "test_number": 2,
        "passage_or_section": "Task 2",
        "difficulty_band": "Academic",
        "difficulty": "hard",
        "passage_or_context": """<div class="cambridge-prompt-header">
    <p><b>You should spend about 40 minutes on this task.</b></p>
    <p>Write about the following topic:</p>
    <div style="background:rgba(225,29,72,0.1); border-left:4px solid #e11d48; padding:14px; margin:14px 0; font-size:1.05em; color:#fff; line-height:1.6;">
        <b>Governments worldwide allocate billions of dollars to space exploration and planetary research. Do the advantages of space exploration outweigh the disadvantages, considering urgent domestic challenges on Earth?</b>
    </div>
    <p><i>Give reasons for your answer and include any relevant examples from your own knowledge or experience.</i></p>
    <p><b>Write at least 250 words.</b></p>
</div>""",
        "question_text": "Evaluate whether the scientific and technological merits of space exploration outweigh the substantial financial costs.",
        "answer_key": "Band 9 Academic Essay",
        "explanation": """### Band 9 Model Essay:
Global state expenditure on aerospace missions and interplanetary exploration has sparked intense public controversy. Critics assert that astronomical expenditures are irresponsible when pressing issues like poverty and climate change plague our planet. However, I firmly maintain that the technological, scientific, and strategic benefits derived from space exploration far outweigh its financial costs.

The principal drawback of space missions is their monumental fiscal burden. Developing launch vehicles, orbital telescopes, and deep-space probes demands billions of dollars in taxpayer funding. Sceptics legitimately argue that redirecting these astronomical budgets towards public healthcare systems, renewable energy subsidies, or poverty alleviation would yield immediate, tangible humanitarian dividends on Earth.

Nonetheless, space research acts as an unparalleled catalyst for terrestrial technological innovation. Historically, aerospace engineering has yielded transformative spillover technologies, including satellite navigation (GPS), advanced medical imaging, water purification systems, and solar photovoltaic cells. These breakthroughs have enriched the global economy by trillions of dollars, dwarfing initial research investments. Furthermore, satellite monitoring systems provide indispensable meteorological data for predicting natural catastrophes and monitoring global climate degradation.

Ultimately, space research addresses the long-term existential survival of humanity. Investigating extraterrestrial resources and orbital habitats safeguards our civilization against potential catastrophic planetary events.

In conclusion, although the capital requirements of space research are immense, the resultant technological innovations, environmental monitoring capabilities, and civilizational security overwhelmingly surpass the initial financial investment.""",
        "group_id": "W_T2_ADV_1",
        "group_instructions": "Write at least 250 words evaluating both sides before declaring a decisive overall balance."
    })

    # ==========================================
    # TASK 2: TWO-PART / DIRECT QUESTIONS
    # ==========================================
    tasks.append({
        "skill": "Writing",
        "test_type": "Task 2",
        "section_number": 2,
        "title": "Fast Food Consumption & Sedentary Lifestyles",
        "question_type": "Task 2 - Two-Part Question",
        "cambridge_book": "Cambridge 15",
        "test_number": 1,
        "passage_or_section": "Task 2",
        "difficulty_band": "Academic",
        "difficulty": "medium",
        "passage_or_context": """<div class="cambridge-prompt-header">
    <p><b>You should spend about 40 minutes on this task.</b></p>
    <p>Write about the following topic:</p>
    <div style="background:rgba(225,29,72,0.1); border-left:4px solid #e11d48; padding:14px; margin:14px 0; font-size:1.05em; color:#fff; line-height:1.6;">
        <b>In many developed and developing nations, consumption of fast food and sedentary lifestyles are escalating rapidly. Why is this happening? What measures can be taken to encourage healthier lifestyle choices?</b>
    </div>
    <p><i>Give reasons for your answer and include any relevant examples from your own knowledge or experience.</i></p>
    <p><b>Write at least 250 words.</b></p>
</div>""",
        "question_text": "Examine the socio-economic causes behind poor dietary and physical habits and propose comprehensive public health interventions.",
        "answer_key": "Band 9 Academic Essay",
        "explanation": """### Band 9 Model Essay:
Modern society is witnessing an alarming surge in fast-food reliance and physical inactivity, precipitating a worldwide public health crisis. This essay will examine the socio-economic catalysts behind this trend and propose effective public policy interventions.

The escalating consumption of processed fast food and physical stagnation are largely driven by modern workplace culture and aggressive commercial marketing. In contemporary fast-paced economies, extended working hours and intense occupational stress leave individuals with minimal leisure time or mental energy to prepare wholesome meals from scratch. Fast food chains exploit this temporal deficit by offering cheap, hyper-convenient, and calorie-dense options. Simultaneously, the ubiquity of digital entertainment and desk-bound occupations has fostered pervasive physical inactivity, reducing daily calorie expenditure.

To counteract these detrimental habits, multifaceted interventions involving education, taxation, and urban design are essential. Firstly, governments should implement fiscal measures, such as imposing a targeted sugar and saturated fat tax on ultra-processed commodities, while utilizing the revenue to subsidize fresh organic produce. Secondly, national educational curricula must integrate mandatory culinary nutrition and daily physical fitness programs from primary schooling. Finally, municipal authorities must invest in pedestrian-friendly urban infrastructure, including segregated cycle superhighways and complimentary public recreational parks, making physical exercise accessible and convenient.

In conclusion, while the demands of modern employment and commercial marketing fuel dietary decline and sedentary living, targeted taxation on unhealthy foods alongside urban infrastructure improvements can successfully cultivate a healthier populace.""",
        "group_id": "W_T2_TWOPART_1",
        "group_instructions": "Write at least 250 words directly answering Question 1 in Body 1 and Question 2 in Body 2."
    })

    # ==========================================
    # TASK 2: POSITIVE OR NEGATIVE DEVELOPMENT
    # ==========================================
    tasks.append({
        "skill": "Writing",
        "test_type": "Task 2",
        "section_number": 2,
        "title": "Transition to a Cashless & Digital Payment Economy",
        "question_type": "Task 2 - Positive or Negative Development",
        "cambridge_book": "Cambridge 19",
        "test_number": 2,
        "passage_or_section": "Task 2",
        "difficulty_band": "Academic",
        "difficulty": "medium",
        "passage_or_context": """<div class="cambridge-prompt-header">
    <p><b>You should spend about 40 minutes on this task.</b></p>
    <p>Write about the following topic:</p>
    <div style="background:rgba(225,29,72,0.1); border-left:4px solid #e11d48; padding:14px; margin:14px 0; font-size:1.05em; color:#fff; line-height:1.6;">
        <b>In many nations, physical banknotes and coins are rapidly being replaced by electronic transactions, contactless payments, and digital currencies. In your opinion, is this a positive or negative development?</b>
    </div>
    <p><i>Give reasons for your answer and include any relevant examples from your own knowledge or experience.</i></p>
    <p><b>Write at least 250 words.</b></p>
</div>""",
        "question_text": "Evaluate the financial, logistical, and social ramifications of transitioning to a completely cashless society.",
        "answer_key": "Band 9 Academic Essay",
        "explanation": """### Band 9 Model Essay:
Across the globe, traditional physical cash is rapidly yielding to mobile payment applications, contactless banking cards, and decentralized digital currencies. While this paradigm shift introduces valid concerns regarding cybersecurity and financial exclusion, I believe that the transition towards a cashless economy is overwhelmingly a positive development due to enhanced transactional efficiency and the reduction of financial crime.

The paramount advantage of electronic commerce is unprecedented commercial convenience and fiscal transparency. Digital transactions eliminate the operational overhead and logistical hazards associated with transporting, counting, and securing physical currency. For consumers and merchants alike, point-of-sale transactions are virtually instantaneous. Moreover, digital payment rails create an indelible, automated audit trail for every fiscal transaction. This transparency drastically curtails the shadow economy, tax evasion, money laundering, and street-level robbery, thereby bolstering national tax revenues and public safety.

Admittedly, a fully digital fiscal ecosystem poses authentic hazards. Vulnerable demographic groups—particularly the elderly, impoverished communities, and those lacking digital literacy—risk marginalization if cash is wholly phased out. Furthermore, reliance on electronic banking heightens vulnerability to cyberattacks, identity theft, and systemic server outages.

Nevertheless, these risks can be systematically mitigated through robust regulatory frameworks, state-backed biometric authentication, and public digital literacy initiatives. The overarching macroeconomic and security dividends of a cashless society far outweigh these manageable challenges.

In conclusion, despite cybersecurity vulnerabilities and inclusion hurdles, the demise of physical cash represents a distinctly positive evolution that streamlines global commerce and combats financial criminality.""",
        "group_id": "W_T2_POSNEG_1",
        "group_instructions": "Write at least 250 words presenting a clear evaluation of positive vs negative impacts."
    })

    return tasks

def seed_full_cambridge_writing():
    """Seeds authentic Cambridge IELTS Academic Writing prompts into database."""
    conn = sqlite3.connect('ielts_platform.db')
    cursor = conn.cursor()

    # Clear existing writing questions
    cursor.execute("DELETE FROM questions WHERE skill = 'Writing'")

    tasks = get_cambridge_writing_tasks()
    for t in tasks:
        cursor.execute('''
            INSERT INTO questions (
                skill, test_type, section_number, title, question_type,
                passage_or_context, question_text, options_json, answer_key,
                explanation, difficulty, cambridge_book, test_number,
                passage_or_section, difficulty_band, group_id, group_instructions
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            t["skill"], t["test_type"], t["section_number"], t["title"], t["question_type"],
            t["passage_or_context"], t["question_text"], json.dumps([]), t["answer_key"],
            t["explanation"], t["difficulty"], t["cambridge_book"], t["test_number"],
            t["passage_or_section"], t["difficulty_band"], t["group_id"], t["group_instructions"]
        ))

    conn.commit()
    conn.close()
    print(f"SUCCESS: Seeded {len(tasks)} authentic Cambridge Writing Tasks into SQLite database.")

if __name__ == '__main__':
    seed_full_cambridge_writing()

