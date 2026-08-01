#!/usr/bin/env python3
"""Generates the four static pages for the Morgan Millions prototype.
Shared chrome (head, nav, footer) lives here so pages stay consistent."""
import pathlib

ROOT = pathlib.Path(__file__).parent

LOGO = '''<svg viewBox="0 0 96 44" fill="currentColor" aria-hidden="true" focusable="false">
        <!-- Modern engraved MM monogram in Playfair Display serif.
             Real letterforms give the proper thick/thin brass-engraved feel.
             Kerned tight, no enclosing shapes, subtle hairline underscore. -->
        <text x="48" y="34" text-anchor="middle"
              font-family="Playfair Display, Georgia, serif"
              font-size="44" font-weight="800"
              letter-spacing="-2">MM</text>
        <line x1="18" y1="41.5" x2="78" y2="41.5"
              stroke="currentColor" stroke-width="0.6" opacity="0.55"/>
      </svg>'''

PROGRAM_SUBNAV = [
    ("program.html",     "Overview",           "What Morgan Millions is"),
    ("classes.html",     "Classes &amp; Purse", "$1M base, 7 classes"),
    ("vault.html",       "The Vault",           "Vaulted &middot; Reserve &middot; Minted"),
    ("crown.html",       "The Crown Purse",     "$105K bonus &middot; 14 placings"),
    ("bridge.html",      "The Bridge",          "2027\u20132030 window"),
    ("nomination.html",  "Nomination &amp; Fees", "How to enter"),
    ("governance.html",  "Governance",          "Board &middot; audit"),
]
PROGRAM_PAGES = {href for href, _, _ in PROGRAM_SUBNAV}

NAV_ITEMS = [
    ("index.html",       "Home",         None),
    ("program.html",     "Program",      PROGRAM_SUBNAV),
    ("stallions.html",   "Stallions",    None),
    ("for-trainers.html","Trainers", None),
    ("event.html",       "Event",        None),
]


def head(title, desc, page):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#3C5878">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="assets/img/hero-a-pasture.jpg">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,800;1,400;1,500&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<link rel="stylesheet" href="assets/css/style.css?v=2026080126">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{nav(page)}
<main id="main">'''


def nav(page):
    parts = []
    for href, label, sub in NAV_ITEMS:
        # Parent is active when the page matches OR when the page is any sub-item under this parent.
        active = (href == page) or (sub is not None and page in PROGRAM_PAGES)
        active_attr = ' aria-current="page"' if active else ""
        if sub is None:
            parts.append(f'      <a class="nav__link" href="{href}"{active_attr}>{label}</a>')
        else:
            sub_items = "\n".join(
                f'''          <a class="subnav__item" href="{s_href}"{" aria-current=\"page\"" if s_href == page else ""}>
            <span class="subnav__label">{s_label}</span>
            <span class="subnav__desc">{s_desc}</span>
          </a>'''
                for s_href, s_label, s_desc in sub)
            parts.append(f'''      <div class="nav__group" data-nav-group>
        <a class="nav__link nav__link--parent" href="{href}"{active_attr} aria-haspopup="true" aria-expanded="false">{label}<span class="nav__caret" aria-hidden="true">▾</span></a>
        <div class="subnav" role="menu" aria-label="{label} sections">
{sub_items}
        </div>
      </div>''')
    links = "\n".join(parts)
    return f'''<header class="nav">
  <a class="brand" href="index.html" aria-label="Morgan Millions — home">
    {LOGO}
    <span class="brand__name">Morgan Millions</span>
  </a>
  <nav class="nav__links" id="nav-links" data-open="false" aria-label="Primary">
{links}
    <button class="pill pill--ghost nav__cta-mobile" type="button" data-placeholder="Coming Soon">Watch Live</button>
  </nav>
  <button class="pill nav__cta" type="button" data-placeholder="Coming Soon">Watch Live</button>
  <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="nav-links" aria-label="Menu">
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M3 7h18M3 12h18M3 17h18" stroke="currentColor" stroke-width="1.4"/></svg>
  </button>
</header>'''


def countdown(large=False, caption="Until the first go &middot; 6 October 2027, 6:00 PM CDT"):
    cls = "countdown countdown--large" if large else "countdown"
    units = [("days", "Days"), ("hours", "Hours"), ("minutes", "Minutes"), ("seconds", "Seconds")]
    parts = []
    for i, (unit, label) in enumerate(units):
        if i:
            parts.append('    <span class="countdown__sep" aria-hidden="true">:</span>')
        parts.append(f'''    <span class="countdown__unit">
      <span class="countdown__value" data-unit="{unit}">--</span>
      <span class="countdown__label">{label}</span>
    </span>''')
    body = "\n".join(parts)
    return f'''<div data-countdown>
  <div class="{cls}" role="timer" aria-live="off" aria-label="Countdown to the inaugural Morgan Millions">
{body}
  </div>
  <p class="countdown__caption">{caption}</p>
</div>'''


FOOTER = '''</main>
<footer class="footer">
  <div class="wrap">
    <div class="footer__top">
      <div>
        <p class="footer__word">Morgan Millions</p>
        <p class="footer__note">A stakes program staging a $1M annual Morgan event.</p>
      </div>
      <div>
        <h4>Program</h4>
        <ul>
          <li><a href="program.html">The Program</a></li>
          <li><a href="program.html#classes">Classes &amp; Purse</a></li>
          <li><a href="program.html#bridge">The Bridge</a></li>
          <li><a href="program.html#governance">Governance</a></li>
        </ul>
      </div>
      <div>
        <h4>Sires &amp; Event</h4>
        <ul>
          <li><a href="stallions.html">Vaulted Sires</a></li>
          <li><a href="stallions.html#bridge">Charter Holders</a></li>
          <li><a href="event.html">October 6&ndash;8, 2027</a></li>
          <li><a href="event.html#tickets">Tickets</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__legal">
      <span>&copy; 2026 Morgan Millions. All rights reserved.</span>
      <span>Target: Oklahoma City &middot; October 6&ndash;8, 2027 (venue pending)</span>
    </div>
  </div>
</footer>
<script src="assets/js/site.js?v=2026080126" defer></script>
</body>
</html>'''


# ---------------------------------------------------------------- index
index = head(
    "Morgan Millions — The Richest Purse in the Breed",
    "Morgan Millions is a premier equestrian program for the Morgan horse breed. "
    "A $1,000,000 target purse across seven stakes classes, planned for October 6–8, 2027, in Oklahoma City (venue pending).",
    "index.html") + f'''
<section class="hero">
  <div class="hero__media" aria-hidden="true">
    <video class="hero__video" src="assets/video/hero.mp4?v=2026073101" poster="assets/img/hero-poster.jpg?v=2026073101" autoplay muted loop playsinline preload="metadata"></video>
  </div>
  <div class="hero__scrim"></div>
  <div class="hero__drift"></div>
  <div class="hero__inner">
    <h1 class="hero__wordmark">Morgan Millions</h1>
    <p class="hero__tagline tagline">Where Rising Talent Competes on the World Stage</p>
    <p class="hero__subtagline">The Richest Purse in the Breed</p>
    <div class="hero__rule" aria-hidden="true"></div>
    {countdown()}
  </div>
</section>

<section class="statbar" aria-label="Event at a glance">
  <div class="wrap">
    <div class="statbar__grid">
      <div class="statbar__item">
        <span class="statbar__value">$1,000,000</span>
        <span class="statbar__label">Base Purse</span>
      </div>
      <div class="statbar__item">
        <span class="statbar__value">Seven</span>
        <span class="statbar__label">Stakes Classes</span>
      </div>
      <div class="statbar__item">
        <span class="statbar__value">Oct 6&ndash;8, 2027</span>
        <span class="statbar__label">Oklahoma City &middot; planned</span>
      </div>
    </div>
    <div class="statbar__cta">
      <button class="pill pill--ghost" type="button" data-placeholder="Coming Soon">Watch Live</button>
    </div>
  </div>
</section>

<section class="section on-cream">
  <div class="wrap">
    <div class="reveal" style="text-align:left">
      <p class="eyebrow">The Program</p>
      <h2 class="h-manifest">The Morgan. The stage. <span class="accent">The millions.</span></h2>
      <p class="lede" style="max-width:56rem; margin-top:2rem">One million in target purse. Seven championship classes. Three days planned in Oklahoma City. Funded by the breed itself.</p>
      <p style="margin-top:1.75rem"><a class="textlink" href="program.html">Read the program</a></p>
    </div>
  </div>
</section>

<section class="section on-cream" style="padding-top:0">
  <div class="wrap">
    <div class="cards reveal">
      <a class="card" href="program.html">
        <span class="card__index">01</span>
        <h3>The Program</h3>
        <p>The purse. The classes. The structure behind it.</p>
        <span class="card__more">Program &rarr;</span>
      </a>
      <a class="card" href="stallions.html">
        <span class="card__index">02</span>
        <h3>Vaulted Sires</h3>
        <p>Twenty permanent seats. Held in perpetuity.</p>
        <span class="card__more">Sires &rarr;</span>
      </a>
      <a class="card" href="event.html">
        <span class="card__index">03</span>
        <h3>The Event</h3>
        <p>Three days. Seven classes. One arena.</p>
        <span class="card__more">Event &rarr;</span>
      </a>
    </div>
  </div>
