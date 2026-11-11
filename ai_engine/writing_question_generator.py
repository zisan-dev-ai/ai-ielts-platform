"""
AI Writing Question Generator for Cambridge IELTS Academic Writing
Supports:
1. Dynamic AI Prompt Generation for Task 1 (with valid vector SVG charts/maps/processes)
2. Dynamic AI Prompt Generation for Task 2 (Discursive Essays with brainstorming structure)
3. Student Custom Topic Inputs (generating custom prompts from student-provided themes)
4. Manual Question Saving (storing student-written prompts directly into database)
"""

import json
import random
import re
from typing import Dict, Any, Optional
import sqlite3
from ai_engine.gemini_adapter import GeminiAdapter

class WritingQuestionGenerator:
    def __init__(self):
        self.ai = GeminiAdapter()

    def generate_custom_topic_prompt(self, task_type: str, custom_theme: str = "", api_key: str = "", api_key_pool: list = None) -> Dict[str, Any]:
        """
        Generates an authentic Cambridge IELTS Writing prompt based on student-selected type or custom theme.
        task_type: 'Task 1 - Line Graph', 'Task 1 - Bar Chart', 'Task 1 - Pie Chart', 'Task 1 - Table', 
                   'Task 1 - Process Diagram', 'Task 1 - Map / Layout', 'Task 2 - Agree or Disagree',
                   'Task 2 - Discuss Both Views', 'Task 2 - Advantages vs Disadvantages', 
                   'Task 2 - Problem and Solution', 'Task 2 - Two-Part Question'
        """
        is_task_1 = "Task 1" in task_type

        # Extensive pool of rotating authentic Cambridge IELTS academic themes
        THEME_TOPICS_TASK1 = [
            "Renewable Electricity Generation (Wind, Solar, Hydro) from 1990 to 2030",
            "Household Expenditure on Housing, Food, Transport and Healthcare across 5 Countries",
            "International Student Enrollment in Universities by Discipline and Gender",
            "Global Water Consumption for Agriculture, Industry and Domestic Use",
            "CO2 Emissions per Capita in Six Developed and Developing Economies",
            "Industrial Manufacturing Process of Paper from Recycled Pulp",
            "Life Cycle and Migration Pattern of Pacific Salmon",
            "Redevelopment Plan of an Industrial Harbor into a Waterfront Commercial Zone",
            "Expansion of a University Campus between 2005 and Present Day",
            "Car Ownership Proportions and Average Annual Mileage by Commuting Purpose",
            "Fast Food and Organic Produce Sales Market Share over a 20-Year Period",
            "Air Passenger Numbers and Rail Travel Statistics in Four European Nations"
        ]

        THEME_TOPICS_TASK2 = [
            "Artificial Intelligence and Robotic Automation in the Modern Workforce",
            "State Funding for Space Exploration vs Immediate Domestic Humanitarian Challenges",
            "University Education Free Tuition vs Private Student Loan Schemes",
            "Compulsory Community Service for School Leavers before Tertiary Education",
            "Sugar Tax and Advertising Restrictions on Ultra-Processed Fast Foods",
            "Transition to a Completely Cashless Economy and Digital Payment Infrastructure",
            "Remote Work from Home vs Mandatory Physical Office Attendance",
            "Preservation of Minority and Indigenous Languages in a Globalized World",
            "Urban Overcrowding, High-Rise Housing and Traffic Congestion in Megacities",
            "Environmental Responsibility: Individual Lifestyle Shifts vs Strict Corporate Regulation",
            "Impact of Social Media and Digital Screen Time on Adolescent Mental Health",
            "Tourism Expansion: Economic Revenue Generation vs Degradation of Natural Heritage",
            "Aging Populations and Government Pension Sustainability in Developed Countries",
            "Artificial Meat and Plant-Based Diets to Combat Global Climate Change"
        ]

        if custom_theme:
            chosen_theme = custom_theme
        else:
            chosen_theme = random.choice(THEME_TOPICS_TASK1 if is_task_1 else THEME_TOPICS_TASK2)

        theme_text = f"specifically on the realistic topic of '{chosen_theme}'"

        if is_task_1:
            prompt = f"""You are a Cambridge IELTS Chief Writing Examiner and expert SVG data visualization designer.
Generate an authentic IELTS Academic Writing Task 1 exam task {theme_text}.
Specific Visual Category: {task_type}

You MUST return a strictly valid JSON object with the following structure:
{{
  "title": "Title of the task (e.g. Global Renewable Energy Trends 2010-2030)",
  "question_type": "{task_type}",
  "prompt_intro": "The chart/diagram below shows...",
  "instructions": "Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.",
  "svg_chart": "<svg>FULL DETAILED SVG HERE</svg>",
  "band_9_model_answer": "Full 170-200 word Band 9 model report organized into: Introduction, Overview, Body Paragraph 1, Body Paragraph 2.",
  "key_features_summary": ["Feature 1...", "Feature 2...", "Feature 3..."],
  "data_categories": ["category1", "category2", "..."],
  "data_series": ["series1", "series2", "..."]
}}

CRITICAL SVG CHART REQUIREMENTS — YOU MUST FOLLOW ALL:
1. viewBox: viewBox='0 0 650 340'. Style: width:100%; max-height:320px; font-family:sans-serif;
2. Background: <rect width='650' height='340' fill='#0f172a' rx='8'/>
3. Y-AXIS: Draw at least 4 horizontal gridlines with <line> (stroke='#334155' stroke-dasharray='4'). Label each gridline with percentage or value using <text fill='#94a3b8'>.
4. X-AXIS: A solid baseline <line stroke='#64748b' stroke-width='2'/>. Label each group/category on the X-axis with <text fill='#cbd5e1'>.
5. VERTICAL AXIS LINE: Draw a vertical axis line on the left side.
6. DATA BARS/LINES: Use EXACTLY these 4 colors for data series: #38bdf8 (blue), #f43f5e (red/pink), #34d399 (green), #fbbf24 (gold).
   - For bar charts: Each group MUST have one <rect> per data series, with width='18' and realistic heights that match the data values.
   - For line graphs: Use <path> or <polyline> with stroke-width='3'.
   - EVERY category mentioned in prompt_intro MUST appear as data in the chart. If prompt says 4 categories, chart must show 4 groups of bars.
7. LEGEND: Near the top of the SVG, include a legend with one colored <rect width='10' height='10'/> and one <text fill='#e2e8f0'> label for EACH data series.
   - The legend MUST list ALL data series, not just some.
8. TITLE: Add a centered title <text> at the top of the chart.
9. The SVG MUST be at least 2500 characters long. Short/incomplete SVGs are REJECTED.
10. ALL numbers in the chart must be mathematically logical and match the model answer.
11. Output ONLY the JSON object, without any markdown backticks or commentary."""
        else:
            prompt = f"""You are a Cambridge IELTS Chief Writing Examiner.
Generate an authentic IELTS Academic Writing Task 2 Essay prompt {theme_text}.
Specific Essay Category: {task_type}

You MUST return a strictly valid JSON object with the following structure:
{{
  "title": "Topic Title (e.g. Artificial Intelligence and Global Employment)",
  "question_type": "{task_type}",
  "statement": "The official controversial topic statement...",
  "instructions": "Give reasons for your answer and include any relevant examples from your own knowledge or experience. Write at least 250 words.",
  "band_9_model_answer": "Full 270-320 word Band 9 model essay organized into: Introduction with thesis, Body Paragraph 1, Body Paragraph 2, Conclusion.",
  "brainstorming_ideas": {{
    "view_a_or_causes": ["Argument 1...", "Argument 2..."],
    "view_b_or_solutions": ["Counter-argument 1...", "Counter-argument 2..."],
    "recommended_vocabulary": ["paradigmatic shift", "exacerbate", "catalyst", "pragmatic intervention"]
  }}
}}

CRITICAL REQUIREMENTS:
1. The essay statement must be formal, thought-provoking, and match official Cambridge phrasing.
2. Output ONLY the JSON object, without any markdown backticks or commentary."""

        raw_response = self._call_ai(prompt, api_key, api_key_pool)
        parsed = self._parse_json_safe(raw_response)

        if not parsed:
            parsed = self._get_fallback_prompt(task_type, custom_theme)

        # Validate SVG chart quality for Task 1
        if is_task_1 and parsed:
            svg = parsed.get("svg_chart", "")
            if not self._validate_svg_chart(svg):
                # SVG too short or incomplete — use fallback instead
                fallback = self._get_fallback_prompt(task_type, custom_theme)
                parsed["svg_chart"] = fallback.get("svg_chart", "")

        # Save generated prompt to database
        saved_id = self._save_to_database(parsed, is_task_1)
        parsed["db_id"] = saved_id
        return parsed

    def generate_full_writing_exam_set(self, api_key: str = "", api_key_pool: list = None) -> Dict[str, Any]:
        """
        Generates a complete, authentic Cambridge IELTS Academic Writing full test set 
        containing BOTH a fresh Task 1 (with vector SVG chart) and a fresh Task 2 (Discursive Essay).
        """
        t1_types = [
            'Academic Task 1 - Line Graph', 'Academic Task 1 - Bar Chart', 'Academic Task 1 - Pie Chart',
            'Academic Task 1 - Table', 'Academic Task 1 - Multiple Charts', 'Academic Task 1 - Process Diagram',
            'Academic Task 1 - Map / Layout'
        ]
        t2_types = [
            'Task 2 - Agree or Disagree', 'Task 2 - Discuss Both Views', 'Task 2 - Advantages vs Disadvantages',
            'Task 2 - Problem and Solution', 'Task 2 - Two-Part Question', 'Task 2 - Positive or Negative Development'
        ]

        chosen_t1 = random.choice(t1_types)
        chosen_t2 = random.choice(t2_types)

        t1_res = self.generate_custom_topic_prompt(chosen_t1, "", api_key, api_key_pool)
        t2_res = self.generate_custom_topic_prompt(chosen_t2, "", api_key, api_key_pool)

        return {
            "task1": t1_res,
            "task2": t2_res,
            "t1_id": t1_res.get("db_id"),
            "t2_id": t2_res.get("db_id")
        }

    def _validate_svg_chart(self, svg: str) -> bool:
        """Validate that an SVG chart meets minimum quality requirements."""
        if not svg or len(svg) < 800:
            return False
        svg_lower = svg.lower()
        # Must contain basic SVG structure
        if '<svg' not in svg_lower or '</svg>' not in svg_lower:
            return False
        # Must have at least 2 different data colors from our palette
        data_colors = ['#38bdf8', '#f43f5e', '#34d399', '#fbbf24']
        colors_found = sum(1 for c in data_colors if c in svg)
        if colors_found < 2:
            return False
        # Must have some text labels (axis labels, legend)
        text_count = svg_lower.count('<text')
        if text_count < 4:
            return False
        # Must have rect elements (bars) or path/polyline (lines)
        has_bars = svg_lower.count('<rect') >= 3
        has_lines = '<path' in svg_lower or '<polyline' in svg_lower
        if not has_bars and not has_lines:
            return False
        return True

    def _call_ai(self, prompt: str, api_key: str, api_key_pool: list) -> str:
        keys_to_try = [api_key] if api_key else []
        if api_key_pool:
            keys_to_try.extend([k for k in api_key_pool if k and k != api_key])

        if not keys_to_try:
            conn = sqlite3.connect('ielts_platform.db')
            cursor = conn.cursor()
            cursor.execute("SELECT api_key FROM ai_credentials WHERE provider_id = 'gemini' AND status = 'Active'")
            keys_to_try = [r[0] for r in cursor.fetchall() if r[0]]
            conn.close()

        models_to_try = [
            "gemini-3.1-flash-lite",
            "gemini-flash-lite-latest",
            "gemini-3.5-flash",
            "gemini-3.7-flash",
            "gemini-flash-latest"
        ]

        for model in models_to_try:
            for key in keys_to_try:
                try:
                    import requests
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
                    resp = requests.post(
                        url,
                        json={
                            "contents": [{"parts": [{"text": prompt}]}],
                            "generationConfig": {
                                "temperature": 0.3,
                                "maxOutputTokens": 4096,
                                "responseMimeType": "application/json"
                            }
                        },
                        timeout=15
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        return data['candidates'][0]['content']['parts'][0]['text']
                except Exception:
                    continue
        return ""

    def _parse_json_safe(self, text: str) -> Optional[Dict[str, Any]]:
        if not text:
            return None
        clean = text.strip()
        if clean.startswith("```json"):
            clean = clean[7:]
        if clean.startswith("```"):
            clean = clean[3:]
        if clean.endswith("```"):
            clean = clean[:-3]
        clean = clean.strip()
        try:
            return json.loads(clean)
        except Exception:
            return None

    def _save_to_database(self, data: Dict[str, Any], is_task_1: bool) -> int:
        conn = sqlite3.connect('ielts_platform.db')
        cursor = conn.cursor()

        title = data.get("title", "Custom Writing Task")
        q_type = data.get("question_type", "Academic Writing")
        section_num = 1 if is_task_1 else 2
        test_type = "Academic Task 1" if is_task_1 else "Task 2"

        if is_task_1:
            svg = data.get("svg_chart", "")
            intro = data.get("prompt_intro", "")
            instructions = data.get("instructions", "Write at least 150 words.")
            context_html = f"""<div class="cambridge-prompt-header">
    <p><b>You should spend about 20 minutes on this task.</b></p>
    <p><i>{intro}</i></p>
    <p><b>Summarise the information by selecting and reporting the main features, and make comparisons where relevant.</b></p>
    <p><b>Write at least 150 words.</b></p>
</div>
<div class="chart-wrapper" style="background:#0f172a; padding:18px; border-radius:10px; margin:16px 0; border:1px solid #334155; text-align:center;">
    {svg}
</div>"""
            q_text = intro
        else:
            statement = data.get("statement", "")
            context_html = f"""<div class="cambridge-prompt-header">
    <p><b>You should spend about 40 minutes on this task.</b></p>
    <p>Write about the following topic:</p>
    <div class="prompt-statement-highlight">
        {statement}
    </div>
    <p><i>Give reasons for your answer and include any relevant examples from your own knowledge or experience.</i></p>
    <p><b>Write at least 250 words.</b></p>
</div>"""
            q_text = statement

        explanation = f"### Band 9 Model Answer:\n{data.get('band_9_model_answer', '')}"

        cursor.execute('''
            INSERT INTO questions (
                skill, test_type, section_number, title, question_type,
                passage_or_context, question_text, options_json, answer_key,
                explanation, difficulty, cambridge_book, test_number,
                passage_or_section, difficulty_band, group_id, group_instructions
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            "Writing", test_type, section_num, title, q_type,
            context_html, q_text, json.dumps(data.get("brainstorming_ideas", {})), "Band 9 Model Answer",
            explanation, "medium", "AI Generated Custom", 1,
            "Task " + str(section_num), "Academic", "W_AI_CUSTOM", "Write according to official Cambridge specifications."
        ))
        inserted_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return inserted_id

    def _get_fallback_prompt(self, task_type: str, custom_theme: str) -> Dict[str, Any]:
        is_task_1 = "Task 1" in task_type
        if is_task_1:
            return {
                "title": f"Global Trends in {custom_theme or 'Renewable Energy Consumption'}",
                "question_type": task_type,
                "prompt_intro": f"The bar chart below compares {custom_theme or 'renewable energy consumption (in terawatt-hours)'} across three major regions (North America, Europe, and Asia-Pacific) in four time periods (2010, 2015, 2020, and 2025).",
                "instructions": "Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.",
                "svg_chart": """<svg viewBox="0 0 650 340" style="width:100%; max-height:320px; font-family:sans-serif;">
    <rect width="650" height="340" fill="#0f172a" rx="8"/>
    <!-- Title -->
    <text x="325" y="22" fill="#e2e8f0" font-size="13" font-weight="bold" text-anchor="middle">Renewable Energy Consumption (TWh)</text>
    <!-- Grid Lines -->
    <line x1="80" y1="50" x2="610" y2="50" stroke="#334155" stroke-dasharray="4"/>
    <line x1="80" y1="100" x2="610" y2="100" stroke="#334155" stroke-dasharray="4"/>
    <line x1="80" y1="150" x2="610" y2="150" stroke="#334155" stroke-dasharray="4"/>
    <line x1="80" y1="200" x2="610" y2="200" stroke="#334155" stroke-dasharray="4"/>
    <line x1="80" y1="250" x2="610" y2="250" stroke="#334155" stroke-dasharray="4"/>
    <!-- Axes -->
    <line x1="80" y1="270" x2="610" y2="270" stroke="#64748b" stroke-width="2"/>
    <line x1="80" y1="40" x2="80" y2="270" stroke="#64748b" stroke-width="2"/>
    <!-- Y-axis labels -->
    <text x="70" y="55" fill="#94a3b8" font-size="11" text-anchor="end">500</text>
    <text x="70" y="105" fill="#94a3b8" font-size="11" text-anchor="end">400</text>
    <text x="70" y="155" fill="#94a3b8" font-size="11" text-anchor="end">300</text>
    <text x="70" y="205" fill="#94a3b8" font-size="11" text-anchor="end">200</text>
    <text x="70" y="255" fill="#94a3b8" font-size="11" text-anchor="end">100</text>
    <text x="70" y="275" fill="#94a3b8" font-size="11" text-anchor="end">0</text>
    <!-- 2010 group -->
    <rect x="105" y="210" width="22" height="60" fill="#38bdf8"/>
    <rect x="130" y="195" width="22" height="75" fill="#f43f5e"/>
    <rect x="155" y="230" width="22" height="40" fill="#34d399"/>
    <!-- 2015 group -->
    <rect x="225" y="180" width="22" height="90" fill="#38bdf8"/>
    <rect x="250" y="160" width="22" height="110" fill="#f43f5e"/>
    <rect x="275" y="195" width="22" height="75" fill="#34d399"/>
    <!-- 2020 group -->
    <rect x="345" y="130" width="22" height="140" fill="#38bdf8"/>
    <rect x="370" y="100" width="22" height="170" fill="#f43f5e"/>
    <rect x="395" y="140" width="22" height="130" fill="#34d399"/>
    <!-- 2025 group -->
    <rect x="465" y="90" width="22" height="180" fill="#38bdf8"/>
    <rect x="490" y="55" width="22" height="215" fill="#f43f5e"/>
    <rect x="515" y="80" width="22" height="190" fill="#34d399"/>
    <!-- X-axis labels -->
    <text x="140" y="290" fill="#cbd5e1" font-size="12" text-anchor="middle">2010</text>
    <text x="260" y="290" fill="#cbd5e1" font-size="12" text-anchor="middle">2015</text>
    <text x="380" y="290" fill="#cbd5e1" font-size="12" text-anchor="middle">2020</text>
    <text x="500" y="290" fill="#cbd5e1" font-size="12" text-anchor="middle">2025</text>
    <!-- Legend -->
    <rect x="180" y="305" width="10" height="10" fill="#38bdf8"/>
    <text x="195" y="314" fill="#e2e8f0" font-size="11">North America</text>
    <rect x="310" y="305" width="10" height="10" fill="#f43f5e"/>
    <text x="325" y="314" fill="#e2e8f0" font-size="11">Europe</text>
    <rect x="410" y="305" width="10" height="10" fill="#34d399"/>
    <text x="425" y="314" fill="#e2e8f0" font-size="11">Asia-Pacific</text>
</svg>""",
                "band_9_model_answer": "The bar chart compares renewable energy consumption measured in terawatt-hours across North America, Europe, and Asia-Pacific over four time periods from 2010 to 2025.\n\nOverall, all three regions witnessed consistent upward trends in renewable energy adoption, with Europe registering the most dramatic increase and becoming the dominant consumer by 2025.\n\nIn 2010, renewable energy consumption was relatively modest across all regions, with North America consuming approximately 136 TWh, Europe slightly higher at 170 TWh, and Asia-Pacific the lowest at around 90 TWh. By 2015, Europe had accelerated its consumption to roughly 250 TWh, overtaking North America (205 TWh), while Asia-Pacific grew modestly to 170 TWh.\n\nThe upward trajectory intensified between 2020 and 2025. Europe surged from 386 TWh to 488 TWh, maintaining its lead. North America followed a similar pattern, rising from 318 TWh to 409 TWh. Asia-Pacific demonstrated the steepest proportional growth, climbing from 295 TWh to 432 TWh, nearly quintupling its 2010 figure."
            }
        else:
            return {
                "title": f"Contemporary Perspectives on {custom_theme or 'Modern Technology and Society'}",
                "question_type": task_type,
                "statement": f"In modern society, developments in {custom_theme or 'artificial intelligence and digital communication'} have transformed human interaction. Some argue that this has eroded genuine social bonds, while others contend it has broadened human collaboration.",
                "instructions": "Discuss both views and give your own opinion. Write at least 250 words.",
                "band_9_model_answer": "Technological advancements have fundamentally restructured interpersonal dynamics across the globe. While critics lament the degradation of authentic face-to-face interaction, I argue that digital connectivity enhances global synergy when utilized judiciously."
            }
