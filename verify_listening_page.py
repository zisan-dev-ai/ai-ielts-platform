import urllib.request

html = urllib.request.urlopen('http://127.0.0.1:8000/listening-cbt').read().decode('utf-8')
print("Status: 200 OK")
print("Total Question Cards in Listening CBT HTML:", html.count('class="q-card"'))
print("Section 1 Title present:", "Section 1: Bayview Eco-Resort" in html)
print("Section 2 Title present:", "Section 2: New Town Maritime" in html)
print("Section 3 Title present:", "Section 3: Academic Tutorial" in html)
print("Section 4 Title present:", "Section 4: Academic Lecture on Marine Bioluminescence" in html)
print("Audio Speed Buttons present:", "0.75x" in html and "1.25x" in html)
print("Transcript Drawer present:", "transcriptDrawer" in html)
