import os
import re
from PIL import Image, ImageEnhance

img_path = r'C:\Users\rihan\.gemini\antigravity-ide\brain\e5c94ef0-6ded-4fb8-8244-41c00f78e595\media__1785133679413.jpg'
img = Image.open(img_path).convert('L')

# Enhance contrast slightly for better ASCII mapping
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.2)

w, h = img.size
# width = 120 chars
# char aspect ratio ~ 0.6 (width / height)
new_w = 120
new_h = int(new_w * (h / w) * 0.6)

img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

# 16-level ASCII scale from dark to light
chars = [' ', '.', ',', ':', ';', '+', '*', '?', '%', 'S', '#', 'M', '@', '8', '0', '&']
# Invert index mapping if needed. Dark background means dark pixels should be ' ' (empty) or '.'
# Wait, the image is a person on a white background? 
# The meme is Ryan Gosling eating cereal. The background is mostly light. 
# In a dark theme SVG, a white background should probably map to empty space or light characters. 
# Let's map bright pixels to ' ' and dark pixels to '@' to invert it for dark mode, or vice versa?
# Ryan's face is light, suit is dark.
# If dark theme: face should be visible. We should map dark pixels to space, light pixels to dense characters.
# Let's check pixel at 0,0 (background).
bg_pixel = img.getpixel((0, 0))
if bg_pixel > 128:
    # Bright background. Map bright to ' ' and dark to dense.
    chars = chars[::-1]

ascii_art = []
for y in range(new_h):
    line = ''
    for x in range(new_w):
        pixel = img.getpixel((x, y))
        idx = int((pixel / 255) * 15)
        # clamp
        idx = max(0, min(15, idx))
        line += chars[idx]
    ascii_art.append(line)

# Generate XML
xml = '''    <!-- ASCII art group with float animation -->\n    <g font-family="'Cascadia Code','Fira Code','JetBrains Mono','Consolas','Courier New',monospace" font-size="6" letter-spacing="-0.03em" fill="url(#asciiGrad)" filter="url(#softGlow)" xml:space="preserve">\n      <animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="5s" repeatCount="indefinite"/>\n'''

# Total height is new_h * 6
total_height = new_h * 6
# Center it vertically in the 586px tall panel
y_start = (586 - total_height) // 2 + 10 # slightly offset

for i, line in enumerate(ascii_art):
    if not line.strip(): continue
    y = y_start + (i * 6)
    dur = 0.25
    begin = 0.1 + (i * 0.03) # faster stagger since there are 70 lines
    
    # Replace special XML characters
    line_esc = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    xml += f'''      <text x="12" y="{y}" opacity="0">\n        <animate attributeName="opacity" from="0" to="1" dur="{dur}s" begin="{begin:.2f}s" fill="freeze"/>\n{line_esc}</text>\n'''

xml += '''    </g>'''

for filename in ['dark.svg', 'light.svg']:
    with open(f'd:/VSC files/Github Profile/{filename}', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # regex match the whole g block
    pattern = re.compile(r'    <!-- ASCII art group with float animation -->\s*<g font-family=.*?</g>', re.DOTALL)
    
    if pattern.search(content):
        new_content = pattern.sub(xml, content)
        with open(f'd:/VSC files/Github Profile/{filename}', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Successfully updated {filename}')
    else:
        print(f'Pattern not found in {filename}')