</section>

''' + FOOTER


# ---------------------------------------------------------------- program
CLASSES = [
    ("Pleasure Driving", "Two-Year-Old Stakes", "$250,000"),
    ("Park Harness", "Two-Year-Old Stakes", "$250,000"),
    ("Pleasure Driving", "Three &amp; Four-Year-Old Stakes", "$100,000"),
    ("Park Harness", "Three &amp; Four-Year-Old Stakes", "$100,000"),
    ("Hunter", "Three &amp; Four-Year-Old Stakes", "$100,000"),
    ("Western", "Three &amp; Four-Year-Old Stakes", "$100,000"),
    ("Road Horse", "Three &amp; Four-Year-Old Stakes", "$100,000"),
]
rows = "\n".join(
    f'''        <tr>
          <td class="name">{name}</td>
          <td>{div}</td>
          <td class="purse">{purse}</td>
        </tr>''' for name, div, purse in CLASSES)

# Reusable page hero — accepts eyebrow, title, subline
def pagehero(eyebrow, title, sub, image="assets/img/hero-a-pasture.jpg",
             alt="A bay Morgan stallion standing at attention on a Kentucky pasture at golden hour"):
    return f'''<section class="pagehero">
  <div class="pagehero__media">
    <img src="{image}" alt="{alt}" fetchpriority="high">
  </div>
  <div class="pagehero__scrim"></div>
  <div class="pagehero__inner">
    <div class="wrap">
      <p class="eyebrow">{eyebrow}</p>
      <h1 class="h-page">{title}</h1>
      <p class="pagehero__sub">{sub}</p>
    </div>
  </div>
</section>'''

# ---------- SECTION BLOCKS (reusable across pages) ----------

CLASSES_SECTION = f'''
<section class="section on-dark" id="classes">
  <div class="wrap">
    <p class="eyebrow">Classes &amp; purse</p>
    <h2 class="h-section reveal">Seven classes. Two stakes groups. One million dollars.</h2>
    <div class="table-wrap reveal" style="margin-top:3rem">
      <table class="classes">
        <caption>Target purse allocation &mdash; inaugural event, October 2027. Funded by pooled nominations, Vault seats, sponsors, and the Founders&rsquo; Circle. Declared purse pays out in full.</caption>
        <thead>
          <tr><th scope="col">Class</th><th scope="col">Stakes group</th><th scope="col" style="text-align:right">Purse</th></tr>
        </thead>
        <tbody>
{rows}
        </tbody>
        <tfoot>
          <tr>
            <td>Target purse</td>
            <td>Seven classes</td>
            <td class="purse">$1,000,000</td>
          </tr>
          <tr class="crown-row">
            <td>
              <span class="crown-eyebrow">The Crown</span>
              <span class="crown-label">Crown Purse</span>
            </td>
            <td class="crown-detail">Champion &amp; Reserve &times; 7 &mdash; 14 placings on top of every target purse</td>
            <td class="purse crown-purse">$105,000</td>
          </tr>
        </tfoot>
      </table>
    </div>
    <div class="deflist deflist--2 reveal" style="margin-top:clamp(3rem,6vw,4.5rem)">
      <div class="def">
        <h3>Two-Year-Old Stakes</h3>
        <p>Two classes at $250,000. Pleasure Driving and Park Harness &mdash; the richest ever offered to two-year-old Morgans.</p>
      </div>
      <div class="def">
        <h3>Three &amp; Four-Year-Old Stakes</h3>
        <p>Five classes at $100,000. Pleasure Driving, Park Harness, Hunter, Western, Road Horse.</p>
      </div>
    </div>
  </div>
</section>
'''

BRIDGE_SECTION = '''
<section class="section on-cream" id="bridge">
  <div class="wrap-narrow">
    <p class="h-section reveal" style="font-family:var(--display);font-style:italic;color:#8A6C3C;margin-bottom:0.5rem">The Bridge</p>
    <p class="eyebrow reveal" style="margin-bottom:1.5rem">2027 &middot; 2028 &middot; 2029 &middot; 2030</p>
    <h2 class="h-section reveal">A four-year window. Then the door closes.</h2>
    <div class="reveal" style="margin-top:2rem">
      <p class="lede">Sires already at stud, with foals on the ground before the Vault. The Bridge brings them in &mdash; once &mdash; so the first events run full.</p>
    </div>
    <div class="reveal" style="margin-top:1.75rem">
      <p><strong>Every sire with a donated breeding is eligible, and every back-nominated foal has a path, during the Bridge years.</strong> The program was built for the future, but the future doesn't start in a vacuum. Champions bred before the Vault opened deserve a lane in.</p>
      <p style="margin-top:1rem">The Bridge is that lane &mdash; a deliberate, time-limited on-ramp that lets four existing foal crops compete for Morgan Millions purses without rewriting the Vault's permanence. It runs for four events. Then the door closes, and every foal born from 2027 forward comes in the same way, through the same September&nbsp;1 nomination that will carry the program for the next fifty years.</p>
    </div>
  </div>
  <div class="wrap" style="margin-top:clamp(2.5rem,5vw,4rem)">
    <div class="duo reveal">
      <div>
        <p class="duo__label">Eligible foals</p>
        <p class="duo__line">The champions already in your barn &mdash; foals of 2023 through 2026. Four crops. One window.</p>
      </div>
      <div>
        <p class="duo__label">Program window</p>
        <p class="duo__line">2027 through 2030 events only. Hard sunset. No extensions.</p>
      </div>
    </div>
  </div>
  <div class="wrap-narrow" style="margin-top:clamp(3rem,5vw,4rem)">
    <h3 class="h-section reveal" style="font-size:clamp(1.4rem,2.4vw,2rem)">Two ways in.</h3>
    <div class="reveal" style="margin-top:1rem">
      <p>Sires and their offspring have two paths onto the Friday card. Owners pick the one that fits how their horse is already positioned.</p>
    </div>
  </div>
  <div class="wrap" style="margin-top:clamp(1.75rem,3vw,2.5rem)">
    <div class="duo reveal">
      <div>
        <p class="duo__label">Bridge Open Roster</p>
        <p class="duo__line">Sires enroll for the 2027-2029 seasons on open terms &mdash; the same nominator economics as a Vaulted seat, without buying the seat itself. When the Vault opens permanently in 2030, the roster sunsets.</p>
      </div>
      <div>
        <p class="duo__label">Guest Pass</p>
        <p class="duo__line">Individual foals can be nominated in as guests &mdash; whether their sire is elsewhere in the Bridge or never enrolled at all. A clean path for one horse without a roster commitment.</p>
      </div>
    </div>
  </div>
  <div class="wrap-narrow" style="margin-top:clamp(3rem,5vw,4rem)">
    <div class="reveal">
      <p class="eyebrow" style="margin-bottom:0.75rem">What the sunset means</p>
      <p>After the 2030 event, back-nomination closes. From the 2027 foal crop onward, every foal comes through the same forward September&nbsp;1 nomination as every crop after them. No side doors. No catch-up windows. The Bridge exists so that after it closes, the program never has to build another one.</p>
    </div>
  </div>
  <div class="wrap">
    <div class="statement-stack reveal" style="margin-top:clamp(3rem,6vw,4.5rem)">
      <p class="statement">The Vault is permanent. <span class="statement__accent">The Bridge is not.</span></p>
      <p class="statement">Four foal crops. Four events. Then it closes.</p>
    </div>
  </div>
</section>
'''

GOVERNANCE_SECTION = '''
<section class="section on-dark" id="governance">
  <div class="wrap">
    <p class="eyebrow">Governance</p>
    <h2 class="h-section reveal">Small board. Public record.</h2>
    <div class="deflist deflist--2 reveal" style="margin-top:3rem">
      <div class="def">
        <h3>Board of Directors</h3>
        <p>An independent board of directors sets policy, approves the budget, and oversees the annual audit. The executive director reports to the board.</p>
      </div>
      <div class="def">
        <h3>Advisory Council</h3>
        <p>Breeders, trainers, judges. Class conditions reviewed and recommended each year.</p>
      </div>
    </div>
  </div>
</section>
'''


# ---------- PROGRAM PAGES ----------

# Overview (repurposed program.html) — landing page for the Program section
program = (
    head("The Program — Morgan Millions",
         "How Morgan Millions is built: a $1,000,000 target purse across seven stakes classes, a $105,000 Crown Purse, and an independent board of directors.",
         "program.html")
    + pagehero("The Program",
               "By the breed. For the breed.",
               "A stakes program carrying a $1,000,000 target purse and a $105,000 Crown Purse.",
               image="assets/img/hero-chestnut-portrait-v2.jpg",
               alt="A chestnut Morgan stallion in showring bridle, high-set neck arched, long flowing tail")
    + '''
