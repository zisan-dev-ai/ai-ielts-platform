# -*- coding: utf-8 -*-
"""
Procedural & AI-Powered Infinite IELTS Map Generator Engine.
Generates unlimited, authentic, high-precision Black & White cartographic SVG maps
strictly adhering to Cambridge IELTS / British Council / IDP CD-IELTS standards.

Capabilities:
1. Unlimited Procedural Map Synthesizer for any custom/AI-generated topic or random session:
   - Estate / Manor Grounds
   - Nature & Wildlife Sanctuaries
   - Arts & Cultural Festivals / Riverfront Promenades
   - Botanical Gardens & Glasshouses
   - Forest Adventure & Mountain Trails
   - Cycling & Nature Reserves
   - Indoor Facility Floorplans & Museum Galleries
   - Harbor & Coastal Town Plans
2. Authentic Directional Compass Rose with North pointer ('N').
3. Scaled Metric Bar (0, 25m/50m, 50m/100m).
4. Clearly marked Starting Point / Entrance / "You are here".
5. Dynamic, non-overlapping A-H interactive clickable hotspots matching test questions.
6. Specific authentic master templates for Cambridge Books 14-19.
"""

import math
import random
import hashlib
from typing import Dict, Any, Optional, List, Tuple


def _compass_and_scale(scale_1="50m", scale_2="100m", compass_x=462, compass_y=360, scale_x=25, scale_y=385) -> str:
    """Authentic Cambridge IELTS Compass Rose + Scale Bar"""
    return f"""
    <!-- Compass Rose -->
    <g transform="translate({compass_x},{compass_y})">
        <polygon points="0,-18 5,0 0,-5 -5,0" fill="#000000"/>
        <polygon points="0,18 5,0 0,5 -5,0" fill="#ffffff" stroke="#000000" stroke-width="0.9"/>
        <text x="-4" y="-22" font-size="11" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">N</text>
    </g>
    <!-- Scale Bar -->
    <g transform="translate({scale_x},{scale_y})">
        <rect x="0" y="-4" width="35" height="5" fill="#000000"/>
        <rect x="35" y="-4" width="35" height="5" fill="#ffffff" stroke="#000000" stroke-width="0.8"/>
        <text x="0" y="9" font-size="7.5" font-family="Arial, Helvetica, sans-serif" fill="#000000">0</text>
        <text x="28" y="9" font-size="7.5" font-family="Arial, Helvetica, sans-serif" fill="#000000">{scale_1}</text>
        <text x="63" y="9" font-size="7.5" font-family="Arial, Helvetica, sans-serif" fill="#000000">{scale_2}</text>
    </g>"""


def _hotspot(letter: str, cx: int, cy: int) -> str:
    """Clickable circular letter badge marker matching official IELTS CBT style"""
    return f"""<g class="map-hotspot" id="hotspot-{letter}" onclick="handleMapClick('{letter}')" style="cursor:pointer;">
        <circle cx="{cx}" cy="{cy}" r="13" fill="#ffffff" stroke="#000000" stroke-width="2"/>
        <text x="{cx}" y="{cy+4.5}" text-anchor="middle" font-size="13" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">{letter}</text>
    </g>"""


# =========================================================================
# PROCEDURAL MAP SYNTHESIZER: UNLIMITED AI-GENERATED MAPS
# =========================================================================

