"""Build the selected hand-built wordmark as portable SVG paths."""
from pathlib import Path
import math
import re
from xml.etree import ElementTree

OUT = Path(__file__).resolve().parents[1] / 'static' / 'images'
# Each letter is drawn independently, with modest rotations and baseline shifts.
letters = [
    ('W', 'M4 8 L27 4 L39 81 L56 39 L76 42 L88 82 L102 3 L126 7 L106 116 L83 119 L65 76 L49 118 L24 115 Z', 6, 21, -5),
    ('i', 'M5 7 L28 9 L27 30 L4 28 Z M4 42 L28 41 L29 118 L3 118 Z', 143, 22, 3),
    ('z', 'M0 43 L72 40 L75 61 L36 94 L75 91 L76 115 L0 120 L-2 98 L37 65 L0 67 Z', 194, 24, -5),
    ('o', 'M35 39 L59 43 L75 61 L79 87 L70 109 L49 122 L25 119 L6 104 L0 82 L7 57 L20 44 Z M32 65 L25 75 L24 87 L31 96 L44 97 L52 87 L51 75 L44 67 Z', 350, 20, -4),
    ('o', 'M35 39 L59 43 L75 61 L79 87 L70 109 L49 122 L25 119 L6 104 L0 82 L7 57 L20 44 Z M32 65 L25 75 L24 87 L31 96 L44 97 L52 87 L51 75 L44 67 Z', 438, 24, 4),
    ('l', 'M3 5 L29 3 L27 121 L1 119 Z', 548, 20, -3),
    ('s', 'M68 46 L62 67 L34 65 L27 71 L30 78 L51 82 L66 94 L66 111 L54 122 L4 122 L6 100 L37 102 L42 97 L39 92 L17 88 L4 76 L5 55 L19 43 Z', 594, 21, 3),
]
# Trace the selected concept's hammer silhouette, including its curved claw.
def hammer_path(path):
    tokens = re.findall(r'[A-Za-z]|-?\d+(?:\.\d+)?', path)
    result = []
    i = 0
    while i < len(tokens):
        if tokens[i].isalpha():
            result.append(tokens[i]); i += 1
        else:
            result.extend([f'{(float(tokens[i])-289)*0.65:.3f}', f'{(float(tokens[i+1])-548)*0.65:.3f}'])
            i += 2
    return ' '.join(result)

face = hammer_path('M293 584 L309 578 Q313 577 314 581 L324 613 Q325 617 321 618 L305 623 Q300 624 299 619 L289 590 Q288 586 293 584 Z')
head_and_handle = hammer_path('M317 577 L341 567 C368 558 389 546 409 548 C430 550 447 562 457 582 Q458 585 455 583 C436 573 420 568 405 571 C394 575 393 578 392 587 Q391 590 383 594 L435 775 Q438 781 431 784 L407 791 Q401 793 399 786 L348 602 L326 609 Z')
hammer = f'<g transform="translate(260 9) rotate(0 0 0)" fill="#efb83f"><path d="{face}"/><path d="{head_and_handle}"/></g>'

def flatten(body):
    root = ElementTree.fromstring('<root>' + body + '</root>')
    def walk(element, transform=None):
        transform = element.attrib.get('transform', transform)
        if element.tag == 'path' and transform:
            tx, ty, angle, cx, cy = map(float, re.findall(r'-?\d+(?:\.\d+)?', transform))
            rad = math.radians(angle)
            tokens = re.findall(r'[A-Za-z]|-?\d+(?:\.\d+)?', element.attrib['d'])
            output = []
            i = 0
            while i < len(tokens):
                if tokens[i].isalpha():
                    output.append(tokens[i]); i += 1
                else:
                    x, y = float(tokens[i])-cx, float(tokens[i+1])-cy
                    output.extend([f'{tx+cx+x*math.cos(rad)-y*math.sin(rad):.3f}', f'{ty+cy+x*math.sin(rad)+y*math.cos(rad):.3f}'])
                    i += 2
            element.set('d', ' '.join(output))
        element.attrib.pop('transform', None)
        for child in element:
            walk(child, transform)
    walk(root)
    return ''.join(ElementTree.tostring(child, encoding='unicode') for child in root)

def svg(body, viewbox, title):
    body = flatten(body)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" role="img" aria-labelledby="title"><title id="title">{title}</title>{body}</svg>\n'''

for name, color in [('wiztools-logo', '#fff7e9'), ('wiztools-logo-light', '#252525')]:
    body = ''.join(f'<path aria-label="{letter}" fill="{color}" fill-rule="evenodd" d="{path}" transform="translate({x} {y}) rotate({angle} 40 75)"/>' for letter,path,x,y,angle in letters)
    data = svg(body + hammer, '0 0 680 175', 'WizTools — hand-built wordmark with angled hammer T')
    ElementTree.fromstring(data)
    (OUT / f'{name}.svg').write_text(data)
icon = hammer.replace('translate(260 9)', 'translate(10 12)')
(OUT / 'wiztools-icon.svg').write_text(svg(icon, '0 0 165 175', 'WizTools hammer T'))