<section class="section on-dark">
  <div class="wrap-narrow">
    <p class="eyebrow">What it is</p>
    <h2 class="h-section reveal">One event. One million. One breed.</h2>
    <div class="reveal" style="margin-top:1.75rem">
      <p class="lede">Morgan Millions is a stakes program built around a single annual event &mdash; seven classes, a $1,000,000 target purse, and a $105,000 Crown Purse paid to Stallion Ticket holders on top of every placing.</p>
      <p style="margin-top:1rem">Morgan Millions carries a target purse of $1,000,000 plus a $105,000 Crown &mdash; funded each year by pooled nominations, Vault seats, sponsors, and the Founders&rsquo; Circle. The program takes no percentage of the purse; the declared purse pays out in full.</p>
    </div>
  </div>
</section>

<section class="section on-cream">
  <div class="wrap">
    <p class="eyebrow">Explore the program</p>
    <h2 class="h-section reveal" style="margin-bottom:clamp(2rem,4vw,3rem)">Six ways in.</h2>
    <div class="cards reveal">
      <a class="card card--link" href="classes.html">
        <p class="card__eyebrow">Classes &amp; Purse</p>
        <h3 class="card__title">$1M base, 7 classes</h3>
        <p class="card__body">Two stakes groups. Two-year-old and three-and-four-year-old. Every class' purse laid out.</p>
      </a>
      <a class="card card--link" href="vault.html">
        <p class="card__eyebrow">The Vault</p>
        <h3 class="card__title">20 seats. One nomination ladder.</h3>
        <p class="card__body">Vaulted, Reserve, Minted. How stallions come into the program and stay in it.</p>
      </a>
      <a class="card card--link" href="crown.html">
        <p class="card__eyebrow">The Crown Purse</p>
        <h3 class="card__title">$105,000 bonus &middot; 14 placings</h3>
        <p class="card__body">Champion and Reserve in every class, paid to the Stallion Ticket holder. Backing pedigree pays.</p>
      </a>
      <a class="card card--link" href="bridge.html">
        <p class="card__eyebrow">The Bridge</p>
        <h3 class="card__title">2027&ndash;2030 &middot; then it closes</h3>
        <p class="card__body">A four-year window for existing sires and back-nominated foals. Then the door closes.</p>
      </a>
      <a class="card card--link" href="nomination.html">
        <p class="card__eyebrow">Nomination &amp; Fees</p>
        <h3 class="card__title">How to enter</h3>
        <p class="card__body">Fee schedule, deadlines, and the September&nbsp;1 forward-nomination process.</p>
      </a>
      <a class="card card--link" href="governance.html">
        <p class="card__eyebrow">Governance</p>
        <h3 class="card__title">Independent board</h3>
        <p class="card__body">Board of directors, advisory council, and audited financials every year.</p>
      </a>
    </div>
  </div>
</section>
''' + FOOTER
)

# Classes & Purse page
classes_page = (
    head("Classes &amp; Purse — Morgan Millions",
         "Seven classes across two stakes groups. A $1,000,000 target purse. The $105,000 Crown Purse on top.",
         "classes.html")
    + pagehero("Classes &amp; Purse",
               "Seven classes. One million dollars.",
               "Two stakes groups. Two-year-old and three-and-four-year-old. Every dollar of the target purse laid out below.")
    + CLASSES_SECTION
    + FOOTER
)

# Bridge page
bridge_page = (
    head("The Bridge — Morgan Millions",
         "A four-year on-ramp for existing sires and back-nominated foals. 2027 through 2030. Then it closes.",
         "bridge.html")
    + pagehero("The Bridge",
               "A four-year window. Then the door closes.",
               "Sires already at stud, with foals on the ground before the Vault. Four events. Then a hard sunset.")
    + BRIDGE_SECTION
    + FOOTER
)

# Governance page
governance_page = (
    head("Governance — Morgan Millions",
         "Governance built around an independent board. Small board. Public record.",
         "governance.html")
    + pagehero("Governance",
               "Small board. Public record.",
               "An independent board of directors, an advisory council of breeders, trainers, and judges, and audited financials every year.")
    + GOVERNANCE_SECTION
    + FOOTER
)

# The Vault page
vault_page = (
    head("The Vault — Morgan Millions",
         "Twenty permanent seats. Two annual auction seats. One Rising Stars auction. How stallions come into Morgan Millions and stay in it.",
         "vault.html")
    + pagehero("The Vault",
               "The Vault holds twenty.",
               "Twenty permanent seats. Two annual auction seats. One annual Rising Stars auction. Every stallion who competes at Morgan Millions comes through one of these three doors.")
    + '''
<section class="section on-dark">
  <div class="wrap">
    <p class="eyebrow">The three tiers</p>
    <h2 class="h-section reveal">Vaulted. Reserve. Minted.</h2>
    <div class="deflist deflist--3 reveal" style="margin-top:3rem">
      <div class="def">
        <h3>Vaulted</h3>
        <p><strong>20 permanent seats.</strong> Public first-come, first-served. $15,000 per year in perpetuity. While current, the seat is permanent. Miss the September&nbsp;1 deadline, lose the seat.</p>
      </div>
      <div class="def">
        <h3>Reserve</h3>
        <p><strong>2 seats per year.</strong> Two annual public auctions. $15,000 minimum bid, resets every year. The winning bidder nominates a stallion of their choice for that year only. An annual entry point without permanence.</p>
      </div>
      <div class="def">
        <h3>Minted</h3>
        <p><strong>Crown Purse Auction.</strong> A mandatory annual service auction for Rising Stars &mdash; sires still building their records. No entry fee. Eligibility: fewer than 20 registered Morgan offspring as of January&nbsp;1 of the auction year.</p>
      </div>
    </div>
  </div>
</section>

<section class="section on-cream" id="vaulted">
  <div class="wrap-narrow">
    <p class="eyebrow">Tier 1 &middot; Vaulted</p>
    <h2 class="h-section reveal">Twenty seats. In perpetuity.</h2>
    <div class="reveal" style="margin-top:1.75rem">
      <p class="lede">The Vault holds twenty seats. All twenty open publicly on a first-come, first-served basis.</p>
    </div>
  </div>
  <div class="wrap" style="margin-top:clamp(2.5rem,5vw,4rem)">
    <div class="deflist deflist--2 reveal">
      <div class="def">
        <h3>How the seat works</h3>
        <p>$15,000 annual nomination, due September&nbsp;1 of the prior fall. Payable in perpetuity &mdash; the fee never escalates, the term never ends. Miss the deadline, lose the seat.</p>
        <p style="margin-top:1rem">Every Vaulted Sire donates one breeding per year to the Crown Purse Auction. 100% of the hammer price flows to the program.</p>
      </div>
      <div class="def">
        <h3>When a seat opens</h3>
        <p>When a Vaulted Sire loses his seat &mdash; missed deadline, withdrawal, or ages out &mdash; the seat is first offered to the longest-tenured Reserve-tier stallion at the $15,000 annual rate. If declined, the seat is sold through a Vaulted Seat Auction at a $15,000 minimum bid, open to anyone. The Vault always holds twenty.</p>
      </div>
    </div>
  </div>
  <div class="wrap-narrow" style="margin-top:clamp(3rem,5vw,4rem)">
    <p class="eyebrow reveal">What the Vaulted seat earns you</p>
    <div class="reveal" style="margin-top:1rem">
      <ul style="padding-left:1.25rem;line-height:1.7">
        <li>Career-long <strong>5% nominator fee</strong> on every money-winning offspring &mdash; every placing, every year, the entire competitive career. Structured as part of the placing split: <strong>85% foal owner &middot; 10% trainer &middot; 5% nominator</strong>, paid out of the $1,000,000 target purse.</li>
        <li>Eligibility for every Morgan Millions event, in perpetuity.</li>
        <li>A permanent place in the sire roster of record for the breed.</li>
      </ul>
    </div>
  </div>
</section>

