"""Draw an original broadsheet-style front page for Friday 13 November 2026."""
from pathlib import Path
import random
from PIL import Image, ImageDraw, ImageFont

random.seed(13)
W = H = 1024
PAPER = (244, 237, 218)
INK = (25, 29, 29)
SOFT = (77, 79, 73)
RED = (157, 43, 43)
BLUE = (36, 87, 116)
GOLD = (193, 137, 48)
GREEN = (70, 112, 81)
TEAL = (36, 119, 119)
PURPLE = (117, 74, 117)
COLORS = {"Americas": BLUE, "Europe": RED, "Mideast": GOLD,
          "Asia": GREEN, "Africa": PURPLE, "Oceania": TEAL}
DISPLAY = "/usr/share/fonts/truetype/sand-box/google/Playfair Display/PlayfairDisplay-VariableFont_wght.ttf"
HEAD = "/usr/share/fonts/truetype/sand-box/custom/Source Serif Pro/SourceSerifPro-Bold.ttf"
BODY = "/usr/share/fonts/truetype/sand-box/google/Merriweather/Merriweather-VariableFont_opsz,wdth,wght.ttf"
LABEL = "/usr/share/fonts/truetype/sand-box/google/Oswald/Oswald-VariableFont_wght.ttf"

im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)
for _ in range(1800):
    px, py = random.randrange(W), random.randrange(H)
    bump = random.choice((-4, -2, 2, 4))
    d.point((px, py), fill=tuple(max(0, min(255, c+bump)) for c in PAPER))

def f(path, size):
    return ImageFont.truetype(path, size)

def text(x, y, value, size, color=INK, face=BODY, anchor=None):
    d.text((x, y), value, font=f(face, size), fill=color, anchor=anchor)

def wrapped(value, face, size, width):
    ft = f(face, size)
    lines, current = [], ""
    for word in value.split():
        candidate = (current + " " + word).strip()
        if d.textlength(candidate, font=ft) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def paragraph(x, y, value, size, width, color=INK, face=BODY, leading=2, limit=None):
    lines = wrapped(value, face, size, width)
    if limit is not None:
        lines = lines[:limit]
    ft = f(face, size)
    for i, line in enumerate(lines):
        d.text((x, y+i*(size+leading)), line, font=ft, fill=color)
    return len(lines)*(size+leading)

def line(y, x0=28, x1=996, width=3):
    d.line((x0, y, x1, y), fill=INK, width=width)

def card(x, y, w, h, fill=(238, 226, 201)):
    d.rounded_rectangle((x, y, x+w, y+h), radius=8, fill=fill, outline=(133, 123, 103), width=1)

def plane(cx, cy, scale=1, color=(232, 239, 237)):
    pts=[(-43,2),(-4,-4),(10,-22),(17,-21),(13,-5),(39,-11),(45,-7),(17,3),(13,13),(24,19),(23,23),(6,17),(-3,8),(-40,9)]
    d.polygon([(cx+int(a*scale),cy+int(b*scale)) for a,b in pts], fill=color)