class ProceduralIELTSMapSynthesizer:
    """
    Synthesizes brand new, unlimited, high-quality Cambridge IELTS SVG maps on the fly
    for any theme, seed, or layout archetype.
    """

    ARCHETYPES = [
        "country_estate",
        "wildlife_sanctuary",
        "riverfront_promenade",
        "botanic_gardens",
        "adventure_park",
        "cycling_trail",
        "indoor_complex",
        "coastal_harbor"
    ]

    def __init__(self, seed: Optional[str] = None):
        if seed:
            # Deterministic pseudo-random seed from string hash
            int_seed = int(hashlib.md5(str(seed).encode('utf-8')).hexdigest()[:8], 16)
            self.rng = random.Random(int_seed)
        else:
            self.rng = random.Random()

    def generate(self, theme_hint: str = "") -> str:
        """Generates a complete procedural SVG map matching the theme or a random archetype."""
        hint = theme_hint.lower()
        if any(k in hint for k in ["estate", "lodge", "manor", "hall", "house"]):
            archetype = "country_estate"
        elif any(k in hint for k in ["wildlife", "sanctuary", "wetland", "marsh", "animal", "bird"]):
            archetype = "wildlife_sanctuary"
        elif any(k in hint for k in ["river", "festival", "promenade", "quay", "music", "arts"]):
            archetype = "riverfront_promenade"
        elif any(k in hint for k in ["botanic", "garden", "conservatory", "plant", "flower", "greenhouse"]):
            archetype = "botanic_gardens"
        elif any(k in hint for k in ["adventure", "park", "ridge", "climbing", "canyon", "forest"]):
            archetype = "adventure_park"
        elif any(k in hint for k in ["cycle", "cycling", "bike", "trail", "valley", "reserve"]):
            archetype = "cycling_trail"
        elif any(k in hint for k in ["museum", "library", "complex", "center", "centre", "sports", "indoor", "facility"]):
            archetype = "indoor_complex"
        elif any(k in hint for k in ["harbor", "harbour", "coastal", "port", "island", "sea", "bay"]):
            archetype = "coastal_harbor"
        else:
            archetype = self.rng.choice(self.ARCHETYPES)

        generator_fn = getattr(self, f"_synth_{archetype}", self._synth_country_estate)
        return generator_fn()

    def _synth_country_estate(self) -> str:
        """Procedural Country Estate / Historic Park Map"""
        r = self.rng
        house_w = r.randint(110, 140)
        house_h = r.randint(70, 90)
        house_x = 250 - house_w // 2
        house_y = r.randint(135, 155)

        lake_x = r.randint(70, 95)
        lake_y = r.randint(270, 300)
        lake_rx = r.randint(40, 55)
        lake_ry = r.randint(25, 38)

        entrance_label = r.choice([
            "Car Park &amp; South Gate",
            "Main Visitor Entrance",
            "South Gate &amp; Ticket Pavilion"
        ])

        # 8 Zone Hotspots (A to H)
        hotspots = [
            ("A", house_x - r.randint(60, 85), house_y + r.randint(10, 30)),       # W of house (Stable / Shop)
            ("B", house_x - r.randint(15, 25), house_y + house_h - 10),            # SW terrace
            ("C", r.randint(375, 410), r.randint(300, 335)),                       # SE Playground / Meadow
            ("D", r.randint(380, 420), r.randint(65, 90)),                         # NE Gardens
            ("E", 250 + r.randint(-20, 20), r.randint(38, 55)),                    # North Temple / Pavilion
            ("F", lake_x + r.randint(-10, 10), lake_y + r.randint(-5, 10)),        # Lake area
            ("G", r.randint(55, 80), r.randint(55, 80)),                           # NW Woodland
            ("H", r.randint(385, 415), r.randint(170, 200)),                      # East Orchard
        ]
        hotspots_svg = "\n    ".join(_hotspot(letter, x, y) for letter, x, y in hotspots)

        return f"""<svg id="cambridgeMapSvg" viewBox="0 0 500 400" style="width:100%; height:auto; display:block; background:#ffffff;">
    <rect width="500" height="400" fill="#ffffff"/>
    <rect x="18" y="12" width="464" height="370" fill="none" stroke="#000000" stroke-width="2.5"/>

    <!-- Driveway & Car Park (South) -->
    <rect x="220" y="315" width="60" height="67" fill="#f1f5f9" stroke="#000000" stroke-width="0.9"/>
    <rect x="238" y="240" width="24" height="75" fill="#f1f5f9" stroke="none"/>
    <ellipse cx="250" cy="240" rx="36" ry="18" fill="#f1f5f9" stroke="#000000" stroke-width="0.8"/>
    <text x="250" y="396" text-anchor="middle" font-size="9" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">{entrance_label}</text>

    <!-- Walking Paths -->
    <line x1="175" y1="240" x2="55" y2="240" stroke="#000000" stroke-width="0.9" stroke-dasharray="5,3"/>
    <line x1="325" y1="240" x2="445" y2="240" stroke="#000000" stroke-width="0.9" stroke-dasharray="5,3"/>
    <line x1="250" y1="220" x2="250" y2="70" stroke="#000000" stroke-width="0.9" stroke-dasharray="5,3"/>

    <!-- Manor House (Center) -->
    <rect x="{house_x}" y="{house_y}" width="{house_w}" height="{house_h}" fill="#ffffff" stroke="#000000" stroke-width="2.2"/>
    <text x="250" y="{house_y + house_h//2 + 4}" text-anchor="middle" font-size="10.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Main Estate House</text>

    <!-- Stable Block (West) -->
    <rect x="28" y="140" width="105" height="55" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>
    <line x1="55" y1="140" x2="55" y2="195" stroke="#000000" stroke-width="0.6"/>
    <line x1="82" y1="140" x2="82" y2="195" stroke="#000000" stroke-width="0.6"/>
    <line x1="109" y1="140" x2="109" y2="195" stroke="#000000" stroke-width="0.6"/>
    <text x="80" y="172" text-anchor="middle" font-size="8.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Stable Block</text>

    <!-- Kitchen Gardens (NE Walled Enclosure) -->
    <rect x="350" y="25" width="125" height="105" fill="#ffffff" stroke="#000000" stroke-width="1.8"/>
    <line x1="365" y1="48" x2="460" y2="48" stroke="#000000" stroke-width="0.5" stroke-dasharray="3,3"/>
    <line x1="365" y1="68" x2="460" y2="68" stroke="#000000" stroke-width="0.5" stroke-dasharray="3,3"/>
    <line x1="365" y1="88" x2="460" y2="88" stroke="#000000" stroke-width="0.5" stroke-dasharray="3,3"/>
    <text x="412" y="122" text-anchor="middle" font-size="8.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Walled Gardens</text>

    <!-- Ornamental Lake (SW) -->
    <ellipse cx="{lake_x}" cy="{lake_y}" rx="{lake_rx}" ry="{lake_ry}" fill="#e0ecf4" stroke="#000000" stroke-width="1.4"/>
    <text x="{lake_x}" y="{lake_y+3}" text-anchor="middle" font-size="8.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Lake</text>

    <!-- Ancient Woodland (NW) -->
    <rect x="30" y="30" width="105" height="85" fill="#f8fafc" stroke="#000000" stroke-width="1.2"/>
    <circle cx="50" cy="55" r="12" fill="none" stroke="#000000" stroke-width="1"/>
    <circle cx="75" cy="48" r="10" fill="none" stroke="#000000" stroke-width="1"/>
    <circle cx="100" cy="60" r="11" fill="none" stroke="#000000" stroke-width="1"/>
    <text x="75" y="100" text-anchor="middle" font-size="8.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Woodland</text>

    <!-- Orchard (East) -->
    <rect x="350" y="150" width="115" height="80" fill="#ffffff" stroke="#000000" stroke-width="1.2" stroke-dasharray="4,2"/>
    <text x="408" y="220" text-anchor="middle" font-size="8" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Fruit Orchard</text>

    <!-- Pavilion / Temple (North Centre) -->
    <polygon points="248,28 282,28 265,16" fill="#ffffff" stroke="#000000" stroke-width="1.3"/>
    <rect x="248" y="28" width="34" height="24" fill="#ffffff" stroke="#000000" stroke-width="1.3"/>
    <text x="265" y="67" text-anchor="middle" font-size="7" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Temple</text>

    {hotspots_svg}
    {_compass_and_scale("50m", "100m")}
</svg>"""

    def _synth_wildlife_sanctuary(self) -> str:
        """Procedural Wildlife & Nature Reserve Map"""
        r = self.rng
        wetland_cx = 250 + r.randint(-20, 20)
        wetland_cy = 210 + r.randint(-15, 15)

        hotspots = [
            ("A", wetland_cx + r.randint(55, 75), wetland_cy - r.randint(30, 50)),   # Discovery Centre
            ("B", r.randint(380, 420), r.randint(70, 95)),                          # Aviary
            ("C", r.randint(375, 415), r.randint(305, 340)),                        # Bio-Dome / Reptile
            ("D", r.randint(70, 100), r.randint(265, 295)),                         # Treehouse Cafe
            ("E", 250 + r.randint(-15, 15), r.randint(65, 85)),                     # North Ridge Ranger Station
            ("F", r.randint(155, 185), wetland_cy),                                 # Western boardwalk
            ("G", r.randint(70, 95), r.randint(80, 110)),                          # Woodland Hide
            ("H", r.randint(265, 295), r.randint(320, 345)),                       # South Meadow
        ]
        hotspots_svg = "\n    ".join(_hotspot(letter, x, y) for letter, x, y in hotspots)

        return f"""<svg id="cambridgeMapSvg" viewBox="0 0 500 400" style="width:100%; height:auto; display:block; background:#ffffff;">
    <rect width="500" height="400" fill="#ffffff"/>
    <rect x="18" y="12" width="464" height="370" fill="none" stroke="#000000" stroke-width="2.5"/>

    <!-- Trail Spine -->
    <line x1="250" y1="380" x2="250" y2="80" stroke="#000000" stroke-width="1.6" stroke-dasharray="6,4"/>
    <line x1="45" y1="210" x2="455" y2="210" stroke="#000000" stroke-width="1.6" stroke-dasharray="6,4"/>
    <text x="250" y="396" text-anchor="middle" font-size="9" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">South Visitor Entrance &amp; Car Park</text>

    <!-- Wetland Marsh (Centre) -->
    <ellipse cx="{wetland_cx}" cy="{wetland_cy}" rx="58" ry="34" fill="#e0ecf4" stroke="#000000" stroke-width="1.4"/>
    <text x="{wetland_cx}" y="{wetland_cy+3}" text-anchor="middle" font-size="8.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Wetland Marsh</text>

    <!-- Ancient Woodland (NW) -->
    <rect x="28" y="28" width="118" height="145" fill="#f8fafc" stroke="#000000" stroke-width="1.4"/>
    <circle cx="55" cy="58" r="10" fill="none" stroke="#000000" stroke-width="0.9"/>
    <circle cx="80" cy="52" r="9" fill="none" stroke="#000000" stroke-width="0.9"/>
    <circle cx="105" cy="62" r="10" fill="none" stroke="#000000" stroke-width="0.9"/>
    <text x="86" y="145" text-anchor="middle" font-size="8.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Ancient Woodland</text>

    <!-- North Ridge Trail -->
    <path d="M 180 35 Q 250 25 330 35 Q 400 45 460 30" fill="none" stroke="#000000" stroke-width="1.2" stroke-dasharray="4,2"/>
    <text x="250" y="48" text-anchor="middle" font-size="8" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">North Ridge Trail</text>

    <!-- Picnic Meadows (SE) -->
    <rect x="330" y="265" width="135" height="95" fill="#f8fafc" stroke="#000000" stroke-width="1.2" stroke-dasharray="4,3"/>
    <text x="398" y="315" text-anchor="middle" font-size="8" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Picnic Meadows</text>

    <!-- Buildings -->
    <rect x="270" y="145" width="80" height="48" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>
    <rect x="355" y="55" width="95" height="60" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>
    <circle cx="395" cy="325" r="24" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>
    <rect x="45" y="255" width="85" height="55" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>
    <rect x="210" y="55" width="80" height="48" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>

    {hotspots_svg}
    {_compass_and_scale("50m", "100m")}
</svg>"""

    def _synth_riverfront_promenade(self) -> str:
        """Procedural Waterfront & Arts Festival Map"""
        r = self.rng
        hotspots = [
            ("A", r.randint(85, 115), r.randint(290, 320)),                         # Main Stage (SW)
            ("B", r.randint(325, 355), r.randint(275, 305)),                         # Food Court (SE)
            ("C", r.randint(320, 350), r.randint(65, 90)),                           # Craft Stalls (NE)
            ("D", 250, r.randint(170, 195)),                                         # HQ Desk (Center)
            ("E", r.randint(75, 105), r.randint(75, 100)),                           # Puppet Pavilion (NW)
            ("F", r.randint(415, 435), r.randint(325, 355)),                         # River Dock
            ("G", r.randint(65, 95), r.randint(190, 220)),                           # Green Glade
            ("H", 250, r.randint(38, 55)),                                           # North Gate
        ]
        hotspots_svg = "\n    ".join(_hotspot(letter, x, y) for letter, x, y in hotspots)

        return f"""<svg id="cambridgeMapSvg" viewBox="0 0 500 400" style="width:100%; height:auto; display:block; background:#ffffff;">
    <rect width="500" height="400" fill="#ffffff"/>
    <rect x="18" y="12" width="464" height="370" fill="none" stroke="#000000" stroke-width="2.5"/>

    <!-- River on East Side -->
    <path d="M 405 12 Q 385 100 395 200 Q 410 300 400 382" fill="none" stroke="#000000" stroke-width="2"/>
    <path d="M 445 12 Q 425 100 435 200 Q 450 300 440 382" fill="none" stroke="#000000" stroke-width="1.5"/>
    <rect x="405" y="12" width="40" height="370" fill="#e0ecf4" opacity="0.35"/>
    <text x="425" y="195" font-size="9.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000" transform="rotate(90,425,195)">River Avon</text>

    <!-- South Promenade & Entrance -->
    <rect x="190" y="325" width="120" height="55" fill="#f1f5f9" stroke="#000000" stroke-width="0.9"/>
    <text x="250" y="396" text-anchor="middle" font-size="9" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">South Main Promenade Entrance</text>

    <!-- Walkway Spine -->
    <rect x="238" y="60" width="24" height="265" fill="#f1f5f9" stroke="#000000" stroke-width="0.6"/>
    <line x1="45" y1="185" x2="405" y2="185" stroke="#000000" stroke-width="0.8" stroke-dasharray="5,3"/>

    <!-- Stage (SW) -->
    <rect x="35" y="265" width="135" height="85" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>
    <polygon points="50,280 150,280 100,265" fill="#f1f5f9" stroke="#000000" stroke-width="0.8"/>
    <text x="102" y="328" text-anchor="middle" font-size="8" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Main Stage Arena</text>

    <!-- Food Court (SE) -->
    <rect x="295" y="260" width="95" height="85" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>
    <text x="342" y="325" text-anchor="middle" font-size="7.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Food Court</text>

    <!-- Craft Stalls (NE) -->
    <rect x="290" y="35" width="95" height="90" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>
    <text x="338" y="115" text-anchor="middle" font-size="7.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Craft Stalls</text>

    <!-- Volunteer HQ (Center) -->
    <rect x="195" y="150" width="110" height="70" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>
    <text x="250" y="185" text-anchor="middle" font-size="7.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Volunteer HQ</text>

    <!-- Puppet Pavilion (NW) -->
    <polygon points="45,115 135,115 90,40" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>
    <text x="90" y="132" text-anchor="middle" font-size="7.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Puppet Pavilion</text>

    {hotspots_svg}
    {_compass_and_scale("30m", "60m")}
</svg>"""

    def _synth_botanic_gardens(self) -> str:
        """Procedural Botanic Gardens & Glasshouse Map"""
        r = self.rng
        pond_rx = r.randint(42, 50)
        pond_ry = r.randint(26, 34)

        hotspots = [
            ("A", r.randint(85, 115), r.randint(240, 270)),                         # Palm Glasshouse (SW)
            ("B", r.randint(205, 235), r.randint(220, 245)),                        # Orchid Nursery
            ("C", r.randint(370, 400), r.randint(285, 315)),                        # Medicinal Herb Garden (SE)
            ("D", 250, r.randint(85, 105)),                                          # Alpine Rockery (North)
            ("E", r.randint(380, 410), r.randint(70, 95)),                          # Seed Bank (NE)
            ("F", r.randint(75, 95), r.randint(80, 105)),                           # Rose Garden (NW)
            ("G", r.randint(325, 355), r.randint(170, 195)),                        # East Pergola
            ("H", r.randint(135, 165), r.randint(335, 360)),                        # South Lawn
        ]
        hotspots_svg = "\n    ".join(_hotspot(letter, x, y) for letter, x, y in hotspots)

        return f"""<svg id="cambridgeMapSvg" viewBox="0 0 500 400" style="width:100%; height:auto; display:block; background:#ffffff;">
    <rect width="500" height="400" fill="#ffffff"/>
    <rect x="18" y="12" width="464" height="370" fill="none" stroke="#000000" stroke-width="2.5"/>
    <text x="250" y="396" text-anchor="middle" font-size="9" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">South Palm Entrance</text>

    <!-- Lily Pond (Centre) -->
    <ellipse cx="250" cy="200" rx="{pond_rx}" ry="{pond_ry}" fill="#e0ecf4" stroke="#000000" stroke-width="1.3"/>
    <text x="250" y="204" text-anchor="middle" font-size="7.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Lily Pond</text>

    <!-- Radiating Paths -->
    <line x1="250" y1="170" x2="250" y2="40" stroke="#000000" stroke-width="0.8" stroke-dasharray="4,3"/>
    <line x1="250" y1="230" x2="250" y2="370" stroke="#000000" stroke-width="0.8" stroke-dasharray="4,3"/>
    <line x1="204" y1="200" x2="40" y2="200" stroke="#000000" stroke-width="0.8" stroke-dasharray="4,3"/>
    <line x1="296" y1="200" x2="460" y2="200" stroke="#000000" stroke-width="0.8" stroke-dasharray="4,3"/>

    <!-- Palm Glasshouse (SW) -->
    <rect x="35" y="200" width="130" height="120" fill="#ffffff" stroke="#000000" stroke-width="1.8"/>
    <path d="M 35 200 Q 100 170 165 200" fill="none" stroke="#000000" stroke-width="1.2"/>
    <text x="100" y="275" text-anchor="middle" font-size="8" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Palm Glasshouse</text>

    <!-- Orchid Nursery -->
    <rect x="180" y="200" width="85" height="75" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>
    <text x="222" y="245" text-anchor="middle" font-size="7" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Orchid Nursery</text>

    <!-- Herb Garden (SE) -->
    <rect x="325" y="250" width="125" height="100" fill="#ffffff" stroke="#000000" stroke-width="1.6" stroke-dasharray="4,3"/>
    <text x="388" y="310" text-anchor="middle" font-size="7.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Herb Beds</text>

    <!-- Alpine Rockery (North) -->
    <polygon points="190,130 310,130 250,50" fill="#f8fafc" stroke="#000000" stroke-width="1.6"/>
    <text x="250" y="105" text-anchor="middle" font-size="7.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Alpine Rockery</text>

    <!-- Seed Bank (NE) -->
    <rect x="345" y="40" width="105" height="80" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>
    <text x="398" y="85" text-anchor="middle" font-size="7.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Seed Bank</text>

    {hotspots_svg}
    {_compass_and_scale("40m", "80m")}
</svg>"""

    def _synth_adventure_park(self) -> str:
        """Procedural Adventure & Forest Park Map"""
        r = self.rng
        hotspots = [
            ("A", r.randint(390, 420), r.randint(330, 360)),                        # Bike Rental Pavilion (SE)
            ("B", 250, r.randint(170, 185)),                                         # Suspension Bridge (Center)
            ("C", r.randint(155, 185), r.randint(55, 80)),                           # Observation Bird Hide (NW)
            ("D", r.randint(365, 395), r.randint(120, 150)),                         # Wilderness Cafe (NE)
            ("E", 250, r.randint(280, 305)),                                         # First Aid Station (Center-South)
            ("F", r.randint(70, 100), r.randint(320, 345)),                          # Climbing Wall
            ("G", r.randint(50, 75), r.randint(110, 135)),                           # West Trailhead
            ("H", r.randint(135, 165), r.randint(285, 315)),                         # Campground
        ]
        hotspots_svg = "\n    ".join(_hotspot(letter, x, y) for letter, x, y in hotspots)

        return f"""<svg id="cambridgeMapSvg" viewBox="0 0 500 400" style="width:100%; height:auto; display:block; background:#ffffff;">
    <rect width="500" height="400" fill="#ffffff"/>
    <rect x="18" y="12" width="464" height="370" fill="none" stroke="#000000" stroke-width="2.5"/>
    <text x="250" y="396" text-anchor="middle" font-size="9" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Main Entrance Gate &amp; Parking</text>

    <!-- River Gorge / Mountain Stream -->
    <path d="M 18 160 Q 120 140 200 170 Q 280 200 370 175 Q 440 155 482 170" fill="none" stroke="#000000" stroke-width="2"/>
    <path d="M 18 178 Q 120 158 200 188 Q 280 218 370 193 Q 440 173 482 188" fill="none" stroke="#000000" stroke-width="1.4"/>
    <text x="120" y="152" font-size="8" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">River Canyon Gorge</text>

    <!-- Suspension Bridge -->
    <rect x="228" y="165" width="44" height="26" fill="#ffffff" stroke="#000000" stroke-width="1.8"/>
    <line x1="228" y1="165" x2="272" y2="165" stroke="#000000" stroke-width="1"/>
    <line x1="228" y1="191" x2="272" y2="191" stroke="#000000" stroke-width="1"/>
    <line x1="238" y1="165" x2="238" y2="191" stroke="#000000" stroke-width="0.7"/>
    <line x1="250" y1="165" x2="250" y2="191" stroke="#000000" stroke-width="0.7"/>
    <line x1="262" y1="165" x2="262" y2="191" stroke="#000000" stroke-width="0.7"/>

    <!-- Alpine Lake (NW) -->
    <ellipse cx="90" cy="70" rx="45" ry="28" fill="#e0ecf4" stroke="#000000" stroke-width="1.3"/>
    <text x="90" y="74" text-anchor="middle" font-size="7.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Alpine Lake</text>

    <!-- Pine Forest (NE) -->
    <circle cx="380" cy="50" r="11" fill="none" stroke="#000000" stroke-width="1"/>
    <circle cx="410" cy="42" r="10" fill="none" stroke="#000000" stroke-width="1"/>
    <circle cx="435" cy="55" r="11" fill="none" stroke="#000000" stroke-width="1"/>
    <text x="405" y="98" text-anchor="middle" font-size="8" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Pine Forest</text>

    <!-- Trails -->
    <line x1="250" y1="380" x2="250" y2="191" stroke="#000000" stroke-width="1.2" stroke-dasharray="5,3"/>
    <line x1="250" y1="165" x2="250" y2="40" stroke="#000000" stroke-width="1.2" stroke-dasharray="5,3"/>
    <line x1="50" y1="300" x2="450" y2="300" stroke="#000000" stroke-width="0.8" stroke-dasharray="5,3"/>

    <!-- Central Picnic Lawn -->
    <ellipse cx="250" cy="255" rx="50" ry="26" fill="#f8fafc" stroke="#000000" stroke-width="1.2" stroke-dasharray="4,2"/>
    <text x="250" y="258" text-anchor="middle" font-size="7.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Picnic Lawn</text>

    <!-- Buildings -->
    <rect x="365" y="325" width="85" height="45" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>
    <rect x="145" y="50" width="55" height="38" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <rect x="340" y="110" width="85" height="50" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>
    <rect x="220" y="275" width="60" height="38" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>

    {hotspots_svg}
    {_compass_and_scale("50m", "100m")}
</svg>"""

    def _synth_cycling_trail(self) -> str:
        """Procedural Cycling Trail & Valley Nature Reserve Map"""
        r = self.rng
        hotspots = [
            ("A", r.randint(60, 85), r.randint(315, 345)),                          # Bike Wash (SW)
            ("B", 250, r.randint(170, 195)),                                         # Riverside Kiosk
            ("C", r.randint(385, 415), r.randint(275, 305)),                        # Pump Track (East)
            ("D", r.randint(225, 250), r.randint(68, 92)),                          # Watermill Museum (North)
            ("E", r.randint(345, 375), r.randint(38, 62)),                          # Lookout Platform (N Ridge)
            ("F", r.randint(75, 100), r.randint(60, 85)),                           # Wildflower Meadow (NW)
            ("G", r.randint(110, 140), r.randint(260, 290)),                        # Bridleway Crossing
            ("H", r.randint(300, 330), r.randint(330, 360)),                        # South Trail Junction
        ]
        hotspots_svg = "\n    ".join(_hotspot(letter, x, y) for letter, x, y in hotspots)

        return f"""<svg id="cambridgeMapSvg" viewBox="0 0 500 400" style="width:100%; height:auto; display:block; background:#ffffff;">
    <rect width="500" height="400" fill="#ffffff"/>
    <rect x="18" y="12" width="464" height="370" fill="none" stroke="#000000" stroke-width="2.5"/>
    <text x="250" y="396" text-anchor="middle" font-size="9" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">South Car Park &amp; Trailhead</text>

    <!-- River Wye -->
    <path d="M 18 240 Q 90 210 170 230 Q 250 250 330 220 Q 410 190 482 210" fill="none" stroke="#000000" stroke-width="2"/>
    <path d="M 18 255 Q 90 225 170 245 Q 250 265 330 235 Q 410 205 482 225" fill="none" stroke="#000000" stroke-width="1.4"/>
    <text x="340" y="210" font-size="8" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">River Wye</text>

    <!-- Footbridge -->
    <rect x="238" y="235" width="24" height="28" fill="#ffffff" stroke="#000000" stroke-width="1.8"/>
    <line x1="238" y1="244" x2="262" y2="244" stroke="#000000" stroke-width="0.8"/>
    <line x1="238" y1="254" x2="262" y2="254" stroke="#000000" stroke-width="0.8"/>

    <!-- Trail Loop -->
    <path d="M 250 375 Q 80 350 50 240 Q 35 130 130 65 Q 220 25 340 35 Q 440 50 460 160 Q 470 270 380 330 Q 300 370 250 375" fill="none" stroke="#000000" stroke-width="1.3" stroke-dasharray="8,4"/>
    <text x="120" y="145" font-size="7.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">← 25km Cycling Trail Loop</text>

    <!-- Meadow (NW) -->
    <rect x="30" y="30" width="115" height="85" fill="#f8fafc" stroke="#000000" stroke-width="1" stroke-dasharray="4,3"/>
    <text x="88" y="75" text-anchor="middle" font-size="8" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Wildflower Meadow</text>

    <text x="250" y="28" text-anchor="middle" font-size="8.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Northern Panoramic Ridge</text>

    <!-- Buildings & Features -->
    <rect x="30" y="305" width="85" height="50" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>
    <rect x="210" y="160" width="80" height="50" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>
    <ellipse cx="400" cy="290" rx="42" ry="28" fill="#f1f5f9" stroke="#000000" stroke-width="1.4"/>
    <text x="400" y="293" text-anchor="middle" font-size="7.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Pump Track</text>
    <rect x="200" y="55" width="75" height="52" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>
    <polygon points="340,65 385,65 362,35" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>

    {hotspots_svg}
    {_compass_and_scale("50m", "100m")}
</svg>"""

    def _synth_indoor_complex(self) -> str:
        """Procedural Indoor Sports / Museum / Library Floorplan Map"""
        r = self.rng
        hotspots = [
            ("A", r.randint(100, 140), r.randint(85, 115)),                         # Room NW
            ("B", r.randint(360, 400), r.randint(85, 115)),                         # Room NE
            ("C", r.randint(100, 140), r.randint(285, 315)),                        # Room SW
            ("D", r.randint(360, 400), r.randint(285, 315)),                        # Room SE
            ("E", 250, r.randint(45, 60)),                                           # North Exit / Stage
            ("F", r.randint(435, 460), 205),                                         # East Wing
            ("G", r.randint(40, 65), 205),                                           # West Wing
            ("H", 250, 205),                                                         # Central Atrium
        ]
        hotspots_svg = "\n    ".join(_hotspot(letter, x, y) for letter, x, y in hotspots)

        return f"""<svg id="cambridgeMapSvg" viewBox="0 0 500 400" style="width:100%; height:auto; display:block; background:#ffffff;">
    <rect width="500" height="400" fill="#ffffff"/>
    <rect x="20" y="15" width="460" height="365" fill="none" stroke="#000000" stroke-width="2.5"/>
    <text x="250" y="394" text-anchor="middle" font-size="9.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Main Entrance &amp; Reception Foyer</text>

    <!-- Corridors -->
    <rect x="225" y="70" width="50" height="310" fill="#f1f5f9" stroke="#000000" stroke-width="1"/>
    <rect x="50" y="190" width="400" height="30" fill="#f1f5f9" stroke="#000000" stroke-width="1"/>

    <!-- Reference Halls -->
    <rect x="40" y="35" width="160" height="135" fill="#ffffff" stroke="#000000" stroke-width="1.8"/>
    <text x="120" y="60" text-anchor="middle" font-size="8.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Exhibition Wing A</text>

    <rect x="300" y="35" width="160" height="135" fill="#ffffff" stroke="#000000" stroke-width="1.8"/>
    <text x="380" y="60" text-anchor="middle" font-size="8.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Auditorium Wing B</text>

    <rect x="40" y="240" width="160" height="120" fill="#ffffff" stroke="#000000" stroke-width="1.8"/>
    <text x="120" y="265" text-anchor="middle" font-size="8.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Fitness Studio C</text>

    <rect x="300" y="240" width="160" height="120" fill="#ffffff" stroke="#000000" stroke-width="1.8"/>
    <text x="380" y="265" text-anchor="middle" font-size="8.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Hydrotherapy Pool D</text>

    {hotspots_svg}
    {_compass_and_scale("20m", "40m")}
</svg>"""

    def _synth_coastal_harbor(self) -> str:
        """Procedural Coastal Harbor & Marine Station Map"""
        r = self.rng
        hotspots = [
            ("A", r.randint(75, 105), r.randint(285, 315)),                         # Ferry Berth
            ("B", r.randint(220, 250), r.randint(245, 275)),                        # Customs & Harbor Office
            ("C", r.randint(370, 400), r.randint(280, 310)),                        # Fish Market Quay
            ("D", r.randint(360, 390), r.randint(90, 115)),                         # Lighthouse Point (NE)
            ("E", r.randint(235, 265), r.randint(55, 80)),                          # Marine Biology Station (North)
            ("F", r.randint(415, 440), r.randint(185, 215)),                        # Breakwater Wall
            ("G", r.randint(65, 95), r.randint(85, 115)),                           # Coastal Battery (NW)
            ("H", 250, r.randint(340, 365)),                                         # Harbor Plaza
        ]
        hotspots_svg = "\n    ".join(_hotspot(letter, x, y) for letter, x, y in hotspots)

        return f"""<svg id="cambridgeMapSvg" viewBox="0 0 500 400" style="width:100%; height:auto; display:block; background:#ffffff;">
    <rect width="500" height="400" fill="#ffffff"/>
    <rect x="18" y="12" width="464" height="370" fill="none" stroke="#000000" stroke-width="2.5"/>
    <text x="250" y="396" text-anchor="middle" font-size="9" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">South Harbor Esplanade Entrance</text>

    <!-- Sea / Bay Basin (North & East) -->
    <path d="M 18 180 Q 150 140 250 160 Q 350 180 482 140 L 482 12 L 18 12 Z" fill="#e0ecf4" opacity="0.4" stroke="#000000" stroke-width="1.5"/>
    <text x="250" y="80" text-anchor="middle" font-size="9.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Outer Sea Basin</text>

    <!-- Stone Breakwater Pier -->
    <path d="M 330 170 L 440 170 L 440 195 L 330 195 Z" fill="#f1f5f9" stroke="#000000" stroke-width="1.6"/>
    <text x="385" y="186" text-anchor="middle" font-size="7.5" font-weight="bold" font-family="Arial, Helvetica, sans-serif" fill="#000000">Breakwater Pier</text>

    <!-- Quayside Piers (South) -->
    <rect x="50" y="270" width="100" height="70" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>
    <rect x="190" y="235" width="120" height="65" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>
    <rect x="350" y="260" width="95" height="80" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>

    {hotspots_svg}
    {_compass_and_scale("50m", "100m")}
</svg>"""