<section class="section on-ink" id="charter">
  <div class="wrap-narrow">
    <p class="eyebrow">Optional &middot; The Vaulted Charter</p>
    <h2 class="h-section reveal">Seat ownership, separate from the nomination.</h2>
    <div class="reveal" style="margin-top:1.75rem">
      <p class="lede">Stallion owners may also purchase the seat itself &mdash; a transferable, leasable ownership right in the Vaulted seat, independent of the $15,000 annual nomination.</p>
    </div>
  </div>
  <div class="wrap" style="margin-top:clamp(2.5rem,5vw,4rem)">
    <div class="deflist deflist--2 reveal">
      <div class="def">
        <h3>Introductory pricing</h3>
        <p>$10,000 introductory Charter, offered only to the original 20 Vaulted stallion owners. 30-day right of first refusal at nomination acceptance.</p>
        <p style="margin-top:1rem">After the founding window, remaining Charters release in tranches over Years 1&ndash;5 at market price set by Morgan Millions. Capped at 4 Charters per beneficial owner.</p>
      </div>
      <div class="def">
        <h3>Sitting tenant rule</h3>
        <p>An incumbent Vaulted stallion meeting his obligations cannot be displaced by a Charter sale. A new Charter owner acquires the seat <em>subject to</em> the existing tenancy &mdash; the incumbent re-nominates each year until he ages out, fails the rule, or is withdrawn.</p>
        <p style="margin-top:1rem">Only then does the Charter owner take active possession of the seat.</p>
      </div>
    </div>
  </div>
  <div class="wrap-narrow" style="margin-top:clamp(2.5rem,5vw,3.5rem)">
    <div class="reveal">
      <p>A Charter must have a nominated stallion by the September&nbsp;1 deadline (or a sitting tenant in place) or it is forfeited &mdash; no refund. 100% of resale proceeds flow to Morgan Millions.</p>
    </div>
    <p class="eyebrow reveal" style="margin-top:2rem">What the Charter earns you</p>
    <div class="reveal" style="margin-top:0.75rem">
      <ul style="padding-left:1.25rem;line-height:1.7">
        <li>Property right in the Vaulted seat &mdash; transferable, leasable, part of your estate.</li>
        <li>Right to nominate any qualifying stallion into the seat you own.</li>
        <li>No governance vote. The Charter is an economic right only.</li>
      </ul>
    </div>
  </div>
</section>

<section class="section on-cream" id="reserve">
  <div class="wrap-narrow">
    <p class="eyebrow">Tier 2 &middot; Reserve</p>
    <h2 class="h-section reveal">The annual seats.</h2>
    <div class="reveal" style="margin-top:1.75rem">
      <p class="lede">Two public seats are auctioned every year to the Morgan community.</p>
    </div>
  </div>
  <div class="wrap" style="margin-top:clamp(2.5rem,5vw,4rem)">
    <div class="duo reveal">
      <div>
        <p class="duo__label">Mechanics</p>
        <p class="duo__line">$15,000 minimum bid, resets annually. No cap. Winning bidder enrolls a stallion they own (or hold breeding rights to) for one show season. Same requirements as Vaulted &mdash; the enrolled stallion donates one breeding to the Crown Purse Auction, and his foals compete in the mature program cohort as they age up. Reserve does not carry Vaulted permanence.</p>
      </div>
      <div>
        <p class="duo__label">Nominator economics</p>
        <p class="duo__line">Reserve nominators earn the same career-long 5% nominator fee on money-winning offspring &mdash; every placing splits <strong>85 / 10 / 5</strong> across foal owner, trainer, and nominator. Reserve is treated the same as Vaulted for revenue-share purposes.</p>
      </div>
    </div>
  </div>
  <div class="wrap-narrow" style="margin-top:clamp(2.5rem,5vw,3.5rem)">
    <div class="reveal">
      <p>Reserve is the annual door. With two seats auctioned each year, any qualifying stallion owner has a shot at enrolling on the same footing as Vaulted &mdash; one show season at a time.</p>
    </div>
  </div>
</section>

<section class="section on-dark" id="minted">
  <div class="wrap-narrow">
    <p class="eyebrow">Tier 3 &middot; Minted</p>
    <h2 class="h-section reveal">Rising Stars.</h2>
    <div class="reveal" style="margin-top:1.75rem">
      <p class="lede">A mandatory annual service auction for Rising Stars &mdash; sires still building their record.</p>
    </div>
  </div>
  <div class="wrap" style="margin-top:clamp(2.5rem,5vw,4rem)">
    <div class="deflist deflist--2 reveal">
      <div class="def">
        <h3>Eligibility</h3>
        <p>Fewer than 20 registered Morgan offspring as of January&nbsp;1 of the auction year &mdash; verified against AMHA registration records. No entry fee. The seller carries a combined $2,500 seller-guaranteed floor.</p>
      </div>
      <div class="def">
        <h3>How it works</h3>
        <p>The winning bidder receives one breeding. Any foal resulting is eligible to compete the following Morgan Millions year. The one-nomination-ladder rule applies.</p>
      </div>
    </div>
  </div>
  <div class="wrap-narrow" style="margin-top:clamp(2.5rem,5vw,3.5rem)">
    <div class="reveal">
      <p>Minted does not earn a nominator fee for the sire owner &mdash; that is reserved for Vaulted and Reserve. The 10% trainer share still applies to every Minted offspring that hits the money. What Minted provides for the sire is the pathway: a Rising Star builds his book at the Crown Purse Auction, his offspring compete the following year, and if the record justifies it, he is positioned to take a Vaulted seat when one opens.</p>
    </div>
  </div>
</section>

<section class="section on-cream">
  <div class="wrap-narrow">
    <p class="eyebrow">One nomination ladder</p>
    <h2 class="h-section reveal">Every foal. No carveouts.</h2>
    <div class="reveal" style="margin-top:1.75rem">
      <p class="lede">The $500&nbsp;/&nbsp;$500&nbsp;/&nbsp;$500&nbsp;/&nbsp;$1,500 nomination ladder applies to every single foal that wants to compete at Morgan Millions.</p>
      <p style="margin-top:1rem">No exemptions for Vaulted donated breedings. No exemptions for Minted auction breedings. No carveouts for Charter holders. One program. One set of rules. Every foal earns its place on the same terms.</p>
      <p style="margin-top:1.5rem"><a class="pill pill--ghost" href="nomination.html">Full nomination detail &rarr;</a></p>
    </div>
  </div>
</section>

<section class="section on-dark">
  <div class="wrap-narrow">
    <p class="eyebrow">What the seat does NOT do</p>
    <h2 class="h-section reveal">Economics, not governance.</h2>
    <div class="reveal" style="margin-top:1.75rem">
      <p class="lede">Vaulted and Reserve seats are economic and property rights. They earn nominator fees, they qualify offspring to compete, they hold their value through the transfer market. They are not seats on the board.</p>
      <ul style="padding-left:1.25rem;line-height:1.7;margin-top:1.5rem">
        <li>Vaulted and Reserve Charter Holders do not vote on program governance.</li>
        <li>Board decisions &mdash; budget, purse structure, class list, hiring the Director &mdash; sit with the program board.</li>
        <li>Every Charter is protected as a property right. No board vote can dilute it, redirect its cash flow, or dissolve the seat.</li>
      </ul>
      <p style="margin-top:1.5rem">The separation is intentional. Charters are for the breed. Governance is for the program. Neither should be able to override the other.</p>
      <p style="margin-top:1.5rem"><a class="pill pill--ghost" href="governance.html">How governance works &rarr;</a></p>
    </div>
  </div>
</section>

<section class="section on-cream">
  <div class="wrap">
    <div class="statement-stack reveal">
      <p class="statement">Vaulted first-come open: <span class="statement__accent">Q4 2026.</span></p>
      <p class="statement">Reserve auction opens: Q4 2026.</p>
      <p class="statement">Minted auction: annual, beginning 2026.</p>
    </div>
  </div>
</section>
''' + FOOTER
)

# The Crown Purse page
crown_page = (
    head("The Crown Purse — Morgan Millions",
         "A $105,000 producing-sire bonus. Sold at the Crown Purse Auction, paid at Friday finals. Fourteen ways to win.",
         "crown.html")
    + pagehero("The Crown Purse",
               "$105,000 on top of the base.",
               "A producing-sire bonus, sold at the Crown Purse Auction, paid at Friday finals. Fourteen ways to win. Up to $105,000 to a single Crown Holder if one sire sweeps the show.")
    + '''
<section class="section on-cream">
  <div class="wrap-narrow">
    <p class="eyebrow">The mechanic</p>
    <h2 class="h-section reveal">How a Stallion Ticket works.</h2>
    <div class="reveal" style="margin-top:1.75rem">
      <p class="lede">Every Crown-eligible sire issues exactly one Stallion Ticket per show season. <strong>That ticket is included with the auctioned stud fee</strong> for that sire at the annual Crown Purse Auction &mdash; for the following year\'s Morgan Millions event.</p>
      <p style="margin-top:1rem">The buyer of that breeding becomes the <strong>Crown Holder</strong> for the upcoming show season.</p>
      <p style="margin-top:1rem">The ticket is on the <em>sire</em>, not on a specific foal. If any foal by that sire places at the Morgan Millions event, the Crown Holder collects &mdash; independent of who owns the winning foal.</p>
    </div>
  </div>
</section>

