import sys, os
from PIL import Image, ImageOps
# prep.py photo SRC DEST [long_edge]   -> resized JPEG, no metadata
# prep.py cutout SRC DEST [height]     -> trimmed, resized PNG
# prep.py share SRC DEST cx cy         -> 1200x630 crop centred at (cx, cy) as fractions
mode, src, dest = sys.argv[1:4]
im = ImageOps.exif_transpose(Image.open(src))
os.makedirs(os.path.dirname(dest), exist_ok=True)
if mode == 'photo':
    edge = int(sys.argv[4]) if len(sys.argv) > 4 else 1400
    im = im.convert('RGB'); im.thumbnail((edge, edge), Image.LANCZOS)
    im.save(dest, 'JPEG', quality=80, optimize=True, progressive=True)
elif mode == 'cutout':
    h = int(sys.argv[4]) if len(sys.argv) > 4 else 1000
    im = im.convert('RGBA'); im = im.crop(im.getchannel('A').point(lambda a: 255 if a > 8 else 0).getbbox())
    if im.height > h: im = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
    im.save(dest, 'PNG', optimize=True)
elif mode == 'share':
    cx, cy = float(sys.argv[4]), float(sys.argv[5])
    im = im.convert('RGB'); s = max(1200 / im.width, 630 / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = min(max(round(cx * im.width - 600), 0), im.width - 1200); y = min(max(round(cy * im.height - 315), 0), im.height - 630)
    im.crop((x, y, x + 1200, y + 630)).save(dest, 'JPEG', quality=82, optimize=True)
print(dest, Image.open(dest).size, os.path.getsize(dest) // 1024, 'KB')