# =========================================================================
# MASTER DISPATCH FUNCTION (SUPPORTS FIXED 14-19 & INFINITE AI MAPS)
# =========================================================================

def generate_dynamic_cambridge_svg_map(theme_hint: str = "", map_data: Optional[Dict[str, Any]] = None, book_number: Optional[int] = None) -> str:
    """
    Primary API entry point for SVG maps.
    - If a specific Cambridge Book (14-19) is requested, returns the authentic calibrated map.
    - If dynamic AI practice or custom theme is requested, generates an infinite procedural map.
    """
    # 1. Direct Book Number Mapping (for Cambridge sets 14 to 19)
    if book_number:
        try:
            b_int = int(book_number)
            from ai_engine.map_generator import (
                get_map_farley_estate,
                get_map_greenwood_sanctuary,
                get_map_riverfront_festival,
                get_map_botanic_gardens,
                get_map_south_ridge_park,
                get_map_valley_cycling_trail,
            )
            book_lookup = {
                19: get_map_farley_estate,
                18: get_map_greenwood_sanctuary,
                17: get_map_riverfront_festival,
                16: get_map_botanic_gardens,
                15: get_map_south_ridge_park,
                14: get_map_valley_cycling_trail,
            }
            if b_int in book_lookup:
                return book_lookup[b_int]()
        except Exception:
            pass

    # 2. Infinite Procedural Synthesis for any custom / AI topic or unseeded test
    seed_str = f"{theme_hint}_{random.randint(1000, 999999)}"
    synthesizer = ProceduralIELTSMapSynthesizer(seed=seed_str)
    return synthesizer.generate(theme_hint=theme_hint)