<section class="section on-dark" id="math">
  <div class="wrap">
    <p class="eyebrow">The math</p>
    <h2 class="h-section reveal">Per class. Per sire. Per show.</h2>
    <div class="table-wrap reveal" style="margin-top:3rem">
      <table class="classes">
        <caption>Crown Purse payout &mdash; per class and full-sweep annual maximum</caption>
        <thead>
          <tr><th scope="col">Placing</th><th scope="col">Per class</th><th scope="col" style="text-align:right">Across 7 classes</th></tr>
        </thead>
        <tbody>
          <tr><td class="name">Champion payout</td><td>$10,000</td><td class="purse">up to $70,000</td></tr>
          <tr><td class="name">Reserve payout</td><td>$5,000</td><td class="purse">up to $35,000</td></tr>
        </tbody>
        <tfoot>
          <tr>
            <td>Total per class</td>
            <td>$15,000</td>
            <td class="purse">up to $105,000</td>
          </tr>
        </tfoot>
      </table>
    </div>
    <div class="wrap-narrow" style="margin-top:clamp(2.5rem,5vw,3.5rem);padding:0">
      <p class="reveal"><strong>14 ways to win</strong> &mdash; Champion + Reserve &times; 7 classes.</p>
      <p class="reveal" style="margin-top:1rem">A single sire can produce both winners &mdash; one foal takes Champion, another takes Reserve, both by the same sire, and both placings pay the Crown Holder. Across seven classes, that\'s fourteen possible placings for one Crown Holder to collect.</p>
      <p class="reveal" style="margin-top:1rem"><strong>Annual maximum:</strong> if a single sire produces both Champion and Reserve in every class &mdash; a full sweep &mdash; the Crown Holder collects the entire $105,000.</p>
    </div>
  </div>
</section>

<section class="section on-ink">
  <div class="wrap">
    <p class="eyebrow">When and how it pays</p>
    <h2 class="h-section reveal">Paid Friday. Same night.</h2>
    <div class="deflist deflist--2 reveal" style="margin-top:3rem">
      <div class="def">
        <h3>Timing</h3>
        <p>Crown Purse is awarded during <strong>Friday finals</strong> &mdash; the same night the class purse is distributed. Reserve is always paid &mdash; no threshold, no cutoff.</p>
      </div>
      <div class="def">
        <h3>Recipient</h3>
        <p>Payment goes to the Crown Holder (the Crown Purse Auction buyer), regardless of who owns the foal. <strong>Double-dip allowed:</strong> if the Crown Holder also owns the winning foal, they collect the class purse and the Crown bonus on top.</p>
      </div>
    </div>
  </div>
</section>

<section class="section on-cream">
  <div class="wrap-narrow">
    <p class="eyebrow">Secondary market</p>
    <h2 class="h-section reveal">Freely transferable.</h2>
    <div class="reveal" style="margin-top:1.75rem">
      <p class="lede">Stallion Tickets are freely transferable all year, until championships are awarded Friday night. No lock-on event. The ticket follows the sire, not a foal.</p>
      <ul style="padding-left:1.25rem;line-height:1.7;margin-top:1.5rem">
        <li>Buy at the Crown Purse Auction, hold or resell as the foal crop develops.</li>
        <li>Owners of promising foals can consolidate &mdash; buy the ticket for the sire of their contender.</li>
        <li>Anyone can trade based on how a sire\'s foal crop is performing through the year.</li>
      </ul>
      <p style="margin-top:1.5rem">The moment championships are decided Friday night, the ticket\'s value crystallizes &mdash; pay out or expire.</p>
    </div>
  </div>
</section>

<section class="section on-dark" id="eligible">
  <div class="wrap-narrow">
    <p class="eyebrow">Who issues a ticket</p>
    <h2 class="h-section reveal">Every enrolled sire issues a ticket.</h2>
  </div>
  <div class="wrap" style="margin-top:clamp(2rem,4vw,3rem)">
    <div class="deflist deflist--2 reveal">
      <div class="def">
        <h3>Vaulted Sires</h3>
        <p>Every seat donates one breeding per show season to the Crown Purse Auction &mdash; required. That breeding issues one Stallion Ticket.</p>
      </div>
      <div class="def">
        <h3>Reserve Sires</h3>
        <p>Every Reserve seat issues one ticket per show season, at the annual Crown Purse Auction. The donated breeding is required, same as Vaulted.</p>
      </div>
      <div class="def">
        <h3>Minted Sires</h3>
        <p>Every sire in the Crown Purse Auction issues one ticket per year, same auction.</p>
      </div>
      <div class="def">
        <h3>Bridge Open Roster</h3>
        <p>Every Bridge Open Roster sire issues one ticket per show season during Bridge years (2027&ndash;2030), same auction. <a href="bridge.html" style="color:var(--brass-light)">See The Bridge &rarr;</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section on-cream">
  <div class="wrap-narrow">
    <p class="eyebrow">What the Crown Purse is NOT</p>
    <h2 class="h-section reveal">Not the target purse. Not a class.</h2>
    <div class="reveal" style="margin-top:1.75rem">
      <ul style="padding-left:1.25rem;line-height:1.7">
        <li><strong>Not paid out of the $1M target purse.</strong> The Crown Purse is a separate $105,000 pool, funded by the Auction Crown ticket sales.</li>
        <li><strong>Not a separate class.</strong> No one enters "the Crown." Any foal that wins a target-purse placing triggers a Crown payout for whoever holds that sire\'s ticket.</li>
        <li><strong>Not paid to the foal owner.</strong> The class purse (target) pays out in the placing split &mdash; 85% foal owner, 10% trainer, 5% nominator. The Crown Purse pays the ticket holder. Two separate checks from the same Friday-night ceremony.</li>
      </ul>
    </div>
  </div>
</section>

<section class="section on-dark">
  <div class="wrap">
    <div class="statement-stack reveal">
      <p class="statement">First Crown Purse Auction: <span class="statement__accent">2026 (online),</span> for 2027 event eligibility.</p>
      <p class="statement">Live at the Crown Purse Auction from 2027 forward.</p>
    </div>
  </div>
</section>
''' + FOOTER
)

# Nomination placeholder
nomination_page = (
    head("Nomination &amp; Fees — Morgan Millions",
         "Fee schedule and nomination deadlines. Publishing ahead of the September 1, 2026 forward-nomination window.",
         "nomination.html")
    + pagehero("Nomination &amp; Fees",
               "Coming soon.",
               "The full fee schedule, deadlines, and September 1 forward-nomination process. Publishing ahead of the 2026 window.")
    + '''
<section class="section on-dark">
  <div class="wrap-narrow">
    <p class="eyebrow">Publishing soon</p>
    <h2 class="h-section reveal">The paperwork side.</h2>
    <div class="reveal" style="margin-top:1.75rem">
      <p class="lede">Every fee, every deadline, every form. Bridge Open Roster terms, Guest Pass terms, and the September&nbsp;1 forward-nomination window that carries the program from 2027 onward.</p>
      <p style="margin-top:1rem">Publishing ahead of the 2026 nomination window. Prize list, entry form, and a fee schedule you can print and sign.</p>
      <p style="margin-top:2rem">In the meantime, browse the rest of the program.</p>
      <p style="margin-top:1.5rem"><a class="pill pill--ghost" href="program.html">Back to Program overview</a></p>
    </div>
  </div>
</section>
''' + FOOTER
)

# ---------------------------------------------------------------- For Trainers
for_trainers_page = (
    head("For Trainers &mdash; Morgan Millions",
         "$100,000 a year to trainers. 10% of every placing. Structured into the placing split, not a tip.",
         "for-trainers.html")
    + pagehero("For Trainers",
               "$100,000 to trainers. Every year.",
               "Ten percent of every placing. Guaranteed by structure.",
               image="assets/img/hero-chestnut-portrait-v2.jpg",
               alt="A chestnut Morgan stallion in showring bridle, high-set neck arched, long flowing tail")
    + '''
<section class="section on-ink" style="padding-top:clamp(2rem,4vw,3rem);padding-bottom:clamp(2rem,4vw,3rem)">
  <div class="wrap-narrow" style="text-align:center">
    <p class="eyebrow" style="margin-bottom:1.25rem">Ready to nominate your barn&rsquo;s next campaigner?</p>
    <a class="pill" href="nomination.html">Nominate a foal &rarr;</a>
  </div>
</section>

<section class="section on-cream">
  <div class="wrap-narrow">
    <p class="eyebrow">How trainers get paid</p>
    <h2 class="h-section reveal">10% of every placing goes to the trainer.</h2>
    <div class="reveal" style="margin-top:1.75rem">
      <p class="lede">Every dollar of the $1,000,000 target purse pays out in one split: <strong>85% foal owner &middot; 10% trainer &middot; 5% nominator</strong>. Every placing, every class, every year.</p>
    </div>
  </div>
</section>

<section class="section on-dark">
  <div class="wrap">
    <div class="statement-stack reveal">
      <p class="statement"><span class="statement__accent">$100,000</span> to trainers, aggregate, on a full $1M target purse.</p>
      <p class="statement"><span class="statement__accent">10%</span> of every single placing &mdash; Champion through 10th.</p>
      <p class="statement"><span class="statement__accent">Every year.</span> Guaranteed by structure.</p>
    </div>
  </div>
</section>

