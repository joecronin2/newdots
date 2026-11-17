#!/usr/bin/python3
# glyph hoard + planner for joe's script. run: ./glyphs.py  (needs /usr/bin/python3 for unicode 16 names)
# glyphs.md next to this file is the saved plan: the page starts from it. edit in the browser,
# "download glyphs.md", move it here, rerun, commit. the browser's own storage is just a cache.
import unicodedata as ud, html, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SPEC_PATH = os.path.join(HERE, "glyphs.md")
SPEC = open(SPEC_PATH).read() if os.path.exists(SPEC_PATH) else ""

FAV = [  # (char, note)
    ("þ","thorn · th"),("ŋ","eng · ng"),("ȣ","ou"),("ß","eszett · ss"),("ƕ","hwair · wh"),("æ","ash · ay"),
    ("ȝ","yogh · gh"),("ş","sh (turkish)"),("ç","ch (turkish)"),("č","ch (czech)"),("ф","ph (cyrillic ef)"),("φ","ph (greek phi)"),
    ("ð","eth"),("ƿ","wynn · w"),("œ","ethel"),("ſ","long s"),("ꝛ","r rotunda"),("ı","dotless i"),
    ("ꝥ","that"),("⁊","and"),("⁊c","etc (old &c)"),("ꝯ","con-"),("ꝑ","per-"),("ꝓ","pro-"),
    ("∵","because"),("∴","therefore / so"),("λ","like"),("⸸","fuck?"),("ж","fuck?"),("🝳","half ounce · cool?"),
    ("々","repeat previous word"),("⌬","benzene ring"),("⏣","benzene ring w/ circle"),("⸮","irony point · maybe?"),
    ("ꙮ","many-eyed seraphim"),("ꙭ","double monocular o (essential)"),("ꙫ","binocular o"),("ꙩ","monocular o"),
    ("ꭘ","x with long left leg & ring"),("ꭔ","chi with low right ring"),("ꭡ","iotified e"),("ƣ","oi"),("Ꙛ","blended yus"),("ѿ","ot · from (one-char word)"),("ѡ","omega"),("ꙍ","broad omega"),("ʬ","bilabial percussive"),("ꙙ","closed little yus"),
    ("Φ","capital phi · particle?"),("Ⲁ","coptic alfa · particle?"),("ⲁ","coptic alfa"),("Ⳣ","old nubian wau · particle?"),("ⳣ","old nubian wau"),("ꙛ","blended yus"),("ꙕ","reversed yu"),("Ѿ","ot · particle?"),("㆒","kanbun one"),("㆝","kanbun heaven"),("㆞","kanbun earth"),("㆟","kanbun man"),
    ("⳦","coptic pi ro"),("ⲷ","coptic cryptogrammic eie"),("ⳃ","coptic crossed shei · sh"),("ɤ","ram's horn"),("Ꙕ","reversed yu"),
    ("ヿ","koto · thing"),("ゟ","yori · from/than"),("ゑ","we (archaic)"),("ゐ","wi (archaic)"),("ヱ","we katakana"),("ヰ","wi katakana"),
    ("ゕ","small ka"),("ゖ","small ke"),("ㇱ","ainu small shi"),("ㇰ","ainu small ku"),("ㇷ゚","ainu small pu"),("〼","masu mark"),
    ("𛂇","hentaigana ni · to"),("𛂙","hentaigana no · of"),("𛂞","hentaigana ha · is"),("𛁷","hentaigana to · with"),("𛃗","hentaigana mo · also"),("𛄚","hentaigana wo"),
    ("⼈","kangxi person"),("⼼","kangxi heart"),("⽬","kangxi eye"),("⿁","kangxi ghost"),("⽍","kangxi death"),("⾔","kangxi speech"),
    ("☽","moon"),("☉","sun"),("⛧","pentagram"),("🜍","sulfur"),("🜔","salt"),("☿","mercury"),("ᚦ","thorn rune"),("ᛗ","man rune"),("ᛞ","day rune"),
    ("し","shi (on s now)"),("か","ka (on k now)"),
]
NERD = [  # private use area, only renders with a Nerd Font
    (0xF07A6,"cannabis"),(0xF068C,"skull"),(0xF30D,"gentoo"),(0xE7A8,"rust"),(0xE61E,"c"),(0xF31A,"tux"),
    (0xE0B0,"powerline arrow"),(0xE0B4,"powerline round"),(0xE725,"git branch"),(0xF120,"terminal"),
]
import glob, re, subprocess
SKIP = re.compile(r"CJK Unified|CJK Compatibility Ideographs|Hangul Syllables|Private Use|Surrogates|Variation Selectors|^Tags$|^Specials$|"
                  r"^Basic Latin$|^Ol Onal$|Emoticons|Transport and Map|Pictographs|Combining")
BLOCKS = []
for line in open(sorted(glob.glob("/usr/lib64/perl5/*/unicore/Blocks.txt"))[-1]):
    m = re.match(r"([0-9A-F]+)\.\.([0-9A-F]+); (.+)", line)
    if m and not SKIP.search(m[3]):
        BLOCKS.append((m[3], int(m[1], 16), int(m[2], 16)))

# Joe's dvorak as it is in ~/newdots/dvcustom: [base, shift, glyph, glyph+shift]
ROWS = [
    [("TLDE","`~"),("AE01","1!"),("AE02","2@"),("AE03","3#"),("AE04","4$"),("AE05","5%"),("AE06","6^"),("AE07","7&"),("AE08","8*"),("AE09","9("),("AE10","0)"),("AE11","[{"),("AE12","]}")],
    [("AD01",";:"),("AD02","'\""),("AD03",".>"),("AD04","pP"),("AD05","yY"),("AD06","qQ"),("AD07","fF"),("AD08","gG"),("AD09","rR"),("AD10","lL"),("AD11","/?"),("AD12","=+"),("BKSL","\\|")],
    [("AC01","aA"),("AC02","oO"),("AC03","eE"),("AC04","iI"),("AC05","uU"),("AC06","dD"),("AC07","hH"),("AC08","tT"),("AC09","nN"),("AC10","sS"),("AC11","-_")],
    [("AB01","xX"),("AB02",",<"),("AB03","kK"),("AB04","cC"),("AB05","jJ"),("AB06","bB"),("AB07","mM"),("AB08","wW"),("AB09","vV"),("AB10","zZ")],
]
GLYPH_NOW = {"AC01": "æ", "AC08": "þ", "AC10": "し", "AB03": "か"}
KEYS = {k: [bs[0], bs[1], GLYPH_NOW.get(k, ""), ""] for row in ROWS for k, bs in row}

