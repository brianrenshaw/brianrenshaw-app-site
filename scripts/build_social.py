#!/usr/bin/env python3
"""Render the homepage share card from bundled fonts and project icons (Pillow)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
SCALE = 2
canvas = Image.new('RGB', (2400, 1260), '#f7f6f2')
draw = ImageDraw.Draw(canvas)
def font(size, serif=False):
    path = 'reading-habit/assets/fonts/Lora[wght].ttf' if serif else 'where-do-we-eat/assets/fonts/Archivo[wdth,wght].ttf'
    return ImageFont.truetype(str(SITE / path), size * SCALE)
def text(x,y,value,size,color='#282b28',serif=False):
    draw.text((x*SCALE,y*SCALE),value,font=font(size,serif),fill=color)
def rect(box,fill,radius=0,outline=None,width=1):
    draw.rounded_rectangle(tuple(v*SCALE for v in box),radius*SCALE,fill=fill,outline=outline,width=width*SCALE)
def polygon(points,fill):
    draw.polygon([(x*SCALE,y*SCALE) for x,y in points],fill=fill)
def icon(x,y,path=None,kind=None):
    if path:
        image=Image.open(SITE/path).convert('RGBA').resize((112,112),Image.Resampling.LANCZOS)
        mask=Image.new('L',(112,112));ImageDraw.Draw(mask).rounded_rectangle((0,0,111,111),22,fill=255)
        canvas.paste(image,(x*SCALE,y*SCALE),mask)
    elif kind=='blog':
        rect((x,y,x+56,y+56),'#ffffff',12)
        polygon([(x+28,y+5),(x+51,y+28),(x+28,y+51),(x+5,y+28)],'#0C2340')
        polygon([(x+28,y+6),(x+50,y+28),(x+28,y+50),(x+6,y+28)],'#C41E3A')
        for dx in [18,29]:
            polygon([(x+dx,y+21),(x+dx+3,y+21),(x+dx+3,y+33),(x+dx+9,y+33),(x+dx+9,y+36),(x+dx,y+36)],'#ffffff')
        for dx,dy in [(28,9),(47,28),(28,47),(9,28)]:
            polygon([(x+dx,y+dy-2),(x+dx+2,y+dy),(x+dx,y+dy+2),(x+dx-2,y+dy)],'#ffffff')
    elif kind=='books':
        rect((x,y,x+56,y+56),'#f2efe8',12)
        for dy in [18,26,34,42]:
            draw.line([((x+11)*SCALE,(y+dy)*SCALE),((x+31 if dy<42 else x+24)*SCALE,(y+dy)*SCALE)],fill='#1a1715',width=3)
        draw.text(((x+35)*SCALE,(y+6)*SCALE),'?',font=ImageFont.truetype(str(SITE/'reading-habit/assets/fonts/Lora[wght].ttf'),34*SCALE),fill='#8c2b18')
    else:
        rect((x,y,x+56,y+56),'#f3f8fc',12)
        rect((x+12,y+12,x+44,y+44),None,3,'#365e83',2)
        for points in [[(12,22),(44,22)],[(12,33),(44,33)],[(23,22),(23,44)],[(34,22),(34,44)]]:
            draw.line([((x+dx)*SCALE,(y+dy)*SCALE) for dx,dy in points],fill='#365e83',width=4)
text(48,22,'BRIAN RENSHAW',18)
text(48,46,'A few things I wanted to exist.',40,serif=True)
text(48,100,'Apps, tools, and experiments built with AI.',18,'#65685f')
# Ingest and Decks lead as a featured pair, matching the homepage, each with
# its own site hero: a MacBook for Ingest, the device trio for Decks. The other nine sit in a 3x3 grid.
featured=[
 ('Ingest','Mac app · Free during beta','Modern photo\nmanagement for Mac.','#fffefb','#242622','#86520b','ingest/assets/icon.png','assets/featured-ingest-0.9.8.webp'),
 ('Decks','iPhone, iPad & Mac · Public beta','Give your photos the\npresentation they deserve.','#eae8e2','#242422','#242422','decks/assets/icon.png','assets/featured-decks-devices-oct06.webp'),
]
for i,(name,kind,tagline,bg,ink,accent,path,shot) in enumerate(featured):
    x=48+i*558;y=140;w=546;h=156
    rect((x,y,x+w,y+h),bg,outline='#e2e0d8' if bg=='#fffefb' else None)
    icon(x+20,y+20,path)
    text(x+90,y+24,name,20,ink)
    text(x+90,y+52,kind,14,accent)
    for n,line in enumerate(tagline.split('\n')):text(x+20,y+94+n*26,line,19,ink)
    image=Image.open(SITE/shot).convert('RGBA');width=218*SCALE
    image=image.resize((width,round(image.height*width/image.width)),Image.Resampling.LANCZOS)
    canvas.paste(image,((x+w-218-12)*SCALE,(y+h)*SCALE-image.height-10*SCALE),image)
projects=[
 ('Folio','iOS app','#ffdbb5','#57331f','folio/assets/icon.png',None),
 ('Who’s First?','iOS app','#bde0d2','#163f3c','whos-first/assets/icon-native.png',None),
 ('Reading Habit','iOS app','#f2dfae','#363127','reading-habit/assets/icon-native.png',None),
 ('Where Do We Eat','iOS app','#fff3df','#482b25','where-do-we-eat/assets/app-icon.png',None),
 ('Canceled','iOS app','#142d4e','#fffdf6','canceled/assets/icon.png',None),
 ('Walkthrough','Mac app','#d5eeeb','#183b3b','walkthrough/assets/icon-1.4.1.png',None),
 ('Lankford Legends','Blog','#ffffff','#0C2340',None,'blog'),
 ('What Did They Read?','Blog','#f2efe8','#1a1715',None,'books'),
 ('Spreadsheet Tools','Utility','#d5e6f4','#293f55',None,'utility'),
]
for i,(name,kind,bg,ink,path,symbol) in enumerate(projects):
    x=48+(i%3)*372;y=312+(i//3)*94
    rect((x,y,x+360,y+84),bg)
    icon(x+14,y+14,path,symbol)
    text(x+84,y+20,name,17,ink)
    text(x+84,y+46,kind,14,ink)
text(48,596,'brianrenshaw.app',16,'#65685f')
canvas.resize((1200,630),Image.Resampling.LANCZOS).save(SITE/'assets/social-projects-v12.png',optimize=True)