<section class="section on-cream">
  <div class="wrap-narrow">
    <p class="eyebrow">Worked example</p>
    <h2 class="h-section reveal">A $250,000 two-year-old class.</h2>
    <div class="reveal" style="margin-top:1.75rem">
      <p class="lede">Champion takes 40% of the class purse: $100,000. That $100,000 splits three ways.</p>
      <ul style="padding-left:1.25rem;line-height:1.9;margin-top:1.5rem">
        <li><strong>Foal owner:</strong> $85,000</li>
        <li><strong>Trainer:</strong> $10,000</li>
        <li><strong>Nominator (Vaulted or Reserve sire owner):</strong> $5,000</li>
      </ul>
      <p style="margin-top:1.5rem">Reserve takes 20%: $50,000. That splits $42,500 / $5,000 / $2,500. Every subsequent placing splits the same way, all the way through 10th. Fourteen possible placings across the seven classes for the trainer of the winning barn on any given year.</p>
    </div>
  </div>
</section>

<section class="section on-cream">
  <div class="wrap-narrow">
    <p class="eyebrow">What counts as the trainer</p>
    <h2 class="h-section reveal">The trainer of record at the show.</h2>
    <div class="reveal" style="margin-top:1.75rem">
      <p class="lede">Declared on the entry form. Verified against the show program. Paid on the same night as the class purse.</p>
      <p style="margin-top:1rem">An amateur owner who trains and shows their own horse still triggers the 10% trainer share &mdash; it flows to whoever the entry form declares as trainer of record. If that is the owner, that is where it lands. If it is a professional barn, that is where it lands.</p>
      <p style="margin-top:1rem">This is a placing-based mechanic, not an employment mechanic. The program does not adjudicate barn contracts. It writes one line in the payout &mdash; 10% of every placing to the declared trainer &mdash; and the paperwork side handles the rest.</p>
    </div>
  </div>
</section>

<section class="section on-dark">
  <div class="wrap-narrow">
    <p class="eyebrow">Back-nominated foals (Bridge years, 2027&ndash;2030)</p>
    <h2 class="h-section reveal">The 10% trainer share triggers on back-noms.</h2>
    <div class="reveal" style="margin-top:1.75rem">
      <p class="lede">A back-nominated foal &mdash; a horse born before the Vault opened, entering through the Bridge &mdash; still pays the trainer 10% of every placing.</p>
      <p style="margin-top:1rem">The trainer share is unconditional. It does not depend on how the foal came into the program. If a horse hits the money at Morgan Millions, the trainer of record gets 10% of that money.</p>
    </div>
  </div>
</section>

<section class="section on-cream">
  <div class="wrap-narrow" style="text-align:center">
    <p class="reveal"><a class="pill" href="nomination.html">Nominate a foal &rarr;</a> &nbsp; <a class="pill pill--ghost" href="program.html">Read the full program</a></p>
  </div>
</section>
''' + FOOTER
)


# ---------------------------------------------------------------- stallions
# Vaulted Sires — first announced stallions. Seats 08-20 remain awaiting announcement.
VAULTED = [
    {
        "name": "MLF Dynamic GCH",
        "call": None,
        "tagline": "World Champion. Written into every foal he sires.",
        "pitch": "After an exceptional show ring career, World Champion MLF Dynamic GCH is poised to leave his legacy in the breeding shed. His first foals are already proving their quality, earning Oklahoma victory passes both in hand and in harness. Among them is the standout two-year-old RHMF Mojo Rising, whose impressive win at the New England Morgan Horse Show has everyone talking. The future is already here. Don&rsquo;t just admire his offspring from the rail &mdash; breed to MLF Dynamic GCH and become part of the next dynamic generation.",
        "pedigree": "Dragonsmeade Sea Dragon CH × RWF On Display",
        "foaled": None,
        "standing": "Owned by Eldon Lambright · Managed by Midstates Equine",
        "image": "assets/img/stallions/mlf-dynamic.jpg",
        "image_pos": "center center",
    },
    {
        "name": "Merriehill After Hours GCH",
        "call": "Puck",
        "tagline": "A legendary show horse. An exceptional sire. A lasting legacy.",
        "pitch": "Merriehill After Hours GCH has distinguished himself as one of the most influential Morgan stallions of his generation, earning acclaim both in the show ring and in the breeding barn. Throughout his remarkable tricolor career, &lsquo;Puck&rsquo; amassed an extraordinary record highlighted by multiple World Championship titles. His accomplishments include earning the prestigious World Champion Stallion title four times, along with numerous World Championships in English Pleasure competition. Sired by Mizrahi and out of Merriehill Dusk To Dawn, he embodies the beauty, athleticism, and charisma that define the modern Morgan horse. His influence extends far beyond his own achievements. Consistently recognized among the leading sires in the Saddle Horse Report Breeders&rsquo; Report, Merriehill After Hours GCH continues to shape the future of the breed through an exceptional collection of offspring. Notable offspring include Sing It CH, Another Lucid Dream, Cingate All Star GCH, Bling It, Oxsana, Bring It, NEF Transcend GCH, Busy Hour, Cherrydale Closing Time, HVK Summer Night CH, Merriehill Justify GCH, and Another Crazy Idea, and many more. From his unmatched presence in the show ring to his proven ability to produce world-class performers, Merriehill After Hours GCH remains a cornerstone of Morgan horse excellence &mdash; a stallion whose legacy continues to inspire each new generation.",
        "pedigree": "Mizrahi × Merriehill Dusk To Dawn BHOF",
        "foaled": "Bay · 2010 · AMHA 182452",
        "standing": "Midstates Equine · Sammi Hazen, agent",
        "image": "assets/img/stallions/merriehill.jpg",
        "image_pos": "center 30%",
    },
    {
        "name": "Jus' Sayin' CH",
        "call": None,
        "tagline": "Unanimous World Champion at two. Then he went straight to the shed.",
        "pitch": "He walked into Oklahoma as a two-year-old &mdash; and walked out the Unanimous World Champion Stallion. In his debut season, he captured the attention of the Morgan world, earning the prestigious 2021 People&rsquo;s Choice Horse of the Year title and establishing himself as one of the breed&rsquo;s brightest young stars. His very first foal crop made an unforgettable debut, producing multiple World Champions as two-year-olds and confirming his ability to pass on the quality, athleticism, and charisma that define true greatness. From an unforgettable start in the show ring to an extraordinary beginning as a sire, his legacy is only just beginning.",
        "pedigree": "Dragonsmeade Axios × Brenda Starr",
        "foaled": "Foaled 2019",
        "standing": "Salem Farm, Vermont · Peggy & Phil Alderman",
        "image": "assets/img/stallions/jus-sayin-v3.jpg",
        "image_pos": "center center",
    },
    {
        "name": "RWF Gettysburg CH",
        "call": "Bryan",
        "tagline": "2023 World Champion Stallion. Unanimous.",
        "pitch": "The ultimate product of the RWF breeding program. 2023 World Champion Stallion. 2024 and 2025 Regional Champion Stallion In-Hand. 2025 Grand National 4YO Stallion. Triple-bred to Waseeka's In Command — the kind of pedigree that only comes together on paper once a decade.",
        "pedigree": "Get Busy × SPR Music By Starlight",
        "foaled": "Bay · 2021 · AMHA 201623",
        "standing": "Clayhill Farm · frozen semen only",
        "image": "assets/img/stallions/rwf-gettysburg.jpg",
        "image_pos": "center center",
    },
    {
        "name": "Extreme Sensation",
        "call": None,
        "tagline": "Lived up to the name from the first go.",
        "pitch": "Won his 3YO Park Saddle qualifier and finished Reserve Champion in Junior Park Saddle in the same debut season.",
        "pedigree": "RL Jackpot \u00d7 FAMS Halleberry Ovation",
        "foaled": None,
        "standing": "Details forthcoming",
        "image": "assets/img/stallions/extreme-sensation.jpg",
        "image_pos": "center center",
    },
    {
        "name": "DJS Select Bourbon",
        "call": None,
        "tagline": "A rising sire the industry is already watching.",
        "pitch": "DJS Select Bourbon made a remarkable show ring debut in 2025. At just four years old, the talented young stallion has already emerged as one of the breed&rsquo;s most promising stars, showcasing exceptional athleticism, balance, and undeniable ring presence. With an elite pedigree, early championship success, and the first signs of his influence already emerging in his offspring, DJS Select Bourbon is poised to make a lasting impact on the Morgan breed for years to come. His oldest foals are now yearlings, while the majority of his first crop arrived this year and are already displaying the elegance, motion, and upright build that define their sire. Frozen semen is available for the 2027 breeding season.",
        "pedigree": None,
        "foaled": None,
        "standing": "Details forthcoming",
        "image": "assets/img/stallions/djs-bourbon-v2.jpg",
        "image_pos": "center center",
    },
    {
        "name": "Get Busy",
        "call": None,
        "tagline": "World Champion. Proven Producer. Lasting Legacy.",
        "pitch": "Get Busy represents the rare combination of championship performance, exceptional pedigree, and lasting breeding influence. A World Champion in his own right, he has earned a reputation not only for his success in the show ring but for consistently passing his talent, presence, and athleticism to the next generation. With a pedigree built on excellence and offspring that continue to excel on the world&rsquo;s biggest stages, Get Busy has established himself as a sire whose impact extends far beyond his own accomplishments. His foals are recognized for their beauty, trainability, motion, and winning attitude &mdash; qualities that have made them standouts in the show ring and sought-after prospects for breeders. For those looking to invest in proven genetics backed by championship performance, Get Busy offers a legacy of excellence that continues to grow with every foal crop.",
        "pedigree": "Astronomicallee × So Vain",
        "foaled": None,
        "standing": "By private treaty",
        "image": "assets/img/stallions/get-busy.jpg",
        "image_pos": "center center",
    },
    {
        "name": "Man In Black GCH",
        "call": None,
        "tagline": "A brilliant show horse. An even more exceptional sire.",
        "pitch": "Man In Black GCH was a brilliant show horse and has proven to be an even more exceptional sire, consistently producing generations of talented Morgans stamped with his unmistakable elegance, athleticism, and presence. A sire of World Champions across every major division &mdash; including In-Hand, Park Saddle, Pleasure Driving, Classic Pleasure, Western, and Hunter Pleasure &mdash; his record speaks for itself. His pedigree is equally remarkable, featuring four Hall of Fame broodmares within the first three generations and an ideal concentration of the legendary Man About Town LPS bloodline. This exceptional genetic foundation crosses beautifully with a wide variety of sire lines, producing versatile, high-quality show horses with lasting appeal. From standouts like Ledyard Oberon GCH, Ledyard the Rebel GCH, Ledyard Walk the Line, and Ledyard Solitary Man to the champions still to come, the results continue to prove his influence.",
        "pedigree": "Town Assets \u00d7 Town Sweetheart",
        "foaled": "Black \u00b7 2008 \u00b7 AMHA 177929",
        "standing": "Owned by Danny & Diana Viall \u00b7 Standing at Mid States Equine, Bloomfield IA",
        "image": "assets/img/stallions/man-in-black.jpg",
        "image_pos": "center 30%",
    },
    {
        "name": "A Star Is Born",
        "call": None,
        "tagline": "Announced. Full profile forthcoming.",
        "pitch": "Vaulted Seat confirmed. Pedigree, show record, and standing farm to be published as enrollment closes.",
        "pedigree": None,
        "foaled": None,
        "standing": "Details forthcoming",
        "image": "assets/img/stallions/a-star-is-born.jpg",
        "image_pos": "center center",
    },
]


def _stallion_card(s, num):
    call_line = f'<p class="card__call">&ldquo;{s["call"]}&rdquo;</p>' if s.get("call") else ""

    # Full-bleed portrait header (or forthcoming placeholder)
    if s.get("image"):
        pos = s.get("image_pos") or "center center"
        # Two-layer photo, both as <img> elements to keep browser URL resolution consistent
        # (CSS variables + pseudo-elements resolve URLs relative to the CSS file location,
        # breaking on nested asset paths). The blur backdrop fills letterbox pillars with a
        # cover-sized, heavily blurred/darkened same-photo bloom; the sharp subject sits on
        # top at contain-size, position-controlled per stallion via object-position.
        portrait = f'''<div class="card__portrait">
          <img class="card__portrait-blur" src="{s["image"]}" alt="" aria-hidden="true" loading="lazy">
          <img class="card__portrait-sharp" src="{s["image"]}" alt="" aria-hidden="true" loading="lazy" style="object-position:{pos};">
          <span class="card__seat">Vaulted Seat {num:02d}</span>
        </div>'''
    else:
        portrait = f'''<div class="card__portrait card__portrait--empty">
          <span class="card__seat">Vaulted Seat {num:02d}</span>
          <span class="card__portrait-note">Portrait forthcoming</span>
        </div>'''

    # Fine-print row: pedigree · foaled/color/AMHA
    fine_bits = []
    if s.get("pedigree"):
        fine_bits.append(f'<span class="card__pedigree">{s["pedigree"]}</span>')
    if s.get("foaled"):
        fine_bits.append(f'<span class="card__foaled">{s["foaled"]}</span>')
    fine_line = ('<div class="card__fine">' + "".join(fine_bits) + "</div>") if fine_bits else ""

    foot_line = f'<footer class="card__foot"><span class="card__standing">{s["standing"]}</span></footer>' if s.get("standing") else ''

    # Data payload for editorial modal — escape quotes
    def _e(v):
        return (v or "").replace('"', '&quot;').replace("'", "&#39;")

    modal_attrs = (
        f'data-modal="stallion" '
        f'data-name="{_e(s["name"])}" '
        f'data-call="{_e(s.get("call"))}" '
        f'data-tagline="{_e(s["tagline"])}" '
        f'data-pitch="{_e(s["pitch"])}" '
        f'data-pedigree="{_e(s.get("pedigree"))}" '
        f'data-foaled="{_e(s.get("foaled"))}" '
        f'data-standing="{_e(s.get("standing"))}" '
        f'data-image="{_e(s.get("image"))}" '
        f'data-image-pos="{_e(s.get("image_pos") or "center center")}" '
        f'data-seat="{num:02d}" '
        f'role="button" tabindex="0" aria-haspopup="dialog" aria-label="Open profile for {_e(s["name"])}"'
    )

    return f'''      <article class="card--stallion is-clickable" {modal_attrs}>
        {portrait}
        <div class="card__body">
          <div class="card__lead">
            <h3 class="card__name">{s["name"]}</h3>
            {call_line}
            <p class="card__tagline">{s["tagline"]}</p>
          </div>
          <p class="card__pitch">{s["pitch"]}</p>
          {fine_line}
          {foot_line}
          <span class="card__view" aria-hidden="true">View the profile <span class="card__view-arrow">&rarr;</span></span>
        </div>
      </article>'''


cards = [_stallion_card(s, i) for i, s in enumerate(VAULTED, start=1)]
for i in range(len(VAULTED) + 1, 21):
    cards.append(f'''      <article class="card--stallion card--stallion-muted">
        <span class="card__seat">Vaulted Seat {i:02d}</span>
        <span class="card__status">Awaiting announcement</span>
      </article>''')
seat_grid = "\n".join(cards)

stallions = head(
    "Vaulted Sires — Morgan Millions",
    "The Vaulted Sires program: twenty permanent Morgan stallion seats at $15,000 per year, two Reserve "
    "Seats offered annually at auction, and the Bridge program for Charter Holders.",
    "stallions.html") + f'''