def R(g, r, kind, uses, status="maybe", note=""):
    return {"g": g, "r": r, "kind": kind, "uses": uses, "status": status, "note": note}

RULES = [  # counts from the vault, Clippings excluded
    R("þ","th","letters",85000,"settled","the first one"),
    R("ŋ","ng","letters",35326,"maybe","31k of these are -ing"),
    R("ȣ","ou","letters",29738),
    R("ç","ch","letters",12646,"maybe","or č"),
    R("ß","ss","letters",11620,"settled","deadaß"),
    R("ƕ","wh","letters",11169),
    R("æ","ay","letters",8942,"settled"),
    R("ȝ","gh","letters",7536,"maybe","niȝt, bȣȝt"),
    R("ゐ","wi","letters",7269,"maybe","with → ゐþ"),
    R("ş","sh","letters",7222,"maybe","or ⳃ · s key clash with し"),
    R("ゑ","we","letters",6525),
    R("ф","ph","letters",3545,"maybe","or φ"),
    R("λ","like","stem",10414,"settled","λd, disλ, dreamλ"),
    R("ヿ","thing","stem",6375,"maybe","koto literally = thing"),
    R("⌬","ring","stem",1930,"maybe","free benzene, or something else"),
    R("⸸","fuck","stem",1310,"maybe","or ж · ⸸iŋ, ⸸ed"),
    R("⁊","and","word",21184,"maybe","& collides with code in notes"),
    R("ꝥ","that","word",13566),
    R("∴","so","word",3865),
    R("∵","because","word",3546),
    R("ゟ","from","word",1990,"maybe","yori"),
    R("","ok","word",658,"maybe","needs a glyph"),
    R("🝳","cool","word",258),
    R("⁊c","etc","word",135),
    R("𛂇","to","particle",15060,"maybe","hentaigana ni"),
    R("𛂙","of","particle",14820,"maybe","hentaigana no"),
    R("𛂞","is","particle",10341,"maybe","hentaigana ha"),
    R("𛁷","with","particle",4019,"maybe","hentaigana to"),
    R("𛃗","also","particle",2160,"maybe","hentaigana mo"),
    R("ꙮ","i think","marker",1111,"maybe","evidential"),
    R("⸮","maybe","marker",1100,"maybe","evidential"),
    R("々","(repeat previous word)","grammar",0,"settled","really々 = really really"),
    R("wt","want","abbr",723),
    R("lta","lot of","abbr",184),
    R("ll","little","abbr",112),
    R("し","shi","letters",0,"maybe","on s now · collides with real japanese → ㇱ?"),
    R("か","ka","letters",0,"drop","on k now · saves nothing, collides"),
    R("ꙭ","","?",0,"maybe","essential"),
    R("⳦","","?",0), R("ⲷ","","?",0), R("ⳃ","","?",0), R("ɤ","","?",0), R("Ꙕ","","?",0), R("⏣","","?",0),
]

PLAN = {"rows": [[k for k, _ in row] for row in ROWS], "keys": KEYS, "rules": RULES}

# k = type + 3*latinish.  type: 0 letter, 1 logogram/picture, 2 symbol/mark/number.
# latinish = plain a-z wearing decorations: diacritics, hooks, strokes, turned/reversed, small caps, math/fancy/circled styles
LOGO = re.compile(r"hieroglyph|cuneiform|linear a|linear b ideogram|tangut|khitan|nushu|kanbun|cjk|kangxi|ideographic|yi syllables|yi radicals", re.I)
LATIN_NAME = re.compile(r"^latin (?:small |capital )?letter (?:[a-z]+ )*?[a-z](?: with .+)?$")
def block_of(cp):
    return next((t for t, lo, hi in BLOCKS if lo <= cp <= hi), "")
def kcode(cp, block=None):
    c = chr(cp); cat = ud.category(c); nm = ud.name(c, "").lower()
    block = block if block is not None else block_of(cp)
    ty = 1 if LOGO.search(block) and (cat[0] == "L" or cat == "So") else 0 if cat[0] == "L" else 2
    kc, d = ud.normalize("NFKC", c), ud.normalize("NFD", c)
    li = (cat[0] == "L" or cat == "So") and ((len(kc) == 1 and kc.isascii() and kc.isalpha() and kc != c)
          or (len(d) > 1 and d[0].isascii() and d[0].isalpha())
          or bool(LATIN_NAME.match(nm)))
    return ty + 3 * li

def tile(ch, label, cls=""):
    k = f' data-ty="{kcode(ord(ch)) % 3}"' + (' data-li' if kcode(ord(ch)) >= 3 else '') if len(ch) == 1 and "nf" not in cls else ""
    return f'<button class="t {cls}"{k} data-c="{html.escape(ch)}" title="{html.escape(label)}"><span>{html.escape(ch)}</span><small>{html.escape(label)}</small></button>'

def name(cp):
    return f"U+{cp:04X} {ud.name(chr(cp), '').lower()}"

parts, total = [], 0
parts.append('<h2>favourites</h2><div class="g">' + "".join(tile(c, n + " · " + " ".join(f"U+{ord(x):04X}" for x in c)) for c, n in FAV) + "</div>")
parts.append('<h2>nerd font (your screen only)</h2><div class="g">' + "".join(tile(chr(cp), f"{n} · U+{cp:04X}", "nf") for cp, n in NERD) + "</div>")
total += len(FAV) + len(NERD)
blocks, nofont = [], []
for title, lo, hi in BLOCKS:
    cps = [cp for cp in range(lo, hi + 1) if ud.category(chr(cp)) not in ("Mn", "Me", "Cc", "Cf", "Zs", "Zl", "Zp", "Cn", "Co", "Cs")]
    if not cps:
        continue
    fams = subprocess.run(["fc-list", f":charset={cps[0]:x}", "family"], capture_output=True, text=True).stdout.split("\n")
    fams = [f for f in fams if f.strip()]
    if not fams:
        nofont.append(title); continue
    pixel = all("unifont" in f.lower() for f in fams)
    # names like "tangut ideograph-17000" say nothing; the block title covers them
    rtl = sum(ud.bidirectional(chr(cp)) in ("R", "AL") for cp in cps) * 2 > len(cps)
    blocks.append([title, [[cp, "" if re.search(r"-[0-9A-F]{4,6}$", ud.name(chr(cp), "-0000")) else ud.name(chr(cp)).lower(), kcode(cp, title)] for cp in cps], int(rtl), int(pixel)])
    total += len(cps)
