import re

def fix_alignment():
    for filename in ['dark.svg', 'light.svg']:
        with open(f'd:/VSC files/Github Profile/{filename}', 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the ASCII group
        pattern = re.compile(r'(    <!-- ASCII art group with float animation -->\s*<g[^>]+>)(.*?)(    </g>)', re.DOTALL)
        
        match = pattern.search(content)
        if not match:
            print(f'Pattern not found in {filename}')
            continue
            
        start_tag = match.group(1)
        text_nodes = match.group(2)
        end_tag = match.group(3)
        
        def replace_spaces(m):
            content_text = m.group(2)
            content_text = content_text.replace(' ', '&#160;')
            return m.group(1) + content_text + '</text>'
        
        new_text_nodes = re.sub(r'(<animate[^>]+/>\n)(.*?)</text>', replace_spaces, text_nodes)
        
        # Center horizontally: change x="12" to x="15"
        new_text_nodes = new_text_nodes.replace('x="12"', 'x="15"')
        
        new_content = content[:match.start()] + start_tag + new_text_nodes + end_tag + content[match.end():]
        
        with open(f'd:/VSC files/Github Profile/{filename}', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Successfully updated {filename}')

if __name__ == "__main__":
    fix_alignment()
