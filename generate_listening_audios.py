# -*- coding: utf-8 -*-
import os
import sys
import urllib.request
import urllib.parse
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(__file__)
AUDIO_DIR = os.path.join(BASE_DIR, "static", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

transcripts = {
    1: "Good morning, Bayview Eco-Lodge and Activity Centre. How may I assist you? Hello, I would like to book accommodation for my family for next month. Could I have your surname, please? Yes, it's Henderson, H-E-N-D-E-R-S-O-N. And your contact telephone number? It is 07911 802341. What date are you checking in? On the 18th of October, staying for 4 nights. We would like the Pine Log Cabin for two adults and two children. My son has a severe nut allergy and my wife is dairy-free. We want to reserve the Forest Canopy Zipline departing from Base Camp Station B. The required holding deposit is 120 pounds.",
    
    2: "Welcome everyone to the New Town Maritime Heritage Museum. Please look at your orientation map. We are standing at the South Entrance. To your immediate left is the Audio-Visual Theater, where a 15-minute documentary plays continuously. In the northwest corner, letter B is the Model Ship Workshop. Directly opposite in the northeast corner, letter C is the Harbor View Cafe overlooking the docks. Letter D along the east corridor is the Children's Discovery Zone. Letter E immediately to the right of the South Entrance is the Museum Souvenir and Book Shop. Admission to all historical galleries is free.",
    
    3: "Welcome Jack and Maya. Let us examine your engineering thesis on localized solar microgrids for rural health clinics. In tropical climates, ambient temperatures exceeding 42 degrees Celsius cause severe thermal stress and electrode passivation in lithium-ion batteries. In Chapter 3, Jack evaluates rooftop shaded solar chimneys, which create natural convective airflow without consuming auxiliary electricity. Maya's embedded microcontroller prioritizes power by shedding non-essential loads when the battery state of charge drops below 35 percent, preserving power for medical refrigeration. We will compare lithium-iron-phosphate against sodium-sulfur battery lifecycle costs.",
    
    4: "Welcome students. Today we examine marine bioluminescence in the ocean bathypelagic zone. In deep waters between 200 and 1,000 meters, over 90 percent of macro-organisms produce cold light. The biochemical reaction requires two components: luciferin pigment and luciferase enzyme catalyst, producing oxyluciferin and cold blue-green photons at 470 nanometers wavelength. Lanternfish use ventral photophores for counter-illumination camouflage to erase their dark silhouette. Deep-sea anglerfish possess an illuminated dorsal esca lure containing symbiotic bacteria. Siphonophores eject glowing clouds of mucus for startle defense. In medical biotechnology, cloned luciferase genes track real-time tumor angiogenesis and drug resistance."
}

def split_text(text, max_len=140):
    sentences = re.split(r'(?<=[.?!])\s+', text)
    chunks = []
    current = ""
    for s in sentences:
        if len(current) + len(s) + 1 <= max_len:
            current = (current + " " + s).strip()
        else:
            if current:
                chunks.append(current)
            current = s
    if current:
        chunks.append(current)
    return chunks

def generate_mp3_files():
    for sec_num, text in transcripts.items():
        filename = f"section{sec_num}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)
        chunks = split_text(text)
        
        full_audio_bytes = bytearray()
        for idx, chunk in enumerate(chunks):
            try:
                url = f"https://translate.googleapis.com/translate_tts?ie=UTF-8&q={urllib.parse.quote(chunk)}&tl=en-US&client=tw-ob"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    full_audio_bytes.extend(resp.read())
            except Exception as e:
                print(f"Error fetching chunk {idx} for Section {sec_num}: {e}")
        
        if len(full_audio_bytes) > 0:
            with open(filepath, 'wb') as f:
                f.write(full_audio_bytes)
            print(f"SUCCESS: Generated {filename} ({len(full_audio_bytes)} bytes)")
        else:
            print(f"FAILED: {filename}")

if __name__ == "__main__":
    generate_mp3_files()
