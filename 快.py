import re

import cv2
from pathlib import Path
from PIL import Image


d = {}


for i in [*Path('.').glob('**/*.jpg'), *Path('.').glob('**/*.png')]:
    img = cv2.imread(str(i))
    if max(img.shape) > 2000:
        r = 2000 / max(img.shape)
        img = cv2.resize(img, [int(img.shape[1]*r), int(img.shape[0] * r)], interpolation=cv2.INTER_AREA)
    for q in range(80, 20, -10):
        cv2.imwrite(str(i.with_suffix('.webp')), img, [cv2.IMWRITE_WEBP_QUALITY, q])
        if i.with_suffix('.webp').stat().st_size < 512 * 1024:
            break
    d[str(i).replace('\\', '/')] = Image.open(i).info


def repl(x):
    name = x.groupdict()['name']
    parameters = d[name].get('parameters', '')
    return f'![{repr(parameters)}]({Path(name).with_suffix(".webp")})'

with open('readme.md', encoding='utf8') as f:
    s = f.read()
s = re.sub(r'!\[.*?\]\((?P<name>.+?\.((png)|(jpg)))\)', repl, s)

s = s.replace('fuku/alice.png', 'fuku/alice.webp')    # 这个不是markdown格式，手动改1下

with open('readme.md', 'w', encoding='utf8') as f:
    f.write(s)