<section class="pagehero pagehero--portrait">
  <div class="pagehero__media">
    <img src="assets/img/hero-c-eye-full.jpg" alt="Close-up portrait of a chestnut Morgan stallion&#39;s head, warm rembrandt lighting highlighting the eye and full face" fetchpriority="high">
  </div>
  <div class="pagehero__scrim"></div>
  <div class="pagehero__inner">
    <div class="wrap">
      <p class="eyebrow">Vaulted Sires</p>
      <h1 class="h-page">Twenty Sires. One Vault.</h1>
      <p class="pagehero__sub">The stallions whose foals compete for a million dollars.</p>
    </div>
  </div>
</section>

<section class="earners reveal">
  <div class="earners__intro">
    <p class="earners__kicker">The payout stack</p>
    <h2 class="earners__headline">Four earners. One nomination.</h2>
    <p class="earners__sub">Every placing at Morgan Millions creates four checks.</p>
  </div>
  <div class="earners__grid">
    <div class="earners__tile">
      <span class="earners__value">85%</span>
      <span class="earners__role">Foal Owner</span>
      <span class="earners__note">of the class purse</span>
    </div>
    <div class="earners__tile">
      <span class="earners__value">10%</span>
      <span class="earners__role">Trainer</span>
      <span class="earners__note">of every placing</span>
    </div>
    <div class="earners__tile">
      <span class="earners__value">5%</span>
      <span class="earners__role">Nominator</span>
      <span class="earners__note">of every placing</span>
    </div>
    <div class="earners__tile">
      <span class="earners__value">+ Bonus</span>
      <span class="earners__role">Crown Holder</span>
      <span class="earners__note">from the Crown Purse</span>
    </div>
  </div>
</section>

<section class="section on-ink">
  <div class="wrap">
    <p class="eyebrow">The Vault</p>
    <h2 class="h-section reveal">Seats 01 &ndash; 20</h2>
    <p class="figure-caption reveal" style="margin-top:0.75rem">Eight announced. Twelve to come.</p>
    <div class="seats reveal" style="margin-top:3rem">
{seat_grid}
    </div>
  </div>
</section>

<section class="section on-cream">
  <div class="wrap-narrow">
    <p class="eyebrow" style="margin-bottom:2.5rem">The Vault</p>
    <div class="statement-stack reveal">
      <p class="statement">Twenty stallions.<br><span class="statement__accent">One permanent record.</span></p>
      <p class="statement">The seat is for life.</p>
      <p class="statement">Every foal, eligible.</p>
    </div>
  </div>
</section>

