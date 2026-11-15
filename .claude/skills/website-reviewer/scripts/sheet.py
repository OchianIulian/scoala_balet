import sys, os
from PIL import Image, ImageDraw
# sheet.py out.jpg files... — labelled contact sheet, 6 per row
files = sys.argv[2:]; th = 260; cols = 6
tiles = []
for f in files:
    im = Image.open(f).convert('RGB'); im.thumbnail((th, th)); tiles.append((os.path.basename(f), im))
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new('RGB', (cols * (th + 6), rows * (th + 24)), (30, 30, 30))
d = ImageDraw.Draw(sheet)
for i, (n, im) in enumerate(tiles):
    x, y = (i % cols) * (th + 6), (i // cols) * (th + 24)
    sheet.paste(im, (x, y + 20)); d.text((x + 2, y + 4), n, fill=(255, 255, 255))
sheet.save(sys.argv[1], quality=85)