def lead_art(kind, x, y, w, h):
    # Saturated ink panels give the three lead packages a strong visual anchor.
    backgrounds={"plane":(34,76,98),"radar":(48,74,80),"flags":(50,82,78)}
    d.rounded_rectangle((x,y,x+w,y+h),radius=6,fill=backgrounds[kind])
    if kind == "plane":
        # Electronic departure board and grounded aircraft above a closed runway.
        bx, by = x+12, y+10
        d.rounded_rectangle((bx,by,bx+126,by+54),radius=3,fill=(18,37,48),outline=(108,146,153),width=1)
        text(bx+8,by+4,"US DEPARTURES",9,(199,213,206),LABEL)
        d.line((bx+6,by+18,bx+118,by+18),fill=(93,112,111),width=1)
        text(bx+8,by+21,"GROUNDED",17,(242,109,84),LABEL)
        text(bx+8,by+41,"HELD · ALL GATES",8,(237,200,130),LABEL)
        plane(x+219,y+35,1.0,(242,239,224))
        d.ellipse((x+185,y+13,x+199,y+27),fill=(239,172,69))
        # Shut runway bars and closed stop gates
        d.polygon([(x+151,y+57),(x+w-12,y+48),(x+w-12,y+62),(x+151,y+71)],fill=(29,42,45))
        for xx in range(x+166,x+w-15,22):
            d.line((xx,y+57,xx+4,y+56),fill=(244,223,166),width=2)
        d.line((x+277,y+48,x+277,y+72),fill=(211,71,59),width=4)
        d.line((x+267,y+51,x+287,y+50),fill=(211,71,59),width=4)
    elif kind == "radar":
        # Filled dish, two incoming aircraft, and an explicit claims/denial key.
        d.ellipse((x+18,y+14,x+82,y+67),fill=(193,137,48))
        d.pieslice((x+22,y+17,x+78,y+64),190,350,fill=(92,164,162))
        d.line((x+50,y+40,x+87,y+8),fill=(230,239,228),width=4)
        d.line((x+50,y+42,x+50,y+69),fill=(224,230,217),width=5)
        d.line((x+31,y+69,x+69,y+69),fill=(224,230,217),width=5)
        plane(x+113,y+20,.42,(229,181,91))
        plane(x+144,y+43,.40,(127,194,197))
        d.rounded_rectangle((x+178,y+8,x+w-9,y+34),radius=4,fill=(132,48,43))
        text(x+185,y+12,"IRAN CLAIMS HIT",9,(255,244,228),LABEL)
        d.rounded_rectangle((x+178,y+42,x+w-9,y+68),radius=4,fill=(210,225,214))
        text(x+185,y+46,"US: NO DAMAGE",9,(35,72,74),LABEL)
    else:
        # Three recognizable flags above a dark podium, names and summit location.
        flag_x=[x+38,x+123,x+208]
        names=[("TRUMP","US"),("XI","CHINA"),("PUTIN","RUSSIA")]
        for i,(who,country) in enumerate(names):
            fx=flag_x[i]
            d.line((fx+25,y+8,fx+25,y+51),fill=(236,230,208),width=2)
            if i == 0:
                d.rectangle((fx+27,y+11,fx+70,y+36),fill=(244,240,224))
                for sy in (14,19,24,29,34): d.rectangle((fx+27,y+sy,fx+70,y+sy+2),fill=(180,54,50))
                d.rectangle((fx+27,y+11,fx+45,y+24),fill=(45,79,117))
            elif i == 1:
                d.rectangle((fx+27,y+11,fx+70,y+36),fill=(184,47,42))
                d.polygon([(fx+36,y+14),(fx+39,y+20),(fx+45,y+20),(fx+40,y+24),(fx+42,y+30),(fx+36,y+26),(fx+31,y+30),(fx+33,y+24),(fx+28,y+20),(fx+34,y+20)],fill=(241,197,75))
            else:
                d.rectangle((fx+27,y+11,fx+70,y+19),fill=(237,237,229))
                d.rectangle((fx+27,y+19,fx+70,y+28),fill=(65,96,143))
                d.rectangle((fx+27,y+28,fx+70,y+36),fill=(171,61,53))
            text(fx+49,y+39,who,9,(255,245,221),LABEL,"mt")
            text(fx+49,y+50,country,8,(216,221,205),LABEL,"mt")
        d.polygon([(x+15,y+70),(x+w-15,y+70),(x+w-28,y+82),(x+28,y+82)],fill=(171,119,49))
        text(x+w//2,y+69,"APEC  ·  SHENZHEN",10,(255,244,220),LABEL,"mt")

# Newspaper masthead
text(30,13,"THE WORLD'S NEWS IN ONE PICTURE",15,RED,LABEL)
text(994,13,"30 STORIES  ·  6 CONTINENTS  ·  ALL FROM FRIDAY",12,INK,LABEL,"ra")
text(27,34,"Friday 13 November 2026",58,INK,DISPLAY)
text(32,101,"A world held at the edge of disruption and diplomacy",15,SOFT,BODY)
line(128,width=4)

leads=[
 ("UNITED STATES · AVIATION","FAA grounds all US departures as air-traffic telecoms fail","Nationwide stop from about 3:54 p.m. ET, lifted about 8:15 p.m. ET (~4½ hours). Thousands of flights delayed or cancelled. Officials: no sign of an attack.","plane"),
 ("MIDDLE EAST · IRAN","Iran says it hit a US radar in Bahrain; US denies it","Guards claim a radar was destroyed; CENTCOM says it shot down two drones and there was no damage. Iran also says a tanker hit a mine near Hormuz (unverified).","radar"),
 ("ASIA · DIPLOMACY","Trump, Xi and Putin to meet in China next week","White House: first three-way talks, on the sidelines of APEC in Shenzhen; nuclear arms are on the agenda.","flags"),
]
lx,lw,lgap,ly,lh=28,312,16,140,267
for i,(tag,headline,dek,art) in enumerate(leads):
    x=lx+i*(lw+lgap)
    card(x,ly,lw,lh,(235,222,195))
    text(x+11,ly+7,f"{i+1:02d}  /  {tag}",11,RED,LABEL)
    lead_art(art,x+10,ly+29,lw-20,84)
    hy=ly+120
    hh=paragraph(x+11,hy,headline,20,lw-22,INK,HEAD,0,3)
    paragraph(x+11,hy+hh+4,dek,10,lw-22,SOFT,BODY,1,6)

line(415,width=4)
stories=[
 ("SCIENCE · SPACE","Starship Flight 15 orbits; catch aborted","26 Starlinks; booster splashes in Gulf.","rocket"),
 ("EUROPE · UKRAINE","Russian strike sets Kyiv hospital on fire","About 30 evacuated; other cities hit.","hospital"),
 ("EUROPE · DIPLOMACY","Europe names team for Ukraine peace talks","Six-nation adviser team follows US talks.","globe"),
 ("SOUTH AMERICA · FAITH","Pope Leo XIV says Mass in Chiclayo","Vatican: about 500,000 at Mass.","pope"),
 ("MARKETS · TECH","Nvidia below $4T after Huang quits","Kress interim; Congress summons Huang.","chart"),
 ("ASIA · INDIA","Bus-truck crash near Kaziranga kills 24+","Head-on crash; students among the dead.","bus"),
 ("UNITED STATES · ACCIDENT","Tanker hits New Orleans cruise boat","All survive; 30 hospitalized.","boat"),
 ("TECH · WORLD","Microsoft 365 outage hits 74 countries","Day-long disruption; broad recovery.","cloud"),
]

def mini(kind,x,y):
    c=(37,70,75)
    if kind=="rocket":
        d.ellipse((x+3,y+2,x+43,y+42),fill=(211,229,223))
        d.polygon([(x+23,y+5),(x+32,y+21),(x+29,y+34),(x+17,y+34),(x+14,y+21)],fill=RED)
        d.ellipse((x+20,y+16,x+26,y+22),fill=(214,231,229))
        d.polygon([(x+17,y+32),(x+10,y+43),(x+22,y+38)],fill=GOLD)
        d.polygon([(x+29,y+32),(x+36,y+43),(x+24,y+38)],fill=GOLD)
    elif kind=="hospital":
        d.rectangle((x+7,y+9,x+41,y+41),fill=(223,211,183),outline=c,width=1)
        d.rectangle((x+21,y+3,x+27,y+18),fill=RED); d.rectangle((x+16,y+8,x+32,y+14),fill=RED)
        d.rectangle((x+12,y+23,x+18,y+29),fill=(87,147,165));d.rectangle((x+30,y+23,x+36,y+29),fill=(87,147,165))
    elif kind=="globe":
        d.ellipse((x+4,y+4,x+42,y+42),fill=(192,215,202),outline=c,width=1)
        d.arc((x+14,y+4,x+32,y+42),90,270,fill=c,width=2);d.arc((x+14,y+4,x+32,y+42),270,90,fill=c,width=2)
        d.line((x+5,y+23,x+41,y+23),fill=c,width=2)
    elif kind=="pope":
        d.ellipse((x+15,y+5,x+31,y+21),fill=(211,185,145))
        d.polygon([(x+8,y+23),(x+23,y+16),(x+38,y+23),(x+34,y+41),(x+12,y+41)],fill=(248,244,227),outline=c)
        d.line((x+23,y+24,x+23,y+38),fill=GOLD,width=3)
    elif kind=="chart":
        for i,h0 in enumerate((15,25,31,37)):
            d.rectangle((x+4+i*9,y+40-h0,x+11+i*9,y+40),fill=(83,142,99))
        d.line((x+3,y+31,x+14,y+25,x+23,y+28,x+39,y+7),fill=RED,width=3)
    elif kind=="bus":
        d.rounded_rectangle((x+3,y+10,x+44,y+34),radius=4,fill=(198,147,53),outline=c,width=1)
        d.rectangle((x+8,y+14,x+39,y+24),fill=(161,197,197))
        d.ellipse((x+9,y+31,x+18,y+40),fill=c);d.ellipse((x+31,y+31,x+40,y+40),fill=c)
    elif kind=="boat":
        d.rectangle((x+10,y+10,x+37,y+27),fill=(233,225,204),outline=c,width=1)
        d.rectangle((x+14,y+14,x+21,y+21),fill=(91,153,171));d.rectangle((x+26,y+14,x+33,y+21),fill=(91,153,171))
        d.polygon([(x+3,y+28),(x+44,y+28),(x+36,y+39),(x+12,y+39)],fill=BLUE)
    elif kind=="cloud":
        d.ellipse((x+6,y+12,x+30,y+35),fill=(178,200,198),outline=c)
        d.ellipse((x+18,y+5,x+43,y+34),fill=(178,200,198),outline=c)
        d.rectangle((x+12,y+22,x+38,y+34),fill=(178,200,198))
        text(x+25,y+31,"365",8,RED,LABEL,"mm")

cw,ch,cgap,sx,sy=234,91,10,28,428
for i,(tag,headline,dek,kind) in enumerate(stories):
    row,col=divmod(i,4)
    x,y=sx+col*(cw+cgap),sy+row*(ch+7)
    card(x,y,cw,ch,(239,228,205))
    mini(kind,x+8,y+38)
    text(x+57,y+6,f"{i+4:02d}  {tag}",9,RED,LABEL)
    hh=paragraph(x+57,y+20,headline,17,cw-65,INK,HEAD,0,3)
    paragraph(x+57,y+23+hh,dek,8,cw-65,SOFT,BODY,0,1)

line(625,width=4)
text(31,635,"WHERE IT HAPPENED",16,INK,LABEL)
text(493,635,"ALSO ON FRIDAY 13 NOVEMBER",16,INK,LABEL)
d.line((480,636,480,966),fill=INK,width=2)

# Ocean field and six clear, simplified continent silhouettes.
mx,my,mw,mh=31,666,435,266
d.rounded_rectangle((mx,my,mx+mw,my+mh),radius=8,fill=(211,226,222),outline=(42,75,79),width=2)
def continent(points):
    d.polygon([(mx+a,my+b) for a,b in points],fill=(214,204,176),outline=(87,99,84),width=2)
# North America, including Alaska and the taper into Central America
continent([(17,56),(29,43),(45,40),(56,29),(81,30),(91,38),(110,37),(130,48),(129,62),(116,69),(111,81),(97,85),(91,98),(82,112),(75,128),(67,143),(59,134),(57,120),(48,111),(44,95),(35,86),(29,72),(17,68),(10,61)])
# South America is long, narrow, and tapers southward
continent([(89,129),(108,128),(122,139),(128,155),(124,173),(118,187),(112,205),(105,222),(98,211),(96,192),(90,177),(87,158),(82,145)])
# Greenland
continent([(133,24),(145,17),(160,23),(157,39),(145,47),(136,41)])
# Europe
continent([(207,62),(218,53),(231,55),(238,61),(250,59),(258,67),(251,74),(240,73),(234,81),(222,77),(216,85),(207,78),(201,69)])
# Africa
continent([(217,88),(234,82),(250,88),(262,101),(260,119),(253,138),(246,157),(237,176),(229,166),(223,149),(218,133),(211,116),(209,100)])
# Asia: broad northern landmass with the Indian and Southeast Asian peninsulas
continent([(252,56),(265,45),(282,42),(295,34),(316,37),(329,31),(350,39),(370,40),(388,51),(410,54),(422,65),(413,74),(397,77),(384,86),(369,83),(357,91),(343,83),(333,93),(319,86),(306,91),(294,82),(282,86),(270,77),(259,78)])
continent([(304,91),(317,95),(322,109),(318,120),(311,115),(307,104)])
continent([(344,89),(357,91),(364,102),(358,108),(349,102)])
# Australia and nearby islands are deliberately prominent and unmistakable
continent([(355,157),(369,147),(390,149),(406,158),(408,172),(398,182),(381,185),(367,178),(355,169)])
d.ellipse((417+mx,139+my,424+mx,144+my),fill=(214,204,176),outline=(87,99,84))

# Dots carry story numbers only. Small offsets spread dense regions without labels.
pins=[
 (1,53,65,"Americas"),(2,261,91,"Mideast"),(3,344,72,"Asia"),(4,75,75,"Americas"),
 (5,211,59,"Europe"),(6,247,59,"Europe"),(7,111,164,"Americas"),(8,91,43,"Americas"),
 (9,337,102,"Asia"),(10,63,91,"Americas"),(11,294,63,"Asia"),(12,105,53,"Americas"),
 (13,288,99,"Mideast"),(14,42,73,"Americas"),(15,242,128,"Africa"),(16,87,90,"Americas"),
 (17,117,73,"Americas"),(18,50,105,"Americas"),(19,268,119,"Mideast"),(20,384,93,"Asia"),
 (21,388,166,"Oceania"),(22,319,130,"Asia"),(23,211,82,"Europe"),(24,247,82,"Europe"),
 (25,288,119,"Mideast"),(26,349,105,"Asia"),(27,278,139,"Mideast"),(28,72,106,"Americas"),
 (29,394,55,"Asia"),(30,229,65,"Europe")]
for number,px,py,region in pins:
    xx,yy=mx+px,my+py
    color=COLORS[region]
    d.ellipse((xx-8,yy-8,xx+8,yy+8),fill=color,outline=(250,246,230),width=1)
    d.text((xx,yy),str(number),font=f(LABEL,8),fill=(255,255,248),anchor="mm")
for i,(label,color) in enumerate(COLORS.items()):
    col=i%3; row=i//3
    xx=mx+11+col*139; yy=my+220+row*16
    d.ellipse((xx,yy+3,xx+10,yy+13),fill=color)
    text(xx+15,yy,label,10,INK,LABEL)

also=[
 (12,"US","Court reviews Trump's asylum order"),
 (13,"GAZA","Infant dies of cold; nations urge more aid"),
 (14,"ECON","US producer prices +6.5%, most since 2022"),
 (15,"AFRICA","Nairobi building collapse: at least 6 dead"),
 (16,"CULTURE","Rosalía wins Latin Grammy album of year, Lux"),
 (17,"US","Scott Colom: Mississippi's first Dem senator since '82"),
 (18,"SPORT","Pochettino leaves US team for Manchester United"),
 (19,"MIDEAST","Houthis claim new drone/missile strikes in Saudi"),
 (20,"ASIA","Taiwan says unannounced China drills; 100+ ships"),
 (21,"OCEANIA","Nauru president: all opposition MPs joined govt"),
 (22,"ASIA","Pakistan van into Gilgit river; 11 dead"),
 (23,"EUROPE","Tuscany floods displace about 100"),
 (24,"EUROPE","Paris marks 11 years since 2015 attacks"),
 (25,"TÜRKIYE","Malatya military helicopter crash kills 4"),
 (26,"S ASIA","Delhi AQI ~334, among world's worst"),
 (27,"MIDEAST","Iran says tanker hit Hormuz mine; unverified"),
 (28,"US","Van Hollen says he will challenge Schumer"),
 (29,"US","Officials cite aging, overloaded air system"),
 (30,"UKRAINE","Drone strikes reported in Ukraine, Russia energy sites"),
]
col_x=[493,747]
for i,(number,tag,summary) in enumerate(also):
    col=0 if i<10 else 1
    row=i if i<10 else i-10
    yy=666+row*29
    xx=col_x[col]
    text(xx,yy,f"{number:02d}",13,RED,LABEL)
    text(xx+28,yy,tag,9,SOFT,LABEL)
    paragraph(xx+69,yy,summary,14,178,INK,BODY,0,2)

line(970,width=3)
text(30,978,"Every story here happened or was first reported on Friday 13 November 2026. Contested claims are labelled as claims. Sources: AP, Reuters, AFP, BBC, CNBC, Al Jazeera, Vatican News, Space.com, BLS.",8,INK,BODY)

out=Path(__file__).resolve().parent/"entry.png"
im.save(out,format="PNG",optimize=True)
print(f"Wrote {out} ({out.stat().st_size} bytes)")