<section class="section on-ink">
  <div class="wrap">
    <div class="duo reveal" id="bridge">
      <div>
        <p class="duo__label">Reserve</p>
        <p class="duo__line">When the twenty are full,<br>two seats open a year.</p>
      </div>
      <div>
        <p class="duo__label">Bridge</p>
        <p class="duo__line">For sires already at stud &mdash;<br>foals 2023 to 2026 come with.</p>
      </div>
    </div>
  </div>
</section>

<section class="section on-cream">
  <div class="wrap">
    <div class="split reveal">
      <figure class="split__media" style="margin:0">
        <img src="assets/img/hero-b-barn.jpg" alt="Warm brass lantern light down the aisle of a traditional Morgan stallion barn at dusk" loading="lazy">
      </figure>
      <div class="split__body">
        <p class="eyebrow">Enrollment</p>
        <h2 class="h-section">A seat in the Vault.</h2>
        <p class="lede">Enrollment opens ahead of the inaugural event.</p>
        <p style="margin-top:1.75rem"><a class="textlink" href="program.html">Read the program</a></p>
      </div>
    </div>
  </div>
</section>

<!-- Editorial-spread modal for stallion profiles -->
<div class="stallion-modal" id="stallion-modal" role="dialog" aria-modal="true" aria-labelledby="stallion-modal-name" hidden>
  <div class="stallion-modal__backdrop" data-modal-close></div>
  <div class="stallion-modal__frame" role="document">
    <button class="stallion-modal__close" type="button" data-modal-close aria-label="Close profile">
      <span aria-hidden="true">&times;</span>
    </button>
    <div class="stallion-modal__portrait">
      <span class="stallion-modal__seat" data-modal-seat></span>
      <div class="stallion-modal__portrait-fallback" data-modal-fallback hidden>
        <span data-modal-fallback-note>Portrait forthcoming</span>
      </div>
    </div>
    <div class="stallion-modal__body">
      <div class="stallion-modal__body-inner">
        <p class="eyebrow stallion-modal__eyebrow">Vaulted Sire</p>
        <h2 class="stallion-modal__name" id="stallion-modal-name" data-modal-name></h2>
        <p class="stallion-modal__call" data-modal-call hidden></p>
        <p class="stallion-modal__tagline" data-modal-tagline></p>
        <div class="stallion-modal__rule" aria-hidden="true"></div>
        <p class="stallion-modal__pitch" data-modal-pitch></p>
        <dl class="stallion-modal__facts">
          <div class="stallion-modal__fact" data-modal-pedigree-wrap hidden>
            <dt>Pedigree</dt>
            <dd data-modal-pedigree></dd>
          </div>
          <div class="stallion-modal__fact" data-modal-foaled-wrap hidden>
            <dt>Registration</dt>
            <dd data-modal-foaled></dd>
          </div>
          <div class="stallion-modal__fact" data-modal-standing-wrap hidden>
            <dt>Standing</dt>
            <dd data-modal-standing></dd>
          </div>
        </dl>
        <div class="stallion-modal__actions">
          <button class="stallion-modal__share" type="button" data-modal-share aria-label="Share this profile">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line></svg>
            <span data-modal-share-label>Share profile</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</div>
''' + FOOTER


# ---------------------------------------------------------------- event
event = head(
    "The Event — October 6–8, 2027 · Oklahoma City (planned)",
    "Three days planned in Oklahoma City: eliminations, the Auction Crown, and finals night with the $105,000 "
    "Crown Purse. October 6–8, 2027. Venue pending.",
    "event.html") + f'''
<section class="pagehero">
  <div class="pagehero__media">
    <img src="assets/img/hero-d-arena.jpg" alt="A grand equestrian competition arena at night with warm amber stadium lights and deep burgundy velvet drapes" fetchpriority="high">
  </div>
  <div class="pagehero__scrim"></div>
  <div class="pagehero__inner">
    <div class="wrap">
      <p class="eyebrow">The Event</p>
      <h1 class="h-page">October 6&ndash;8, 2027&nbsp;&middot; Oklahoma City <span style="font-size:0.55em;letter-spacing:0.05em;text-transform:uppercase;opacity:0.7">Venue pending</span></h1>
      <p class="pagehero__sub">Three days. Seven classes. One million dollars in target purse.</p>
    </div>
  </div>
</section>

<section class="section on-ink" style="text-align:center">
  <div class="wrap">
    {countdown(large=True, caption="First go &middot; Wednesday 6 October 2027, 6:00 PM CDT")}
    <p style="margin-top:2.5rem">
      <button class="pill pill--ghost" type="button" data-placeholder="Coming Soon">Watch Live</button>
    </p>
  </div>
</section>

<section class="section on-dark">
  <div class="wrap">
    <p class="eyebrow">Schedule at a glance</p>
    <h2 class="h-section reveal">Three days.</h2>
    <div class="schedule reveal" style="margin-top:3rem">
      <div class="day">
        <p class="day__date">Wednesday &middot; Oct 6</p>
        <h3>1st Go</h3>
        <p>Eliminations for all seven classes. The finals field is set by the end of the night.</p>
        <ul>
          <li>Two-Year-Old Pleasure Driving</li>
          <li>Two-Year-Old Park Harness</li>
          <li>3&amp;4-Year-Old Pleasure Driving</li>
          <li>3&amp;4-Year-Old Park Harness</li>
          <li>3&amp;4-Year-Old Hunter</li>
          <li>3&amp;4-Year-Old Western</li>
          <li>3&amp;4-Year-Old Road Horse</li>
        </ul>
      </div>
      <div class="day">
        <p class="day__date">Thursday &middot; Oct 7</p>
        <h3>Dark Day &amp; Auction Crown Night</h3>
        <p>Schooling by day. Auction Crown by night &mdash; Stallion Tickets sold, Crown Purse set.</p>
        <ul>
          <li>Dark day &mdash; schooling only</li>
          <li>Auction Crown &mdash; evening</li>
          <li>Stallion Ticket sale</li>
        </ul>
      </div>
      <div class="day">
        <p class="day__date">Friday &middot; Oct 8</p>
        <h3>Finals &amp; Crown Purse</h3>
        <p>Finals in all seven classes. Crown Purse paid to the Stallion Ticket holders of Champion and Reserve.</p>
        <ul>
          <li>Finals &mdash; all seven classes</li>
          <li>Crown Purse presentation</li>
          <li>Champion &amp; Reserve awards</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section on-ink">
  <div class="wrap">
    <div class="panel reveal">
      <div class="split" style="align-items:center">
        <div>
          <p class="eyebrow">The Crown Purse</p>
          <p class="big-figure">$105,000</p>
          <p class="figure-caption" style="margin-top:1rem">Champion &amp; Reserve &times; 7 classes &mdash; 14 placings</p>
        </div>
        <div>
          <p class="lede">On top of the base money. Champion and Reserve in each of seven classes &mdash; fourteen placings, paid not to the horse's owner, but to the holder of its Stallion Ticket from the Auction Crown.</p>
          <p class="lede">The program's wager on pedigree. Back a sire. Share in what his get accomplish.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section on-cream">
  <div class="wrap">
    <div class="deflist deflist--2 reveal">
      <div class="def">
        <h3>Venue</h3>
        <p style="color:rgba(20,32,27,0.72)">Target market: Oklahoma City. Facility pending final contract. Prize list to follow with stabling, warm-up, and travel details.</p>
        <p class="figure-caption">Venue announcement to follow</p>
      </div>
      <div class="def" id="tickets">
        <h3>Tickets</h3>
        <p style="color:rgba(20,32,27,0.72)">Three-day passes, finals-night seating, and Auction Crown tables &mdash; released ahead of the event.</p>
        <p style="margin-top:1.5rem">
          <button class="pill" type="button" data-placeholder="Coming Soon">Tickets coming soon</button>
        </p>
      </div>
    </div>
  </div>
</section>
''' + FOOTER


FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="#E4BE6A">
  <rect width="64" height="64" fill="#3C5878"/>
  <text x="32" y="46" text-anchor="middle"
        font-family="Georgia, serif"
        font-size="36" font-weight="800"
        letter-spacing="-1.5">MM</text>
</svg>
'''

(ROOT / "index.html").write_text(index, encoding="utf-8")
(ROOT / "program.html").write_text(program, encoding="utf-8")
(ROOT / "classes.html").write_text(classes_page, encoding="utf-8")
(ROOT / "vault.html").write_text(vault_page, encoding="utf-8")
(ROOT / "crown.html").write_text(crown_page, encoding="utf-8")
(ROOT / "bridge.html").write_text(bridge_page, encoding="utf-8")
(ROOT / "nomination.html").write_text(nomination_page, encoding="utf-8")
(ROOT / "for-trainers.html").write_text(for_trainers_page, encoding="utf-8")
(ROOT / "governance.html").write_text(governance_page, encoding="utf-8")
(ROOT / "stallions.html").write_text(stallions, encoding="utf-8")
(ROOT / "event.html").write_text(event, encoding="utf-8")
(ROOT / "assets" / "img" / "favicon.svg").write_text(FAVICON, encoding="utf-8")
print("built 10 pages")
