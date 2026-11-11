import urllib.request

html = urllib.request.urlopen('http://127.0.0.1:8000/reading-cbt').read().decode('utf-8')
print("Status: 200 OK")
print("Total Question Cards in HTML:", html.count('class="question-card"'))
print("Total Passage Blocks in HTML:", html.count('class="passage-block"'))
print("Passage 1 Title present:", "The Secret Life of the Urban Fox" in html)
print("Passage 2 Title present:", "The Neuroscience of Sleep Architecture" in html)
print("Passage 3 Title present:", "Artificial Intelligence in Environmental Archaeology" in html)