print("right-to-left blocks:", sum(b[2] for b in blocks), "with", sum(len(b[1]) for b in blocks if b[2]), "chars")
print("no font installed, skipped:", ", ".join(nofont) or "none")

TEMPLATE = r"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Glyph Hoard</title><style>
:root{--bg:#f4f1ea;--fg:#1b1a17;--tile:#fffdf8;--line:#ddd6c8;--dim:#857d6e;--hi:#7a3cff;--glyph:#9a2f6e;--bad:#c62828}
@media (prefers-color-scheme:dark){:root{--bg:#111013;--fg:#ece6da;--tile:#1a191d;--line:#2c2a30;--dim:#8b8494;--hi:#b590ff;--glyph:#ff8fc8;--bad:#ff6b6b}}
*{box-sizing:border-box}
body{margin:0;padding:0 16px 40px;background:var(--bg);color:var(--fg);font:15px/1.4 "Noto Serif",serif}
.fx{font-family:"Noto Serif","Noto Sans Symbols","Noto Sans Symbols 2","Noto Sans Runic","Noto Sans Glagolitic","Noto Sans Gothic","Noto Sans Ogham","Noto Sans Coptic","Noto Sans Old Italic","Noto Sans Phoenician","Noto Sans CJK JP","Noto Serif Hentaigana","Noto Serif Khitan Small Script","Noto Traditional Nushu","Noto Serif Tangut","Noto Sans Linear B","Noto Sans Yi","Noto Sans Canadian Aboriginal","Noto Sans Vai","Noto Sans Tifinagh","Noto Sans Tifinagh APT","Noto Sans Cherokee","Noto Sans Egyptian Hieroglyphs",serif}
header{position:sticky;top:0;background:var(--bg);padding:10px 0;z-index:2;border-bottom:1px solid var(--line);display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center}
h1{margin:0;font-size:24px} h1 em{font-size:13px;color:var(--dim);font-style:normal}
h2{margin:28px 0 10px;font-size:17px} h2 em{color:var(--dim);font-style:normal;font-size:13px}
input,select{font:inherit;background:var(--tile);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:4px 6px}
#q{flex:1 1 260px;max-width:420px;padding:8px 10px}
#selinfo{font-size:13px;color:var(--dim)} #selinfo b{color:var(--hi)}
button.b{font:inherit;font-size:13px;background:var(--tile);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:5px 10px;cursor:pointer}
button.b:hover{border-color:var(--hi)}
.kbwrap{overflow-x:auto;padding-bottom:6px}
.kb{display:inline-flex;flex-direction:column;gap:4px;min-width:max-content}
.row{display:flex;gap:4px}
.row:nth-child(2){padding-left:28px}.row:nth-child(3){padding-left:42px}.row:nth-child(4){padding-left:64px}
.key{width:60px;height:60px;display:grid;grid-template:1fr 1fr/1fr 1fr;background:var(--tile);border:1px solid var(--line);border-radius:7px;overflow:hidden}
.lv{all:unset;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:17px;line-height:1;min-width:0}
.lv.l0,.lv.l1{color:var(--dim)} .lv.l2,.lv.l3{color:var(--glyph);font-size:20px}
.lv.l2:empty::after,.lv.l3:empty::after{content:"·";color:var(--line)}
.lv:hover{background:color-mix(in srgb,var(--hi) 12%,transparent)}
.lv.on{outline:2px solid var(--hi);outline-offset:-2px;background:color-mix(in srgb,var(--hi) 18%,transparent)}
.legend{font-size:12px;color:var(--dim);margin:6px 0 0}
.tbl{overflow-x:auto} table{border-collapse:collapse;width:100%;min-width:760px;font-size:14px}
th{text-align:left;font-size:12px;color:var(--dim);font-weight:normal;padding:4px}
td{padding:3px 4px;border-top:1px solid var(--line);vertical-align:middle}
td input{width:100%} td.n input{width:80px}
.rg{all:unset;cursor:pointer;font-size:26px;min-width:40px;display:inline-block;text-align:center;color:var(--glyph)}
.gi{width:70px!important}
tr.settled td:first-child{box-shadow:inset 3px 0 var(--glyph)} tr.drop{opacity:.45}
input.dup{border-color:var(--bad);color:var(--bad)} .on-key{font-size:12px;color:var(--dim);white-space:nowrap}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(76px,1fr));gap:6px}
.t{background:var(--tile);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:8px 4px 4px;cursor:pointer;display:flex;flex-direction:column;align-items:center;min-width:0}
.t:hover,.t:focus-visible{border-color:var(--hi);outline:none}
.t span{font-size:34px;line-height:1.15}
.t.nf span{font-family:"Symbols Nerd Font Mono","0xProto Nerd Font Propo"}
.t small{color:var(--dim);font-size:10px;width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.t.used{border-color:var(--glyph)}
.hide{display:none} [hidden]{display:none!important}
body.movefavs :is(.static, #blocks, #results, #fit) .t.fav{display:none}
body.case-low :is(.static, #blocks, #results) .t.cu, body.case-up :is(.static, #blocks, #results) .t:not(.cu){display:none}
body.ty-0 :is(.static, #blocks, #results) .t[data-ty]:not([data-ty="0"]){display:none}
body.ty-1 :is(.static, #blocks, #results) .t[data-ty]:not([data-ty="1"]){display:none}
body.ty-2 :is(.static, #blocks, #results) .t[data-ty]:not([data-ty="2"]){display:none}
body.lat-hide :is(.static, #blocks, #results) .t[data-li], body.lat-only :is(.static, #blocks, #results) .t[data-ty]:not([data-li]){display:none}
.fitg{grid-template-columns:repeat(auto-fill,minmax(96px,1fr))} .fitg .t span{font-size:30px;white-space:nowrap} .fitg .t span i{font-style:normal;color:var(--dim);opacity:var(--ctx,.55)}
.t{position:relative;user-select:none} .t.fav::after{content:"★";position:absolute;top:2px;right:5px;font-size:11px;color:var(--glyph)}
details.blk{border-top:1px solid var(--line)} details.blk summary{cursor:pointer;padding:8px 0;font-size:16px} details.blk summary em{color:var(--dim);font-style:normal;font-size:13px}
details.blk.done > summary{color:var(--dim)} details.blk.done > summary::after{content:" ✓";color:var(--glyph)}
#toc a.done{color:var(--dim);text-decoration:line-through} body.hide-checked :is(details.blk.done, #toc a.done){display:none}
.chk{vertical-align:middle;margin-right:4px}
details.blk .g{padding-bottom:12px;content-visibility:auto;contain-intrinsic-size:auto 400px} .toc summary{cursor:pointer;color:var(--hi);margin-bottom:8px}
#toc{columns:3 220px;font-size:13px;margin-bottom:12px} #toc a{display:block;color:var(--fg);text-decoration:none;padding:1px 0} #toc a:hover{color:var(--hi)} #toc em{color:var(--dim);font-style:normal}
#toast{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);background:var(--hi);color:#fff;padding:6px 14px;border-radius:20px;opacity:0;transition:opacity .2s;pointer-events:none}
</style></head><body class="fx">
<header><h1>glyph hoard <em>__TOTAL__ chars</em></h1>
<input id="q" placeholder="search name or paste a char (rune, eye, thorn, hentaigana…)">
<span id="selinfo">click a key slot to place a glyph · otherwise clicking a glyph copies it</span></header>

<h2>keyboard <em>your dvorak · each key: shift / glyph+shift on top, base / glyph below</em></h2>
<div class="kbwrap"><div class="kb" id="kb"></div></div>
<p class="legend">select a slot, then click any glyph on the page, or just type one · backspace clears · esc cancels · pink = glyph layer</p>

<h2>rules <em>what each glyph replaces · uses = count in your vault</em></h2>
<p style="margin:0 0 8px;display:flex;flex-wrap:wrap;gap:6px">
<button class="b" id="add">+ rule</button><button class="b" id="sort">sort by uses</button>
<button class="b" id="copy">copy as glyphs.md</button><button class="b" id="dl">download glyphs.md</button><button class="b" id="imp">import glyphs.md</button><input type="file" id="impf" accept=".md,text/markdown,text/plain" hidden><button class="b" id="reset">reset to saved</button></p>
<div class="tbl"><table><thead><tr><th>glyph</th><th>replaces</th><th>kind</th><th>uses</th><th>status</th><th>on key</th><th>note</th><th></th></tr></thead><tbody id="rules"></tbody></table></div>

<h2>★ yours <em>double-click any glyph anywhere to star or unstar it</em></h2>
<p style="margin:0 0 8px"><label style="font-size:13px;color:var(--dim)"><input type="checkbox" id="movefavs"> move starred glyphs here (hide them from the other lists)</label></p>
<div id="myfavs" class="g"></div>
__PARTS__
<h2>everything <em id="bcount"></em></h2>
<p style="margin:0 0 8px;display:flex;flex-wrap:wrap;gap:6px;align-items:center">
<button class="b" id="view">latin-fit view</button><button class="b" id="expand">expand all</button><button class="b" id="collapse">collapse all</button>
<label style="font-size:13px;color:var(--dim)"><input type="checkbox" id="hidechk"> hide checked blocks</label>
<label style="font-size:13px;color:var(--dim)"><input type="checkbox" id="sortfit"> sort inside blocks by latin fit</label>
<label style="font-size:13px;color:var(--dim)">type <select id="typef"><option value="">any</option><option value="0">letters</option><option value="1">logograms / pictures</option><option value="2">symbols & marks</option></select></label>
<label style="font-size:13px;color:var(--dim)">latin-ish <select id="latf"><option value="">any</option><option value="hide">hide decorated latin</option><option value="only">only decorated latin</option></select></label>
<label style="font-size:13px;color:var(--dim)">case <select id="casef"><option value="">any</option><option value="low">lowercase + caseless (in-word picks)</option><option value="up">capitals only (particles)</option></select></label>
<label style="font-size:13px;color:var(--dim)"><input type="checkbox" id="rtl"> show right-to-left scripts (hebrew, arabic, phoenician…)</label></p>
<details class="toc"><summary>jump to a block</summary><div id="toc"></div></details>
<div id="results" class="g" hidden></div><p id="rinfo" class="legend" hidden></p>
<div id="blocks"></div>
<div id="fitwrap" hidden><p class="legend" style="display:flex;flex-wrap:wrap;gap:6px 16px;align-items:center"><span id="fitinfo"></span><label>surrounding a · e <input type="range" id="ctx" min="0" max="100" style="vertical-align:middle"></label></p><div id="fit" class="g fitg"></div>
<p><button class="b" id="fitmore">show more</button></p></div>
<div id="toast"></div>
<script>
const DEF = __PLAN__;
const B = __BLOCKS__;
const KEY = 'glyph-plan-v1', LV = ['base', 'shift', 'glyph', 'glyph+shift'];
const KINDS = ['letters', 'stem', 'word', 'particle', 'marker', 'grammar', 'abbr', '?'], STATUS = ['settled', 'maybe', 'drop'];
let plan = null, sel = null;
try { plan = JSON.parse(localStorage.getItem(KEY)); } catch (e) {}
const SPEC = __SPEC__;
// glyphs.md → plan. same format md() writes: ## rules / ## keys tables, ## favourites line
function parseMd(txt) {
  if (!txt) return null;
  const sec = {}; let cur = null;
  for (const line of txt.split('\n')) {
    const h = line.match(/^##\s+(\w+)/);
    if (h) { cur = h[1].toLowerCase(); sec[cur] = []; } else if (cur) sec[cur].push(line);
  }
  if (!sec.rules) return null;
  const table = ls => (ls || []).map(l => l.trim()).filter(l => l.startsWith('|') && !/^\|[\s:|-]+\|$/.test(l)).slice(1)
    .map(l => l.slice(1, -1).split(/(?<!\\)\|/).map(c => c.trim().replace(/\\\|/g, '|')));
  const p = { keys: structuredClone(DEF.keys), rules: [], favs: [] };
  for (const [g, r, kind, uses, status, , note] of table(sec.rules))
    p.rules.push({ g, r, kind: kind || '?', uses: +uses || 0, status: status || 'maybe', note: note || '' });
  for (const [id, ...lv] of table(sec.keys)) if (p.keys[id]) p.keys[id] = [0, 1, 2, 3].map(i => lv[i] ?? '');
  p.favs = (sec.favourites || []).join(' ').split(/\s+/).filter(Boolean);
  p.checked = (sec.checked || []).filter(l => /^\s*-\s+/.test(l)).map(l => l.replace(/^\s*-\s+/, '').trim());
  return p;
}
const start = () => { const p = parseMd(SPEC) || structuredClone(DEF); p.favs ??= []; p.checked ??= []; return p; };
if (!plan || !plan.keys) plan = start();
plan.favs ??= [];
plan.checked ??= [];
let favSet = new Set(plan.favs);
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(plan)); } catch (e) {} };
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const toast = m => { const t = $('toast'); t.textContent = m; t.style.opacity = 1; clearTimeout(t.h); t.h = setTimeout(() => t.style.opacity = 0, 1100); };

function where(g) {
  if (!g) return '';
  const out = [];
  for (const row of DEF.rows) for (const id of row) plan.keys[id].forEach((c, l) => {
    if (c === g) out.push((l >= 2 ? (l === 3 ? 'glyph+shift+' : 'glyph+') : (l === 1 ? 'shift+' : '')) + plan.keys[id][0]);
  });
  return out.join(', ');
}

function renderKb() {
  $('kb').innerHTML = DEF.rows.map(row => '<div class="row">' + row.map(id => '<div class="key">' +
    [1, 3, 0, 2].map(l => `<button class="lv l${l}${sel && sel[0] === id && sel[1] === l ? ' on' : ''}" data-k="${id}" data-l="${l}" title="${id} · ${LV[l]}">${esc(plan.keys[id][l])}</button>`).join('') +
    '</div>').join('') + '</div>').join('');
  $('selinfo').innerHTML = sel ? `placing on <b>${LV[sel[1]]} + ${esc(plan.keys[sel[0]][0])}</b> · click a glyph or type one · esc cancels`
    : 'click a key slot to place a glyph · otherwise clicking a glyph copies it';
}

function renderRules() {
  const cnt = f => plan.rules.reduce((m, r) => (r[f] && (m[r[f]] = (m[r[f]] || 0) + 1), m), {});
  const gc = cnt('g'), rc = cnt('r');
  $('rules').innerHTML = plan.rules.map((r, i) => `<tr class="${r.status}">
    <td><button class="rg fx" data-i="${i}" title="click to copy / place">${esc(r.g) || '·'}</button> <input class="gi fx${gc[r.g] > 1 ? ' dup' : ''}" data-i="${i}" data-f="g" value="${esc(r.g)}"></td>
    <td><input class="${rc[r.r] > 1 ? 'dup' : ''}" data-i="${i}" data-f="r" value="${esc(r.r)}"></td>
    <td><select data-i="${i}" data-f="kind">${KINDS.map(k => `<option${k === r.kind ? ' selected' : ''}>${k}</option>`).join('')}</select></td>
    <td class="n"><input type="number" data-i="${i}" data-f="uses" value="${r.uses || ''}"></td>
    <td><select data-i="${i}" data-f="status">${STATUS.map(k => `<option${k === r.status ? ' selected' : ''}>${k}</option>`).join('')}</select></td>
    <td class="on-key">${esc(where(r.g)) || '—'}</td>
    <td><input data-i="${i}" data-f="note" value="${esc(r.note)}"></td>
    <td><button class="b" data-del="${i}" title="delete rule">×</button></td></tr>`).join('');
  const used = new Set(plan.rules.filter(r => r.status !== 'drop').map(r => r.g));
  document.querySelectorAll('.t').forEach(t => t.classList.toggle('used', used.has(t.dataset.c)));
}

const render = () => { renderKb(); renderRules(); };

function place(g) {
  plan.keys[sel[0]][sel[1]] = g;
  toast(`${g || 'cleared'} → ${LV[sel[1]]} + ${plan.keys[sel[0]][0]}`);
  sel = null; save(); render();
}

const cell = s => String(s ?? '').replace(/\|/g, '\\|');
function md() {
  let s = '# glyphs\n\n## rules\n\n| glyph | replaces | kind | uses | status | on key | note |\n|---|---|---|---|---|---|---|\n';
  for (const r of plan.rules) s += `| ${cell(r.g)} | ${cell(r.r)} | ${r.kind} | ${r.uses || ''} | ${r.status} | ${cell(where(r.g))} | ${cell(r.note)} |\n`;
  s += '\n## keys\n\n| key | base | shift | glyph | glyph+shift |\n|---|---|---|---|---|\n';
  for (const row of DEF.rows) for (const id of row) s += `| ${id} | ${plan.keys[id].map(cell).join(' | ')} |\n`;
  s += '\n## favourites\n\n' + plan.favs.join(' ') + '\n';
  s += '\n## checked\n\n' + plan.checked.map(t => '- ' + t + '\n').join('');
  return s;
}

document.addEventListener('click', e => {
  const lv = e.target.closest('.lv');
  if (lv) { const k = [lv.dataset.k, +lv.dataset.l]; sel = sel && sel[0] === k[0] && sel[1] === k[1] ? null : k; renderKb(); return; }
  const t = e.target.closest('.t, .rg');
  if (t) {
    const g = t.classList.contains('rg') ? plan.rules[t.dataset.i].g : t.dataset.c;
    if (!g) return;
    if (sel) return place(g);
    navigator.clipboard.writeText(g).then(() => toast('copied ' + g), () => toast(g));
    return;
  }
  if (e.target.dataset.del !== undefined) { plan.rules.splice(+e.target.dataset.del, 1); save(); renderRules(); }
});
$('rules').addEventListener('input', e => {
  const { i, f } = e.target.dataset; if (i === undefined) return;
  plan.rules[i][f] = f === 'uses' ? +e.target.value || 0 : e.target.value; save();
  if (e.target.tagName === 'SELECT') renderRules();
});
$('rules').addEventListener('change', e => { if (e.target.tagName === 'INPUT') renderRules(); });
document.addEventListener('keydown', e => {
  if (!sel || e.target.matches('input, select')) return;
  if (e.key === 'Escape') { sel = null; renderKb(); }
  else if (e.key === 'Backspace' || e.key === 'Delete') { e.preventDefault(); place(''); }
  else if ([...e.key].length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) { e.preventDefault(); place(e.key); }
});
$('imp').onclick = () => $('impf').click();
$('impf').onchange = async e => {
  const f = e.target.files[0]; if (!f) return;
  const p = parseMd(await f.text());
  if (!p) return toast("that doesn't look like a glyphs.md");
  plan = Object.assign(p, { showRtl: plan.showRtl, moveFavs: plan.moveFavs, ctx: plan.ctx });
  sel = null; save(); render(); renderFavs(); renderChecks(); toast(`imported ${p.rules.length} rules · ${p.favs.length} favourites`);
  e.target.value = '';
};
$('add').onclick = () => { plan.rules.unshift({ g: '', r: '', kind: 'word', uses: 0, status: 'maybe', note: '' }); save(); renderRules(); };
$('sort').onclick = () => { plan.rules.sort((a, b) => (b.uses || 0) - (a.uses || 0)); save(); renderRules(); };
$('copy').onclick = () => navigator.clipboard.writeText(md()).then(() => toast('copied glyphs.md'), () => toast('copy failed, use download'));
$('dl').onclick = () => { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([md()], { type: 'text/markdown' })); a.download = 'glyphs.md'; a.click(); };
$('reset').onclick = () => { if (confirm('throw away browser edits and go back to glyphs.md as it was when this page was built?')) { const f = plan.favs; plan = start(); if (!SPEC) plan.favs = f; sel = null; save(); render(); renderFavs(); renderChecks(); } };
const usedSet = () => new Set(plan.rules.filter(r => r.status !== 'drop').map(r => r.g));
const hex = cp => 'U+' + cp.toString(16).toUpperCase().padStart(4, '0');
const isUp = c => c !== c.toLowerCase();  // has a lowercase form = it's a capital
const kattr = k => k === undefined ? '' : ` data-ty="${k % 3}"${k >= 3 ? ' data-li' : ''}`;
function tileHtml(cp, nm, bt, used, k) {
  const c = String.fromCodePoint(cp), label = `${hex(cp)} ${nm || bt.toLowerCase()}`;
  return `<button class="t${isUp(c) ? ' cu' : ''}${used.has(c) ? ' used' : ''}${favSet.has(c) ? ' fav' : ''}"${kattr(k)} data-c="${esc(c)}" title="${esc(label)}"><span>${esc(c)}</span><small>${esc(nm || hex(cp))}</small></button>`;
}

$('toc').innerHTML = B.map(([t, cs], i) => `<a href="#b${i}" data-open="${i}" class="${B[i][2] ? 'rtlb' : ''}">${esc(t)} <em>${cs.length}</em></a>`).join('');
$('blocks').innerHTML = B.map(([t, cs], i) => `<details class="blk${B[i][2] ? ' rtlb' : ''}" id="b${i}" data-i="${i}"><summary><input type="checkbox" class="chk" data-i="${i}" title="mark this block as checked"> ${esc(t)} <em>${cs.length}</em></summary><div class="g"></div></details>`).join('');
function renderChecks() {
  const done = new Set(plan.checked);
  B.forEach(([t], i) => {
    const d = $('b' + i), on = done.has(t);
    d.classList.toggle('done', on); d.querySelector('.chk').checked = on;
    document.querySelector(`#toc a[data-open="${i}"]`).classList.toggle('done', on);
  });
  const n = B.filter(([t]) => done.has(t)).length;
  $('bcount').textContent = `${B.length} blocks · ${n} checked · open one to load it`;
}
document.addEventListener('change', e => {
  if (!e.target.matches('.chk')) return;
  const t = B[e.target.dataset.i][0], i = plan.checked.indexOf(t);
  if (e.target.checked && i < 0) plan.checked.push(t); else if (!e.target.checked && i >= 0) plan.checked.splice(i, 1);
  save(); renderChecks();
});
renderChecks();
$('hidechk').checked = !!plan.hideChecked;
document.body.classList.toggle('hide-checked', !!plan.hideChecked);
$('hidechk').onchange = e => { plan.hideChecked = e.target.checked; save(); document.body.classList.toggle('hide-checked', plan.hideChecked); };
async function renderBlock(d) {
  d.dataset.done = 1;
  if (plan.sortFit) await getFit();
  const [t, cs] = B[d.dataset.i], used = usedSet();
  const list = plan.sortFit ? [...cs].sort((a, b) => byFit(a[0], b[0])) : cs;
  d.querySelector('.g').innerHTML = list.map(([cp, nm, k]) => tileHtml(cp, nm, t, used, k)).join('');
}
$('blocks').addEventListener('toggle', e => { const d = e.target; if (d.open && !d.dataset.done) renderBlock(d); }, true);
$('toc').addEventListener('click', e => { const a = e.target.closest('a'); if (a) $('b' + a.dataset.open).open = true; });

let qt, fitMode = false;
$('q').addEventListener('input', e => { clearTimeout(qt); qt = setTimeout(() => search(e.target.value.trim().toLowerCase()), 150); });
function search(q) {
  document.querySelectorAll('.static .t').forEach(t => t.classList.toggle('hide', !!q && !t.title.toLowerCase().includes(q) && t.dataset.c !== q));
  $('blocks').hidden = !!q || fitMode; $('fitwrap').hidden = !!q || !fitMode; $('results').hidden = $('rinfo').hidden = !q;
  if (!q) return;
  const out = [], used = usedSet(), MAX = 800;
  for (const [t, cs, rtl] of B) {
    if (rtl && !plan.showRtl) continue;
    const tl = t.toLowerCase();
    for (const [cp, nm, k] of cs) {
      if (String.fromCodePoint(cp) === q || nm.includes(q) || tl.includes(q)) out.push([cp, nm, t, k]);
      if (out.length >= MAX) break;
    }
    if (out.length >= MAX) break;
  }
  if (plan.sortFit && fitMap) out.sort((a, b) => byFit(a[0], b[0]));
  $('results').innerHTML = out.map(([cp, nm, t, k]) => tileHtml(cp, nm, t, used, k)).join('');
  $('rinfo').textContent = out.length >= MAX ? `showing the first ${MAX} matches, narrow it down` : `${out.length} matches`;
}
render();

// ★ favourites: double-click any glyph (hoard, favourites, rules table) to star / unstar it
let names;
function nameOf(c) {
  const st = document.querySelector(`.static .t[data-c="${CSS.escape(c)}"]`);
  if (st) return st.title;
  if (!names) { names = new Map(); for (const [t, cs] of B) for (const [cp, nm] of cs) names.set(String.fromCodePoint(cp), nm || t.toLowerCase()); }
  return names.get(c) || '';
}
function renderFavs() {
  favSet = new Set(plan.favs);
  const used = usedSet();
  $('myfavs').innerHTML = plan.favs.length
    ? plan.favs.map(c => `<button class="t fav${isUp(c) ? ' cu' : ''}${used.has(c) ? ' used' : ''}" data-c="${esc(c)}" title="${esc(nameOf(c))}"><span>${esc(c)}</span><small>${esc(nameOf(c))}</small></button>`).join('')
    : '<p class="legend">nothing yet · double-click any glyph to star it</p>';
  document.querySelectorAll('.t').forEach(t => t.classList.toggle('fav', favSet.has(t.dataset.c)));
}
document.addEventListener('dblclick', e => {
  const t = e.target.closest('.t, .rg');
  if (!t) return;
  const g = t.classList.contains('rg') ? plan.rules[t.dataset.i].g : t.dataset.c;
  if (!g) return;
  const i = plan.favs.indexOf(g);
  if (i < 0) plan.favs.push(g); else plan.favs.splice(i, 1);
  save(); renderFavs(); toast((i < 0 ? '★ starred ' : 'unstarred ') + g);
});
renderFavs();

// right-to-left scripts mess with cursor movement and word order in left-to-right text, so they're hidden by default
const applyRtl = () => document.querySelectorAll('.rtlb').forEach(el => el.hidden = !plan.showRtl);
$('rtl').checked = !!plan.showRtl;
$('rtl').onchange = e => { plan.showRtl = e.target.checked; save(); applyRtl(); search($('q').value.trim().toLowerCase()); };
applyRtl();

const applyCase = () => {
  const b = document.body.classList;
  b.toggle('case-low', plan.caseF === 'low'); b.toggle('case-up', plan.caseF === 'up');
  for (const i of [0, 1, 2]) b.toggle('ty-' + i, plan.typeF === String(i));
  b.toggle('lat-hide', plan.latF === 'hide'); b.toggle('lat-only', plan.latF === 'only');
};
for (const [id, key] of [['typef', 'typeF'], ['latf', 'latF']]) {
  $(id).value = plan[key] || '';
  $(id).onchange = e => { plan[key] = e.target.value; save(); applyCase(); if (fitMode && fitList) showFit(false); };
}
document.querySelectorAll('.static .t').forEach(t => [...t.dataset.c].length === 1 && isUp(t.dataset.c) && t.classList.add('cu'));
$('casef').value = plan.caseF || '';
$('casef').onchange = e => { plan.caseF = e.target.value; save(); applyCase(); if (fitMode && fitList) showFit(false); };
applyCase();

$('movefavs').checked = !!plan.moveFavs;
document.body.classList.toggle('movefavs', !!plan.moveFavs);
$('movefavs').onchange = e => { plan.moveFavs = e.target.checked; save(); document.body.classList.toggle('movefavs', plan.moveFavs); };

// open blocks a few at a time so the page doesn't freeze on 37k glyphs
$('expand').onclick = async () => {
  const ds = [...document.querySelectorAll('details.blk')].filter(d => !d.hidden && !d.open);
  toast(`opening ${ds.length} blocks…`);
  for (const [n, d] of ds.entries()) { d.open = true; if (n % 6 === 5) await new Promise(r => setTimeout(r, 0)); }
  toast('all open');
};
// latin-fit: measure every glyph as it actually renders and score how close it is to a latin letter
// (size, height vs ascenders/descenders, sitting on the baseline, letter vs symbol, latin-ish script)
let fitList = null, fitShown = 0, fitMap = null, fitting = null;
async function getFit() {
  if (fitList) return;
  if (!fitting) { toast('measuring 37k glyphs, a few seconds…'); fitting = computeFit(); }
  fitList = await fitting;
  fitMap = new Map(fitList.map(x => [x[1], x[0]]));
}
const byFit = (a, b) => (fitMap.get(a) ?? 99) - (fitMap.get(b) ?? 99);
const FIT_PAGE = 1500;
const JUNK = /legacy computing|box drawing|block elements|braille|sextant|geometric shapes|control pictures|optical character|mahjong|domino|playing cards|chess|musical|ornamental dingbats|enclosed alphanumeric/i;
const NEAR = /latin|ipa|phonetic|spacing modifier/i, KIN = /greek|cyrillic|coptic|armenian|georgian|glagolitic|gothic|runic|old italic|cherokee|deseret|shavian|osage|vithkuqi|todhri|elbasan|caucasian albanian|ogham|old permic|old hungarian|old turkic|tifinagh|lisu|bamum|vai|nko/i;
async function computeFit() {
  const ctx = document.createElement('canvas').getContext('2d'), em = 48;
  ctx.font = `${em}px ` + getComputedStyle(document.body).fontFamily;
  const m = t => { const r = ctx.measureText(t); return { w: r.actualBoundingBoxLeft + r.actualBoundingBoxRight, a: r.actualBoundingBoxAscent, d: r.actualBoundingBoxDescent }; };
  const lat = [...'abcdefghijklmnopqrstuvwxyz'].map(m);
  const ref = { xh: m('x').a, asc: Math.max(...[...'bdfhklt'].map(c => m(c).a)), desc: Math.max(...[...'gjpqy'].map(c => m(c).d)),
                maxW: Math.max(...lat.map(x => x.w)) };
  // readability: draw at text size and count how often each pixel row flips ink/no-ink. latin tops out around m;
  // glyphs much busier than that turn into blobs when you read them small
  const S = 36, cv = document.createElement('canvas'); cv.width = cv.height = S;
  const c2 = cv.getContext('2d', { willReadFrequently: true });
  c2.font = '24px ' + getComputedStyle(document.body).fontFamily;
  const busy = ch => {
    c2.clearRect(0, 0, S, S); c2.fillText(ch, 4, 27);
    const px = c2.getImageData(0, 0, S, S).data;
    let flips = 0, rows = 0;
    for (let y = 0; y < S; y++) {
      let prev = false, any = false;
      for (let x = 0; x < S; x++) { const on = px[(y * S + x) * 4 + 3] > 110; if (on !== prev) { flips++; prev = on; } any ||= on; }
      rows += any;
    }
    return rows ? flips / rows : 0;
  };
  const busyRef = Math.max(...[...'abcdefghijklmnopqrstuvwxyz'].map(busy));
  const all = [];
  let n = 0;
  for (const [t, cs, rtl, pixel] of B) {
    const bonus = (NEAR.test(t) ? -0.12 : KIN.test(t) ? -0.06 : 0) + (JUNK.test(t) ? 0.5 : 0) + (pixel ? 0.6 : 0);
    for (const [cp, nm, k] of cs) {
      const g = m(String.fromCodePoint(cp)), h = g.a + g.d;
      if (!(g.w > 0) || !(h > 0)) continue;
      let p = Math.max(0, g.w - 1.3 * ref.maxW) / em * 4        // wider than m / w
            + Math.max(0, g.a - 1.08 * ref.asc) / em * 5        // taller than ascenders
            + Math.max(0, g.d - 1.15 * ref.desc) / em * 5       // deeper than descenders
            + Math.max(0, -g.d - 0.08 * em) / em * 3            // floats above the baseline
            + Math.max(0, 0.7 * ref.xh - h) / em * 3            // tiny marks
            + Math.max(0, busy(String.fromCodePoint(cp)) - 1.1 * busyRef) * 0.12   // too busy to read small
            + [0, 0.2, 0.35][(k ?? 2) % 3] + bonus;
      if (/\p{P}/u.test(String.fromCodePoint(cp))) p += 0.5;        // dots, commas, brackets
      all.push([p, cp, nm, t, k, rtl]);
      if (++n % 3000 === 0) { $('fitinfo').textContent = `measuring… ${n} glyphs`; await new Promise(r => setTimeout(r, 0)); }
    }
  }
  return all.sort((x, y) => x[0] - y[0]);
}
function showFit(more) {
  const used = usedSet(), from = more ? fitShown : 0;
  const keep = ([, cp, , , k, rtl]) => (!rtl || plan.showRtl) && (!plan.caseF || (plan.caseF === 'up') === isUp(String.fromCodePoint(cp)))
    && (!plan.typeF || String(k % 3) === plan.typeF) && (!plan.latF || (plan.latF === 'only') === (k >= 3));
  const fl = fitList.filter(keep);
  fitShown = Math.min(fl.length, from + FIT_PAGE);
  const html = fl.slice(from, fitShown).map(([p, cp, nm, t, k]) => {
    const c = String.fromCodePoint(cp), label = `${hex(cp)} ${nm || t.toLowerCase()} · fit ${p.toFixed(2)}`;
    return `<button class="t${isUp(c) ? ' cu' : ''}${used.has(c) ? ' used' : ''}${favSet.has(c) ? ' fav' : ''}"${kattr(k)} data-c="${esc(c)}" title="${esc(label)}"><span><i>a</i>${esc(c)}<i>e</i></span><small>${esc(nm || hex(cp))}</small></button>`;
  }).join('');
  if (more) $('fit').insertAdjacentHTML('beforeend', html); else $('fit').innerHTML = html;
  $('fitinfo').textContent = `best latin fits first · showing ${fitShown} of ${fl.length} · hover a glyph for its score (lower = fits better)`;
  $('fitmore').hidden = fitShown >= fl.length;
}
$('view').onclick = async () => {
  fitMode = !fitMode;
  $('view').textContent = fitMode ? 'block view' : 'latin-fit view';
  $('blocks').hidden = fitMode; $('fitwrap').hidden = !fitMode;
  if (fitMode) await getFit();
  if (fitMode) showFit(false);
};
$('fitmore').onclick = () => showFit(true);
$('sortfit').checked = !!plan.sortFit;
$('sortfit').onchange = async e => {
  plan.sortFit = e.target.checked; save();
  for (const d of document.querySelectorAll('details.blk[data-done]')) await renderBlock(d);
  search($('q').value.trim().toLowerCase());
};
const setCtx = v => document.body.style.setProperty('--ctx', v / 100);
$('ctx').value = plan.ctx ?? 55; setCtx($('ctx').value);
$('ctx').oninput = e => { plan.ctx = +e.target.value; setCtx(plan.ctx); save(); };
// ←/→ anywhere in latin-fit view nudge the surrounding letters (unless you're typing or placing on a key)
document.addEventListener('keydown', e => {
  if (!fitMode || sel || e.target.matches('input, select, textarea') || !['ArrowLeft', 'ArrowRight'].includes(e.key)) return;
  e.preventDefault();
  plan.ctx = Math.max(0, Math.min(100, (plan.ctx ?? 55) + (e.key === 'ArrowRight' ? 10 : -10)));
  $('ctx').value = plan.ctx; setCtx(plan.ctx); save();
});
$('rtl').addEventListener('change', () => { if (fitMode && fitList) showFit(false); });

$('collapse').onclick = () => document.querySelectorAll('details.blk[open]').forEach(d => d.open = false);
</script></body></html>"""

page = (TEMPLATE.replace("__TOTAL__", str(total))
        .replace("__SPEC__", json.dumps(SPEC, ensure_ascii=False).replace("</", "<\\/"))
        .replace("__PLAN__", json.dumps(PLAN, ensure_ascii=False).replace("</", "<\\/"))
        .replace("__PARTS__", '<div class="static">' + "".join(parts) + "</div>")
        .replace("__BLOCKS__", json.dumps(blocks, ensure_ascii=False, separators=(",", ":"))))
out = os.path.join(HERE, "glyph-hoard.html")
open(out, "w").write(page)
print(out, total, "glyphs", len(page) // 1024, "KB")
