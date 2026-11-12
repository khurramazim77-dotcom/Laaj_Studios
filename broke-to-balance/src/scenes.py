"""Script + scene renderers for 'Broke to Balance — How to Budget Your Paycheck (50/30/20)'."""
import math
from lib import *

TAKE_HOME, GROSS, TAXES = 3000, 3600, 600
_r = 0.07 / 12
FV60 = 600 * (((1 + _r) ** 60 - 1) / _r)          # ~ $42,957
CONTRIB60 = 600 * 60


def fv(m):
    return 600 * (((1 + _r) ** m - 1) / _r)


# ---- SCRIPT: scene id -> list of (seg_id, spoken text, on-screen caption text) -----------
SCRIPT = [
    ('hook', [
        ('h1', "Payday hits, and for about forty-eight hours, you feel rich.", "Payday hits, and for about 48 hours, you feel rich."),
        ('h2', "Then rent, subscriptions, and one little impulse order take everything.", None),
        ('h3', "And by the twentieth, you're broke again.", "And by the 20th, you're broke again."),
        ('h4', "If that sounds familiar, this video is for you.", None)]),
    ('title', [
        ('t1', "Welcome to Broke to Balance, where we turn paychecks into plans.", None),
        ('t2', "Today, you'll learn how to budget your paycheck using one simple rule, in under five minutes.", None)]),
    ('takehome', [
        ('a1', "Step one: budget your take-home pay, not your salary.", None),
        ('a2', "Take-home is the money that actually lands in your bank account, after taxes and deductions.", None),
        ('a3', "In this example, you earn thirty-six hundred dollars a month.", "In this example, you earn $3,600 a month."),
        ('a4', "After six hundred dollars in taxes and deductions,", "After $600 in taxes and deductions,"),
        ('a5', "three thousand dollars is yours to plan.", "$3,000 is yours to plan.")]),
    ('rule', [
        ('r1', "Now meet the fifty, thirty, twenty rule, popularized by Elizabeth Warren and Amelia Warren Tee-ah-gee in the book, All Your Worth.",
         "Meet the 50/30/20 rule, popularized by Elizabeth Warren and Amelia Warren Tyagi in the book All Your Worth."),
        ('r2', "Fifty percent of your take-home goes to needs.", "50% of your take-home goes to needs."),
        ('r3', "Thirty percent goes to wants.", "30% goes to wants."),
        ('r4', "And twenty percent goes to savings and debt payoff.", "And 20% goes to savings and debt payoff."),
        ('r5', "On three thousand dollars, that's fifteen hundred, nine hundred, and six hundred.", "On $3,000, that's $1,500, $900, and $600.")]),
    ('needs', [
        ('n1', "Needs are the bills you can't skip: rent, groceries, utilities, transportation, and insurance.", None),
        ('n2', "Add them up in a spreadsheet, like this.", None),
        ('n3', "In our example, needs total fifteen hundred dollars, exactly fifty percent.", "In our example, needs total $1,500, exactly 50%."),
        ('n4', "If yours come in higher, don't panic. That's not failure, it's information, and it shows you where to trim.", None)]),
    ('wants', [
        ('w1', "Wants are what make life fun: eating out, streaming, shopping, and trips.", None),
        ('w2', "Nine hundred dollars is a real amount of fun, but only if you decide where it goes before the month starts.",
         "$900 is a real amount of fun, but only if you decide where it goes before the month starts."),
        ('w3', "Here's the trick: give every want a name and a limit.", None)]),
    ('savings', [
        ('s1', "The last twenty percent is what builds your balance.", "The last 20% is what builds your balance."),
        ('s2a', "First, a starter emergency fund.", None),
        ('s2b', "Then, pay down high-interest debt.", None),
        ('s2c', "Then, invest for your future.", None),
        ('s3', "Saving six hundred dollars a month adds up to seventy-two hundred dollars in one year.", "Saving $600 a month adds up to $7,200 in one year."),
        ('s4', "And if you invested it for five years at a seven percent average return, which is an assumption, not a guarantee, it could grow to about forty-three thousand dollars.",
         "Invested for 5 years at an assumed 7% average return (not a guarantee), it could grow to about $43,000."),
        ('s5', "That's the power of consistency.", None)]),
    ('tips', [
        ('p1', "Three tips to make this stick.", None),
        ('p2', "One: pay yourself first. Automate a transfer on payday, so your savings leave before you can spend them.", None),
        ('p3', "Two: track it in a simple spreadsheet. Ten minutes a week is all it takes.", "Two: track it in a simple spreadsheet. 10 minutes a week is all it takes."),
        ('p4', "Three: adjust the rule to fit your life. If rent is high where you live, try sixty, twenty, twenty. Progress beats perfection.",
         "Three: adjust the rule to fit your life. If rent is high where you live, try 60/20/20. Progress beats perfection.")]),
    ('mistakes', [
        ('m1', "Before we wrap up, three mistakes that quietly break budgets.", None),
        ('m2', "Mistake one: budgeting your gross salary instead of your take-home pay. That makes every number look bigger than it really is.", None),
        ('m3', "Mistake two: forgetting irregular costs, like car repairs, gifts, and annual fees. Set aside a little each month, so they don't surprise you.", None),
        ('m4', "Mistake three: making your budget so strict that you quit. Leave room for fun, because a budget you can stick with beats a perfect one you can't.", None)]),
    ('outro', [
        ('c1', "So, here's the recap.", None),
        ('c2', "Fifty percent for needs.", "50% for needs."),
        ('c3', "Thirty percent for wants.", "30% for wants."),
        ('c4', "Twenty percent for future you.", "20% for future you."),
        ('c5', "If this helped, subscribe to Broke to Balance, and tell me in the comments: which bucket is hardest for you?", None),
        ('c6', "This video is for education only, and isn't financial advice. See you next time.", None)]),
]


# ---- helpers -----------------------------------------------------------------
def header(img, t, t0, step, title, col=GREEN):
    p = e_out(prog(t, t0, 0.5))
    if p <= 0:
        return
    pill(img, 960 - 0, 168 - 20 * (1 - p), step, 24, col, NAVY if col in (GOLD, GREEN) else WHITE, padx=24, h=44, alpha=p)
    text(img, (960, 232 - 20 * (1 - p)), title, 58, 'ExtraBold', WHITE, 'mm', p)


def A(S):
    return lambda k: S[k][0]


def D(S):
    return lambda k: S[k][1]


# ======================= 1. HOOK ==========================================
def s_hook(img, t, S):
    a, d = A(S), D(S)
    bg_city(img, t)
    fade_overlay(img, (8, 14, 36), 0.28)
    pin = e_back(prog(t, a('h1') - 0.35, 0.9))
    dy = lerp(-520, 0, pin)
    cx, cy = 960, 440
    box = (cx - 420, cy - 190 + dy, cx + 420, cy + 190 + dy)

    chips = [('Rent', 1000), ('Groceries', 450), ('Subscriptions', 85), ('Delivery', 210), ('Impulse order', 160), ('Gas', 140), ('Everything else', 955)]
    t0 = a('h2')
    t1 = a('h3') + d('h3') * 0.85
    span = t1 - t0
    spent = 0.0
    sched = []
    for i, (n, am) in enumerate(chips):
        ts = t0 + span * i / len(chips)
        spent += am * e_out(prog(t, ts, 0.55))
        sched.append((n, am, ts))
    bal = max(0, TAKE_HOME - spent)
    day = 1 + int(19 * prog(t, t0, t1 - t0))

    card(img, box, 34, WHITE)
    cv = Cv((box[0], box[1], box[2], box[1] + 92))
    cv.rrect((box[0], box[1], box[2], box[1] + 90), 34, fill=rgba(GREEN))
    cv.rrect((box[0], box[1] + 50, box[2], box[1] + 90), 0, fill=rgba(GREEN))
    cv.paste(img)
    text(img, (box[0] + 40, box[1] + 45), 'PAYDAY', 36, 'ExtraBold', NAVY, 'lm')
    text(img, (box[2] - 40, box[1] + 45), f'DAY {day}', 34, 'ExtraBold', NAVY, 'rm')
    text(img, (cx, box[1] + 135), 'YOUR BALANCE', 26, 'Bold', GREY, 'mm')
    fr = clamp(bal / TAKE_HOME)
    col = lerpc(CORAL, (214, 150, 0), fr / 0.5) if fr < 0.5 else lerpc((214, 150, 0), GREEN_D, (fr - 0.5) / 0.5)
    text(img, (cx, box[1] + 245), money(bal, True), 128, 'Black', col, 'mm')
    bw = 640
    cvb = Cv((cx - bw // 2 - 3, box[1] + 312, cx + bw // 2 + 3, box[1] + 342))
    cvb.rrect((cx - bw // 2, box[1] + 318, cx + bw // 2, box[1] + 334), 8, fill=rgba(LIGHT))
    if bal > 1:
        cvb.rrect((cx - bw // 2, box[1] + 318, cx - bw // 2 + bw * bal / TAKE_HOME, box[1] + 334), 8, fill=rgba(col))
    cvb.paste(img)

    for i, (n, am, ts) in enumerate(sched):
        p = prog(t, ts, 1.4)
        if p <= 0 or p >= 1:
            continue
        side = -1 if i % 2 == 0 else 1
        x = cx + side * (260 + 520 * e_out(p))
        y = cy + dy - 40 - 220 * math.sin(p * math.pi * 0.9) + 260 * p ** 2
        al = 1 - clamp((p - 0.55) / 0.45)
        pill(img, x, y, f'−{money(am)}  {n}', 30, CORAL, WHITE, padx=24, h=56, alpha=al)

    q = e_out(prog(t, a('h4') + 0.1, 0.6))
    text(img, (cx, 870), 'Sound familiar?', 92, 'Black', WHITE, 'mm', q)


# ======================= 2. TITLE =========================================
def s_title(img, t, S):
    a, d = A(S), D(S)
    bg_soft(img, t, NAVY, NAVY2, GREEN, 1)
    money_rain(img, t + 5, 22, 11, 0.85)
    fade_overlay(img, NAVY, 0.25)
    p = e_back(prog(t, a('t1') - 0.2, 0.9))
    cy = 440 + 80 * (1 - p)
    w1, w2 = text_w('Broke', 170, 'Black'), text_w('Balance', 170, 'Black')
    arrow = 170
    total = w1 + arrow + w2
    x0 = 960 - total / 2
    al = clamp(p)
    text(img, (x0, cy), 'Broke', 170, 'Black', CORAL, 'lm', al)
    ap = e_out(prog(t, a('t1') + 0.5, 0.6))
    ax = x0 + w1 + 20
    cvv = Cv((ax - 4, cy - 50, ax + arrow, cy + 50))
    cvv.line([(ax + 10, cy), (ax + 10 + (arrow - 76) * ap, cy)], rgba(WHITE), 12)
    if ap > .6:
        cvv.poly([(ax + arrow - 92, cy - 34), (ax + arrow - 50, cy), (ax + arrow - 92, cy + 34)], fill=rgba(WHITE))
    cvv.paste(img)
    text(img, (x0 + w1 + arrow, cy), 'Balance', 170, 'Black', GREEN, 'lm', al)
    lp = e_out(prog(t, a('t1') + 0.4, 0.9))
    cv = Cv((960 - 600, cy + 110, 960 + 600, cy + 134))
    cv.rrect((960 - 560 * lp, cy + 116, 960 + 560 * lp, cy + 126), 5, fill=rgba(GOLD))
    cv.paste(img)
    sp = e_out(prog(t, a('t2') - 0.2, 0.7))
    pill(img, 960, cy + 230 - 16 * (1 - sp), 'How to Budget Your Paycheck', 46, WHITE, NAVY, padx=44, h=86, alpha=sp)
    text(img, (960, cy + 340 - 16 * (1 - sp)), 'THE 50 / 30 / 20 RULE  •  EPISODE 1', 30, 'Bold', LIGHT, 'mm', sp)


# ======================= 3. TAKE-HOME =====================================
def s_takehome(img, t, S):
    a, d = A(S), D(S)
    bg_soft(img, t, NAVY, NAVY2, BLUE, 2)
    header(img, t, a('a1'), 'STEP 1', 'Start with your TAKE-HOME pay')

    # bank notification (a1..a2)
    n_in = e_back(prog(t, a('a1') + 0.4, 0.8))
    n_out = 1 - e_inout(prog(t, a('a3') - 0.35, 0.5))
    if n_in > 0 and n_out > 0:
        al = clamp(n_in) * n_out
        y = 560 - 40 * (1 - clamp(n_in)) - 40 * (1 - n_out)
        box = (410, y - 170, 1510, y + 170)
        shadow(img, box, 36, 28, int(120 * al))
        cv = Cv((box[0] - 3, box[1] - 3, box[2] + 3, box[3] + 3))
        cv.rrect(box, 36, fill=rgba(WHITE))
        cv.ellipse((box[0] + 44, y - 56, box[0] + 156, y + 56), fill=rgba(GREEN))
        cv.line([(box[0] + 76, y), (box[0] + 96, y + 20), (box[0] + 130, y - 20)], rgba(WHITE), 10)
        cv.paste(img, al)
        text(img, (box[0] + 200, y - 62), 'DEPOSIT RECEIVED', 26, 'Bold', GREY, 'lm', al)
        text(img, (box[0] + 200, y), '+ $3,000.00', 96, 'Black', GREEN_D, 'lm', al)
        text(img, (box[0] + 200, y + 66), 'Direct deposit  •  Checking •••• 4821  •  your real money', 26, 'Medium', GREY, 'lm', al)

    # waterfall (a3..a5)
    base_y, scale = 840, 440 / GROSS
    bars = [
        (480, 0, GROSS, WHITE, a('a3'), money(GROSS), 'Gross pay', 'before taxes'),
        (840, TAKE_HOME, GROSS, CORAL, a('a4'), '−' + money(TAXES), 'Taxes & deductions', 'what comes out'),
        (1200, 0, TAKE_HOME, GREEN, a('a5'), money(TAKE_HOME), 'Take-home pay', 'what lands in your account'),
    ]
    cp = e_out(prog(t, a('a3') - 0.1, 0.5))
    if cp > 0:
        for i, (x, lo, hi, col, ts, lab, l1, l2) in enumerate(bars):
            p = e_out(prog(t, ts, 0.8))
            if p <= 0:
                continue
            yb = base_y - lo * scale
            yt = base_y - (lo + (hi - lo) * p) * scale
            cv = Cv((x - 4, yt - 4, x + 244, yb + 4))
            cv.rrect((x, yt, x + 240, yb), 18, fill=rgba(col))
            cv.paste(img)
            text(img, (x + 120, yt - 44), lab, 54, 'Black', col, 'mm', clamp(p * 2))
            text(img, (x + 120, base_y + 46), l1, 30, 'Bold', WHITE, 'mm', clamp(p * 2))
            text(img, (x + 120, base_y + 84), l2, 24, 'Medium', GREY, 'mm', clamp(p * 2))
            if i < 2:
                nx = bars[i + 1][0]
                pc = clamp(p * 2)
                ImageDraw.Draw(img, 'RGBA').line([(x + 240, yt), (nx, yt)], fill=rgba(GREY, 120 * pc), width=2)
        ImageDraw.Draw(img, 'RGBA').line([(380, base_y), (1540, base_y)], fill=rgba(GREY, 160), width=3)
    text(img, (960, 962), 'Example numbers for illustration only', 24, 'Medium', GREY, 'mm', 0.8)


# ======================= 4. THE RULE ======================================
SPLIT = [('NEEDS', .50, NEEDS, 'house', 1500), ('WANTS', .30, WANTS, 'star', 900), ('SAVINGS & DEBT', .20, SAVE, 'piggy', 600)]


def s_rule(img, t, S):
    a, d = A(S), D(S)
    bg_soft(img, t, NAVY, NAVY2, GREEN, 3)
    header(img, t, a('r1'), 'THE RULE', 'The 50 / 30 / 20 rule', GOLD)
    cx, cy, R, r = 600, 640, 270, 168
    starts = [('r2', 0), ('r3', 180), ('r4', 288)]
    cv = Cv((cx - R - 10, cy - R - 10, cx + R + 10, cy + R + 10), s=3)
    cv.ellipse((cx - R, cy - R, cx + R, cy + R), fill=rgba(WHITE, 28))
    for i, (sid, a0) in enumerate(starts):
        name, frac, col, ic, amt = SPLIT[i]
        p = e_inout(prog(t, a(sid) + 0.05, min(1.3, d(sid) * 0.9)))
        if p > 0.003:
            a1 = a0 - 90 + 360 * frac * p
            cv.pie((cx - R, cy - R, cx + R, cy + R), a0 - 90 + 0.8, max(a0 - 90 + 1.0, a1 - 0.8), rgba(col))
    cv.d.ellipse(cv.B((cx - r, cy - r, cx + r, cy + r)), fill=(0, 0, 0, 0))
    cv.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgba(NAVY, 255))
    cv.paste(img)
    text(img, (cx, cy - 34), 'TAKE-HOME', 26, 'Bold', GREY, 'mm')
    text(img, (cx, cy + 18), '$3,000', 66, 'Black', WHITE, 'mm')
    text(img, (cx, cy + 82), 'per month', 26, 'Medium', GREY, 'mm')

    # book card (r1)
    bp = e_back(prog(t, a('r1') + 0.3, 0.8))
    bo = 1 - e_inout(prog(t, a('r2') - 0.1, 0.5))
    if bp > 0 and bo > 0.01:
        al = clamp(bp) * bo
        bx, by = 1180, 640 + 60 * (1 - clamp(bp)) + 30 * (1 - bo)
        box = (bx - 210, by - 290, bx + 210, by + 290)
        shadow(img, box, 20, 26, int(130 * al))
        cvb = Cv((box[0] - 3, box[1] - 3, box[2] + 3, box[3] + 3))
        cvb.rrect(box, 20, fill=rgba((232, 226, 210)))
        cvb.rrect((box[0], box[1], box[0] + 26, box[3]), 10, fill=rgba((150, 38, 54)))
        cvb.rrect((box[0] + 26, box[1] + 40, box[2] - 26, box[1] + 220), 8, fill=rgba((150, 38, 54)))
        cvb.paste(img, al)
        text(img, (bx + 12, by - 150), 'ALL YOUR', 56, 'Black', (240, 226, 200), 'mm', al)
        text(img, (bx + 12, by - 88), 'WORTH', 56, 'Black', (240, 226, 200), 'mm', al)
        text(img, (bx + 12, by + 20), 'Elizabeth Warren', 29, 'Bold', (60, 50, 40), 'mm', al)
        text(img, (bx + 12, by + 56), '& Amelia Warren Tyagi', 27, 'Medium', (60, 50, 40), 'mm', al)
        text(img, (bx + 12, by + 150), 'The 50/30/20 budget', 26, 'SemiBold', (150, 38, 54), 'mm', al)

    # legend rows
    for i, (name, frac, col, ic, amt) in enumerate(SPLIT):
        sid = ['r2', 'r3', 'r4'][i]
        p = e_out(prog(t, a(sid) + 0.15, 0.6))
        if p <= 0:
            continue
        y = 440 + i * 190
        x = 1060 + 60 * (1 - p)
        box = (x, y - 78, x + 760, y + 78)
        card(img, box, 30, (255, 255, 255), int(26 * p), shad=False, outline=rgba(col, int(200 * p)))
        icon(img, ic, x + 78, y, 40, NAVY, col, p)
        text(img, (x + 148, y - 30), name, 30, 'Bold', LIGHT, 'lm', p)
        text(img, (x + 148, y + 26), f'{int(frac * 100)}%', 62, 'Black', col, 'lm', p)
        dp = e_out(prog(t, a('r5') + 0.25 * i, 0.9))
        if dp > 0:
            text(img, (x + 730, y), money(amt * dp), 66, 'Black', WHITE, 'rm', dp)


# ======================= 5. NEEDS (spreadsheet) ==========================
ROWS = [('Rent', 1000), ('Groceries', 250), ('Utilities', 100), ('Transportation', 100), ('Insurance & minimums', 50)]


def sheet_frame(img, box, title, formula_ref, formula_txt, col_labels=('A', 'B', 'C')):
    x0, y0, x1, y1 = box
    shadow(img, box, 22, 30, 130)
    cv = Cv((x0 - 3, y0 - 3, x1 + 3, y1 + 3))
    cv.rrect(box, 22, fill=rgba((252, 253, 255)))
    cv.rrect((x0, y0, x1, y0 + 58), 22, fill=rgba((232, 238, 246)))
    cv.rrect((x0, y0 + 30, x1, y0 + 58), 0, fill=rgba((232, 238, 246)))
    for i, c in enumerate(((255, 95, 87), (254, 188, 46), (40, 200, 64))):
        cv.ellipse((x0 + 24 + i * 30, y0 + 20, x0 + 40 + i * 30, y0 + 36), fill=rgba(c))
    cv.paste(img)
    text(img, ((x0 + x1) / 2, y0 + 29), title, 24, 'SemiBold', (80, 92, 112), 'mm')
    d = ImageDraw.Draw(img)
    fy = y0 + 58
    d.rectangle([x0, fy, x1, fy + 52], fill=(245, 247, 251))
    d.rectangle([x0 + 12, fy + 8, x0 + 112, fy + 44], fill=WHITE, outline=(200, 208, 220))
    text(img, (x0 + 62, fy + 26), formula_ref, 24, 'SemiBold', (60, 70, 90), 'mm')
    text(img, (x0 + 140, fy + 26), 'fx', 24, 'Bold', (120, 130, 150), 'mm')
    text(img, (x0 + 175, fy + 26), formula_txt, 26, 'Medium', (30, 40, 60), 'lm')
    d.line([(x0, fy + 52), (x1, fy + 52)], fill=(210, 216, 228), width=1)


def s_needs(img, t, S):
    a, d = A(S), D(S)
    bg_soft(img, t, NAVY, NAVY2, BLUE, 4)
    header(img, t, a('n1'), 'BUCKET 1 • 50%', 'NEEDS: the bills you can’t skip', NEEDS)
    box = (130, 300, 1170, 960)
    x0, y0, x1, y1 = box
    sp = e_out(prog(t, a('n1') - 0.1, 0.7))
    if sp < 0.01:
        return
    # formula text typing
    typed = int(len('=SUM(B2:B6)') * prog(t, a('n2') + 0.3, 1.2))
    sel_total = t > a('n3') - 0.2
    ftxt = '=SUM(B2:B6)'[:typed] if typed > 0 else ''
    ref = 'B7' if typed > 0 else 'A1'
    if t < a('n2'):
        ftxt, ref = 'Need', 'A1'
    sheet_frame(img, box, 'Monthly Budget — Needs.xlsx', ref, ftxt)
    dd = ImageDraw.Draw(img)
    gy = y0 + 58 + 52
    cols = [64, 520, 240, 216]
    cx = [x0, x0 + 64, x0 + 584, x0 + 824, x1]
    # column header
    dd.rectangle([x0, gy, x1, gy + 36], fill=(236, 240, 247))
    for i, lab in enumerate(('A', 'B', 'C')):
        text(img, ((cx[i + 1] + cx[i + 2]) / 2, gy + 18), lab, 20, 'SemiBold', (110, 122, 145), 'mm')
    rh = 56
    ry = gy + 36
    for rr in range(9):
        yy = ry + rr * rh
        dd.line([(x0, yy + rh), (x1, yy + rh)], fill=(226, 231, 240), width=1)
        dd.rectangle([x0, yy, x0 + 64, yy + rh], fill=(240, 243, 249))
        text(img, (x0 + 32, yy + rh / 2), str(rr + 1), 20, 'Medium', (120, 130, 150), 'mm')
    for i in range(1, 4):
        dd.line([(cx[i], ry), (cx[i], ry + 9 * rh)], fill=(226, 231, 240), width=1)
    # header row
    hp = e_out(prog(t, a('n1') + 0.1, 0.5))
    dd.rectangle([cx[1] + 1, ry + 1, x1 - 1, ry + rh - 1], fill=(226, 236, 252))
    for i, lab in enumerate(('Need', 'Monthly cost', '% of take-home')):
        xx = cx[i + 1] + (16 if i == 0 else cols[i + 1] - 16)
        text(img, (xx, ry + rh / 2), lab, 26, 'Bold', (30, 60, 130), 'lm' if i == 0 else 'rm', hp)
    n = len(ROWS)
    span = max(0.5, d('n1') - 1.4)
    for i, (nm, am) in enumerate(ROWS):
        ts = a('n1') + 0.9 + span * i / n
        p = e_out(prog(t, ts, 0.45))
        yy = ry + (i + 1) * rh
        if p <= 0:
            continue
        text(img, (cx[1] + 16, yy + rh / 2), nm, 27, 'Medium', (30, 40, 60), 'lm', p)
        text(img, (cx[2] + cols[2] - 16, yy + rh / 2), f'{am:,}', 27, 'Medium', (30, 40, 60), 'rm', p)
        text(img, (x1 - 16, yy + rh / 2), f'{am / TAKE_HOME * 100:.1f}%', 27, 'Medium', (110, 122, 145), 'rm', p)
    # selection on B2:B6
    selp = prog(t, a('n2') + 0.2, 0.5) * (1 - prog(t, a('n3') - 0.2, 0.3))
    if selp > 0:
        sx0, sx1 = cx[2], cx[3]
        sy0, sy1 = ry + rh, ry + 6 * rh
        ov = Cv((sx0 - 4, sy0 - 4, sx1 + 4, sy1 + 4), s=1)
        ov.rrect((sx0, sy0, sx1, sy1), 4, fill=rgba(BLUE, 40 * selp), outline=rgba(BLUE, 255 * selp), width=3)
        ov.paste(img)
    # total row
    tp = e_back(prog(t, a('n3') + 0.2, 0.7))
    yy = ry + 6 * rh
    if tp > 0:
        al = clamp(tp)
        dd = ImageDraw.Draw(img, 'RGBA')
        dd.rectangle([cx[1] + 1, yy + 1, x1 - 1, yy + rh - 1], fill=rgba(GREEN, 55 * al))
        dd.rectangle([cx[2] + 1, yy + 1, cx[3] - 1, yy + rh - 1], outline=rgba(GREEN_D, 255 * al), width=3)
        text(img, (cx[1] + 16, yy + rh / 2), 'TOTAL NEEDS', 27, 'ExtraBold', (10, 90, 60), 'lm', al)
        cnt = 1500 * e_out(prog(t, a('n3') + 0.3, 1.1))
        text(img, (cx[2] + cols[2] - 16, yy + rh / 2), f'{cnt:,.0f}', 28, 'ExtraBold', (10, 90, 60), 'rm', al)
        text(img, (x1 - 16, yy + rh / 2), '50.0%', 28, 'ExtraBold', (10, 90, 60), 'rm', al)

    # right panel: gauge, then "if higher"
    gx, gy2, gr = 1530, 520, 170
    gp = e_out(prog(t, a('n3') + 0.2, 1.4))
    mp = 1 - e_inout(prog(t, a('n4') - 0.1, 0.5))
    if gp > 0:
        cvg = Cv((gx - gr - 20, gy2 - gr - 20, gx + gr + 20, gy2 + gr + 20), s=3)
        cvg.arc((gx - gr, gy2 - gr, gx + gr, gy2 + gr), 0, 360, rgba(WHITE, 40), 34)
        cvg.arc((gx - gr, gy2 - gr, gx + gr, gy2 + gr), -90, -90 + 180 * gp, rgba(NEEDS), 34)
        cvg.paste(img, 1.0)
        text(img, (gx, gy2 - 12), f'{50 * gp:.0f}%', 100, 'Black', WHITE, 'mm')
        text(img, (gx, gy2 + 62), 'of take-home', 28, 'Medium', GREY, 'mm')
        pill(img, gx, gy2 + gr + 60, 'ON TARGET', 28, GREEN, NAVY, padx=28, h=54, alpha=clamp(gp))
    ip = e_out(prog(t, a('n4') + 0.2, 0.6))
    if ip > 0:
        for i, (lab, ic) in enumerate((('Trim a bill', 'cart'), ('Negotiate a rate', 'bolt'), ('Boost income', 'star'))):
            q = e_out(prog(t, a('n4') + 0.9 + i * 0.7, 0.5))
            y = 830 + i * 0  # placed in a row below gauge
            bx = 1290 + i * 0
            yy2 = 800 + i * 74
            if q > 0:
                pill(img, 1530, yy2, lab, 28, (255, 255, 255), NAVY, padx=34, h=56, alpha=q)
                icon(img, ic, 1530 - text_w(lab, 28) / 2 - 62, yy2, 22, NAVY, GOLD, q)
        text(img, (1530, 752), 'Over 50%? Try one of these:', 28, 'Bold', GOLD, 'mm', ip)


# ======================= 6. WANTS =========================================
WANTS_ROWS = [('Dining out', 250, 'fork'), ('Shopping', 200, 'bag'), ('Entertainment', 150, 'play'), ('Travel fund', 140, 'plane'), ('Other fun', 100, 'star'), ('Subscriptions', 60, 'dots')]


def s_wants(img, t, S):
    a, d = A(S), D(S)
    bg_soft(img, t, NAVY, (40, 36, 78), GOLD, 5)
    header(img, t, a('w1'), 'BUCKET 2 • 30%', 'WANTS: the fun stuff', GOLD)
    x0 = 170
    for i, (nm, am, ic) in enumerate(WANTS_ROWS):
        ts = a('w1') + 0.7 + (d('w1') - 1.4) * i / len(WANTS_ROWS)
        p = e_out(prog(t, ts, 0.7))
        if p <= 0:
            continue
        y = 360 + i * 108
        icon(img, ic, x0 + 40, y, 36, NAVY, GOLD, p)
        text(img, (x0 + 100, y), nm, 34, 'SemiBold', WHITE, 'lm', p)
        bx0, maxw = 520, 560
        w = am / 250 * maxw * p
        cv = Cv((bx0 - 3, y - 30, bx0 + maxw + 160, y + 30))
        cv.rrect((bx0, y - 22, bx0 + maxw, y + 22), 22, fill=rgba(WHITE, 28))
        cv.rrect((bx0, y - 22, bx0 + max(w, 44), y + 22), 22, fill=rgba(GOLD))
        cv.paste(img)
        text(img, (bx0 + maxw + 28, y), money(am * p), 34, 'Black', GOLD, 'lm', p)
    # total card
    tp = e_back(prog(t, a('w2') - 0.2, 0.8))
    if tp > 0:
        al = clamp(tp)
        box = (1260, 340, 1790, 700)
        yoff = 40 * (1 - al)
        card(img, (box[0], box[1] + yoff, box[2], box[3] + yoff), 36, (255, 255, 255), int(255 * al))
        text(img, (1525, 410 + yoff), 'WANTS BUDGET', 28, 'Bold', GREY, 'mm', al)
        cnt = 900 * e_out(prog(t, a('w2') + 0.1, 1.4))
        text(img, (1525, 520 + yoff), money(cnt), 120, 'Black', (200, 140, 0), 'mm', al)
        text(img, (1525, 610 + yoff), '30% of $3,000', 32, 'SemiBold', (80, 92, 112), 'mm', al)
    for i, (lab, ic) in enumerate((('Name it', 'check'), ('Cap it', 'check'))):
        q = e_back(prog(t, a('w3') + 0.4 + i * 0.9, 0.7))
        if q > 0:
            al = clamp(q)
            pill(img, 1525, 790 + i * 100 + 30 * (1 - al), lab, 48, GOLD, NAVY, padx=60, h=80, alpha=al)
            icon(img, 'check', 1525 - text_w(lab, 48) / 2 - 90, 790 + i * 100 + 30 * (1 - al), 24, NAVY, None, al)


# ======================= 7. SAVINGS =======================================
def s_savings(img, t, S):
    a, d = A(S), D(S)
    bg_soft(img, t, NAVY, (8, 52, 58), GREEN, 6)
    header(img, t, a('s1'), 'BUCKET 3 • 20%', 'SAVINGS & DEBT: build your balance', GREEN)

    lad = 1 - e_inout(prog(t, a('s3') - 0.2, 0.6))
    if lad > 0.01:
        steps = [('1', 'Starter emergency fund', 'Cover small surprises', 'shield', 's2a'),
                 ('2', 'Pay down high-interest debt', 'Stop the interest drain', 'bolt', 's2b'),
                 ('3', 'Invest for your future', 'Let time do the work', 'star', 's2c')]
        for i, (num, ttl, sub, ic, sid) in enumerate(steps):
            p = e_back(prog(t, a(sid) - 0.05, 0.8))
            if p <= 0:
                continue
            al = clamp(p) * lad
            x = 190 + i * 520
            top = 730 - i * 120 + 60 * (1 - clamp(p))
            box = (x, top, x + 480, 960)
            card(img, box, 30, (255, 255, 255), int(40 * al), shad=False, outline=rgba(GREEN, 220 * al))
            cvn = Cv((x + 20, top + 20, x + 100, top + 100))
            cvn.ellipse((x + 24, top + 24, x + 96, top + 96), fill=rgba(GREEN))
            cvn.paste(img, al)
            text(img, (x + 60, top + 60), num, 44, 'Black', NAVY, 'mm', al)
            icon(img, ic, x + 420, top + 62, 34, NAVY, GREEN, al)
            text(img, (x + 30, top + 140), ttl, 29, 'Bold', WHITE, 'lm', al)
            text(img, (x + 30, top + 184), sub, 25, 'Medium', GREY, 'lm', al)
        # headline number
        hp = e_out(prog(t, a('s1') + 0.3, 0.7)) * lad
        text(img, (960, 330), '20% of $3,000  =  $600 a month', 54, 'ExtraBold', GREEN, 'mm', hp)

    # chart
    cp = e_out(prog(t, a('s3') + 0.1, 0.7))
    if cp > 0.01:
        px0, px1, py0, py1 = 330, 1440, 400, 850
        ymax = 45000
        X = lambda m: px0 + (px1 - px0) * m / 60
        Y = lambda v: py1 - (py1 - py0) * v / ymax
        dd = ImageDraw.Draw(img, 'RGBA')
        for v in range(0, 45001, 10000):
            dd.line([(px0, Y(v)), (px1, Y(v))], fill=rgba(WHITE, 36 * cp), width=1)
            text(img, (px0 - 20, Y(v)), money(v), 24, 'Medium', GREY, 'rm', cp)
        for m in range(0, 61, 12):
            text(img, (X(m), py1 + 34), 'Start' if m == 0 else f'Year {m // 12}', 24, 'Medium', GREY, 'mm', cp)
        text(img, (px0, py0 - 56), 'Saving $600 a month', 32, 'Bold', LIGHT, 'lm', cp)

        pc1 = prog(t, a('s3') + 0.4, 1.8)            # contributions to month 12
        pc2 = prog(t, a('s4') + 0.3, max(2.0, d('s4') * .8))     # extend to 60 + growth
        m_c = 12 * pc1 + 48 * e_inout(pc2)
        pts_c = [(X(m), Y(600 * m)) for m in [i * 0.5 for i in range(int(m_c * 2) + 1)]]
        pts_c.append((X(m_c), Y(600 * m_c)))
        cv = Cv((px0 - 10, py0 - 40, px1 + 330, py1 + 20), s=2)
        if len(pts_c) > 1:
            cv.line(pts_c, rgba((120, 170, 255)), 7)
        if pc2 > 0:
            m_g = 60 * e_inout(pc2)
            pts_g = [(X(m), Y(fv(m))) for m in [i * 0.5 for i in range(int(m_g * 2) + 1)]]
            pts_g.append((X(m_g), Y(fv(m_g))))
            cv.line(pts_g, rgba(GREEN), 9)
            cv.ellipse((X(m_g) - 13, Y(fv(m_g)) - 13, X(m_g) + 13, Y(fv(m_g)) + 13), fill=rgba(WHITE), outline=rgba(GREEN), width=5)
        cv.ellipse((X(m_c) - 11, Y(600 * m_c) - 11, X(m_c) + 11, Y(600 * m_c) + 11), fill=rgba(WHITE), outline=rgba((120, 170, 255)), width=5)
        cv.paste(img, cp)
        # year-1 callout
        c1 = e_back(prog(t, a('s3') + 1.8, 0.7))
        c1o = 1 - prog(t, a('s4') + 1.2, 0.6)
        if c1 > 0 and c1o > 0:
            al = clamp(c1) * c1o
            pill(img, X(12) + 60, Y(7200) - 70, '$7,200 after 1 year', 32, (120, 170, 255), NAVY, padx=28, h=62, alpha=al)
        # end labels
        e1 = e_back(prog(t, a('s4') + max(2.0, d('s4') * .8) * 0.85, 0.7))
        if e1 > 0:
            al = clamp(e1)
            text(img, (X(60) + 30, Y(CONTRIB60) + 8), f'{money(CONTRIB60)}', 40, 'Black', (140, 185, 255), 'lm', al)
            text(img, (X(60) + 30, Y(CONTRIB60) + 48), 'what you put in', 24, 'Medium', GREY, 'lm', al)
            text(img, (X(60) + 30, Y(FV60) - 34), f'≈ {money(round(FV60, -2))}', 54, 'Black', GREEN, 'lm', al)
            text(img, (X(60) + 30, Y(FV60) + 8), 'with 7% assumed return', 24, 'Medium', GREY, 'lm', al)
        fp = e_out(prog(t, a('s4') + 1.0, 0.6))
        text(img, (960, 950), 'Hypothetical example: assumes a constant 7% annual return, compounded monthly. Not a guarantee. Investing involves risk.', 22, 'Medium', GREY, 'mm', fp)


# ======================= 8. TIPS ==========================================
def _flow(img, pts, t, t0, col, n=4, speed=0.55):
    """Animated dots travelling along polyline pts."""
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    tot = sum(seg)
    cv = Cv((0, 0, W, H), s=1)
    for k in range(n):
        u = ((t - t0) * speed + k / n) % 1.0
        if t < t0:
            continue
        dist = u * tot
        for i, sl in enumerate(seg):
            if dist <= sl:
                f = dist / sl
                x = lerp(pts[i][0], pts[i + 1][0], f); y = lerp(pts[i][1], pts[i + 1][1], f)
                cv.ellipse((x - 11, y - 11, x + 11, y + 11), fill=rgba(col))
                break
            dist -= sl
    cv.paste(img)


def s_tips(img, t, S):
    a, d = A(S), D(S)
    bg_soft(img, t, NAVY, NAVY2, CORAL, 7)
    ends = {'p1': a('p2') - 0.25, 'p2': a('p3') - 0.25, 'p3': a('p4') - 0.25, 'p4': 1e9}
    for sid in ('p1', 'p2', 'p3', 'p4'):
        pin = e_out(prog(t, a(sid) - 0.05, 0.5))
        pout = 1 - e_inout(prog(t, ends[sid], 0.4))
        al = pin * pout
        if al <= 0.01:
            continue
        ox = 30 * (1 - pin)
        if sid == 'p1':
            text(img, (960, 300), '3 tips to make it stick', 92, 'Black', WHITE, 'mm', al)
            for i, (lab, col) in enumerate((('Pay yourself first', GREEN), ('Track it weekly', BLUE), ('Adjust to your life', GOLD))):
                q = e_back(prog(t, a('p1') + 0.5 + i * 0.35, 0.7))
                if q <= 0:
                    continue
                x = 360 + i * 600
                cv = Cv((x - 130, 480, x + 130, 740))
                cv.ellipse((x - 100, 520, x + 100, 720), fill=rgba(col))
                cv.paste(img, clamp(q) * al, dy=30 * (1 - clamp(q)))
                text(img, (x, 620 + 30 * (1 - clamp(q))), str(i + 1), 120, 'Black', NAVY, 'mm', clamp(q) * al)
                text(img, (x, 790), lab, 38, 'Bold', WHITE, 'mm', clamp(q) * al)
        elif sid == 'p2':
            pill(img, 960, 148, 'TIP 1', 24, GREEN, NAVY, padx=24, h=44, alpha=al)
            text(img, (960, 212), 'Pay yourself first', 58, 'ExtraBold', WHITE, 'mm', al)
            card(img, (170, 400, 640, 640), 30, (255, 255, 255), int(255 * al))
            text(img, (405, 462), 'PAYCHECK ARRIVES', 24, 'Bold', GREY, 'mm', al)
            text(img, (405, 540), '+ $3,000', 76, 'Black', GREEN_D, 'mm', al)
            text(img, (405, 600), 'Payday ✓', 28, 'Bold', GREY, 'mm', al)
            bx0, bx1 = 1060, 1760
            card(img, (bx0, 330, bx1, 520), 30, (255, 255, 255), int(40 * al), shad=False, outline=rgba(GREEN, 230 * al))
            icon(img, 'piggy', bx0 + 80, 425, 42, NAVY, GREEN, al)
            text(img, (bx0 + 150, 395), 'Auto-transfer to savings', 32, 'Bold', WHITE, 'lm', al)
            text(img, (bx0 + 150, 455), '$600', 60, 'Black', GREEN, 'lm', al)
            card(img, (bx0, 600, bx1, 790), 30, (255, 255, 255), int(40 * al), shad=False, outline=rgba(BLUE, 230 * al))
            icon(img, 'cart', bx0 + 80, 695, 42, NAVY, BLUE, al)
            text(img, (bx0 + 150, 665), 'Left to spend: needs + wants', 32, 'Bold', WHITE, 'lm', al)
            text(img, (bx0 + 150, 725), '$2,400', 60, 'Black', (140, 185, 255), 'lm', al)
            dd = ImageDraw.Draw(img, 'RGBA')
            for pts, col in (([(640, 520), (850, 520), (850, 425), (1050, 425)], GREEN), ([(640, 520), (850, 520), (850, 695), (1050, 695)], BLUE)):
                dd.line(pts, fill=rgba(WHITE, 70 * al), width=6, joint='curve')
            if al > .5:
                _flow(img, [(640, 520), (850, 520), (850, 425), (1050, 425)], t, a('p2') + 1.2, GREEN, 4)
                _flow(img, [(640, 520), (850, 520), (850, 695), (1050, 695)], t, a('p2') + 1.6, (140, 185, 255), 6)
            pill(img, 960, 905, 'Savings leave BEFORE you can spend them', 36, GOLD, NAVY, padx=44, h=72, alpha=al * e_out(prog(t, a('p2') + 2.6, 0.6)))
        elif sid == 'p3':
            pill(img, 960, 148, 'TIP 2', 24, BLUE, WHITE, padx=24, h=44, alpha=al)
            text(img, (960, 212), 'Track it in a simple spreadsheet', 58, 'ExtraBold', WHITE, 'mm', al)
            box = (230, 330, 1250, 900)
            card(img, box, 30, (252, 253, 255), int(255 * al))
            text(img, (270, 380), 'This week: how am I doing?', 30, 'Bold', (50, 60, 80), 'lm', al)
            tr = [('Needs', 1420, 1500, NEEDS), ('Wants', 610, 900, GOLD), ('Savings', 600, 600, GREEN)]
            for i, (nm, sp, bu, col) in enumerate(tr):
                q = e_out(prog(t, a('p3') + 0.4 + i * 0.5, 0.9))
                y = 480 + i * 128
                text(img, (270, y - 22), nm, 30, 'Bold', (30, 40, 60), 'lm', al)
                text(img, (1210, y - 22), f'{money(sp * q)} / {money(bu)}', 28, 'SemiBold', (90, 102, 125), 'rm', al)
                cvp = Cv((266, y, 1214, y + 52), s=2)
                cvp.rrect((270, y + 4, 1210, y + 40), 18, fill=rgba(LIGHT))
                cvp.rrect((270, y + 4, 270 + max(36, 940 * sp / bu * q), y + 40), 18, fill=rgba(col))
                cvp.paste(img, al)
            cp = e_back(prog(t, a('p3') + 1.6, 0.8))
            if cp > 0:
                al2 = clamp(cp) * al
                card(img, (1330, 400, 1730, 760), 36, (255, 255, 255), int(255 * al2))
                text(img, (1530, 470), 'WEEKLY CHECK-IN', 24, 'Bold', GREY, 'mm', al2)
                text(img, (1530, 575), '10', 150, 'Black', BLUE, 'mm', al2)
                text(img, (1530, 665), 'minutes a week', 34, 'Bold', (50, 60, 80), 'mm', al2)
                text(img, (1530, 715), 'Sunday is a great time', 24, 'Medium', GREY, 'mm', al2)
        else:
            pill(img, 960, 148, 'TIP 3', 24, GOLD, NAVY, padx=24, h=44, alpha=al)
            text(img, (960, 212), 'Adjust the rule to fit your life', 58, 'ExtraBold', WHITE, 'mm', al)
            bars = [('Standard', (50, 30, 20), 440), ('High-rent city', (60, 20, 20), 690)]
            for i, (nm, sp, y) in enumerate(bars):
                q = e_out(prog(t, a('p4') + 0.3 + i * (d('p4') * 0.42), 0.9))
                if q <= 0:
                    continue
                text(img, (260, y - 70), nm, 38, 'Bold', WHITE, 'lm', al * clamp(q * 2))
                x = 260
                tw = 1400
                cvb = Cv((x - 4, y - 44, x + tw + 4, y + 64), s=2)
                xa = x
                for j, (v, col) in enumerate(zip(sp, (NEEDS, WANTS, SAVE))):
                    w = tw * v / 100 * q
                    cvb.rrect((xa, y - 40, xa + w + (2 if j < 2 else 0), y + 60), 0, fill=rgba(col))
                    xa += w
                mask = Image.new('L', cvb.im.size, 0)
                ImageDraw.Draw(mask).rounded_rectangle([(0 + 4) * 2, 4 * 2, (4 + tw * q) * 2, (4 + 100) * 2], 48, fill=255)
                cvb.im.putalpha(ImageChops.multiply(cvb.im.getchannel('A'), mask))
                cvb.paste(img, al)
                cx_ = x
                for v, lab in zip(sp, ('Needs', 'Wants', 'Savings')):
                    w = tw * v / 100 * q
                    text(img, (cx_ + w / 2, y + 10), f'{v}%', 44, 'Black', NAVY, 'mm', al * clamp(q * 2))
                    text(img, (cx_ + w / 2, y + 92), lab, 24, 'Medium', GREY, 'mm', al * clamp(q * 2))
                    cx_ += w
            text(img, (960, 940), 'The goal: progress, not perfection', 40, 'Bold', GREEN, 'mm', al * e_out(prog(t, a('p4') + d('p4') * 0.75, 0.6)))


# ======================= 9. OUTRO =========================================
def s_outro(img, t, S):
    a, d = A(S), D(S)
    bg_soft(img, t, NAVY, NAVY2, GREEN, 8)
    money_rain(img, t + 20, 14, 21, 0.45)
    fade_overlay(img, NAVY, 0.35)
    tiles = [('c2', '50%', 'NEEDS', '$1,500', NEEDS, 'house'), ('c3', '30%', 'WANTS', '$900', WANTS, 'star'), ('c4', '20%', 'FUTURE YOU', '$600', SAVE, 'piggy')]
    ly = 0
    tf = 1 - e_inout(prog(t, a('c5') - 0.2, 0.6))
    la = 1 - 0.0
    text(img, (960, 190 + ly * 0.6), 'THE RECAP', 36, 'Bold', GREY, 'mm', e_out(prog(t, a('c1'), 0.5)) * (1 - prog(t, a('c5') - 0.2, 0.4)))
    for i, (sid, pc, nm, amt, col, ic) in enumerate(tiles):
        q = e_back(prog(t, a(sid) - 0.05, 0.8))
        if q <= 0:
            continue
        al = clamp(q) * tf
        if al < 0.01:
            continue
        x = 190 + i * 560
        y0 = 280 + 40 * (1 - clamp(q)) + ly
        box = (x, y0, x + 520, y0 + 520)
        card(img, box, 36, (255, 255, 255), int(34 * al), shad=False, outline=rgba(col, 240 * al))
        icon(img, ic, x + 260, y0 + 100, 52, NAVY, col, al)
        text(img, (x + 260, y0 + 260), pc, 150, 'Black', col, 'mm', al)
        text(img, (x + 260, y0 + 370), nm, 40, 'Bold', WHITE, 'mm', al)
        text(img, (x + 260, y0 + 440), amt + ' / month', 34, 'SemiBold', GREY, 'mm', al)
    # CTA
    cp = e_back(prog(t, a('c5') + 0.2, 0.9))
    if cp > 0:
        al = clamp(cp)
        yy = 520 + 40 * (1 - al)
        text(img, (960, yy - 180), 'Enjoyed this?', 84, 'Black', WHITE, 'mm', al)
        bw = 560
        cv = Cv((960 - bw / 2 - 6, yy - 60, 960 + bw / 2 + 120, yy + 70))
        cv.rrect((960 - bw / 2, yy - 56, 960 + bw / 2, yy + 56), 56, fill=rgba((235, 40, 40)))
        cv.poly([(960 - bw / 2 + 56, yy - 22), (960 - bw / 2 + 56, yy + 22), (960 - bw / 2 + 92, yy)], fill=rgba(WHITE))
        cv.paste(img, al)
        text(img, (960 + 24, yy), 'SUBSCRIBE', 52, 'Black', WHITE, 'mm', al)
        text(img, (960, yy + 130), 'Which bucket is hardest for you?  Tell me in the comments.', 38, 'SemiBold', LIGHT, 'mm', al * e_out(prog(t, a('c5') + 1.8, 0.6)))
        text(img, (960, yy + 200), 'Broke → Balance  •  your paycheck, simplified', 32, 'Bold', GREEN, 'mm', al * e_out(prog(t, a('c5') + 2.6, 0.6)))
    dp = e_out(prog(t, a('c6') + 0.1, 0.8))
    text(img, (960, 940), 'For educational purposes only. Not financial advice. Examples are illustrative.', 26, 'Medium', GREY, 'mm', dp)


# ======================= 8b. MISTAKES =====================================
def s_mistakes(img, t, S):
    a, d = A(S), D(S)
    bg_soft(img, t, NAVY, (58, 28, 48), CORAL, 9)
    header(img, t, a('m1'), 'WATCH OUT', '3 mistakes that break budgets', CORAL)
    cards = [
        ('m2', 'Budgeting gross pay', ['$3,600  \u2717', '$3,000  \u2713'], 'Always start from take-home', 'bolt'),
        ('m3', 'Forgetting irregular costs', ['Car repairs', 'Gifts  \u2022  Annual fees'], 'Set a little aside each month', 'shield'),
        ('m4', 'Being too strict', ['All rules, no fun', '\u2192  you quit'], 'Leave room for fun', 'star'),
    ]
    for i, (sid, ttl, lines, fix, ic) in enumerate(cards):
        p = e_back(prog(t, a(sid) - 0.05, 0.8))
        if p <= 0:
            continue
        al = clamp(p)
        x = 150 + i * 580
        y0 = 340 + 50 * (1 - al)
        box = (x, y0, x + 540, y0 + 540)
        card(img, box, 34, (255, 255, 255), int(30 * al), shad=False, outline=rgba(CORAL, 230 * al))
        icon(img, 'x', x + 84, y0 + 84, 44, WHITE, CORAL, al)
        text(img, (x + 40, y0 + 190), ttl, 36, 'ExtraBold', WHITE, 'lm', al)
        for j, ln in enumerate(lines):
            text(img, (x + 40, y0 + 262 + j * 54), ln, 32, 'SemiBold', LIGHT, 'lm', al)
        fp = e_out(prog(t, a(sid) + 1.8, 0.6))
        pill(img, x + 270, y0 + 462, 'FIX: ' + fix, 25, GREEN, NAVY, padx=24, h=58, alpha=al * fp) if fp > 0 else None


RENDER = {'hook': s_hook, 'title': s_title, 'takehome': s_takehome, 'rule': s_rule, 'needs': s_needs,
          'wants': s_wants, 'savings': s_savings, 'tips': s_tips, 'mistakes': s_mistakes, 'outro': s_outro}


# ---- sound-effect events (local scene time, kind) ----------------------------
def events(sid, S):
    a, d = A(S), D(S)
    ev = []
    if sid == 'hook':
        ev.append((a('h1') - 0.3, 'whoosh'))
        t0 = a('h2'); span = (a('h3') + d('h3') * .85) - t0
        ev += [(t0 + span * i / 7, 'pop') for i in range(7)]
    elif sid == 'title':
        ev += [(a('t1') - 0.2, 'whoosh'), (a('t1') + 0.5, 'ching')]
    elif sid == 'takehome':
        ev += [(a('a1') + 0.4, 'ding'), (a('a3'), 'pop'), (a('a4'), 'pop'), (a('a5'), 'ching')]
    elif sid == 'rule':
        ev += [(a('r1') + 0.3, 'whoosh'), (a('r2') + .05, 'swell'), (a('r3') + .05, 'swell'), (a('r4') + .05, 'swell')]
    elif sid == 'needs':
        n = len(ROWS); span = max(0.5, d('n1') - 1.4)
        ev += [(a('n1') + 0.9 + span * i / n, 'pop') for i in range(n)] + [(a('n3') + 0.2, 'ching')]
    elif sid == 'wants':
        ev += [(a('w1') + 0.7 + (d('w1') - 1.4) * i / 6, 'pop') for i in range(6)] + [(a('w2') - .2, 'ching'), (a('w3') + .4, 'pop'), (a('w3') + 1.3, 'pop')]
    elif sid == 'savings':
        ev += [(a(k), 'pop') for k in ('s2a', 's2b', 's2c')] + [(a('s3') + .1, 'whoosh'), (a('s4') + max(2.0, d('s4') * .8) * 0.85, 'ching')]
    elif sid == 'tips':
        ev += [(a('p1') + .5 + i * .35, 'pop') for i in range(3)] + [(a('p2'), 'whoosh'), (a('p3'), 'whoosh'), (a('p4'), 'whoosh')]
    elif sid == 'mistakes':
        ev += [(a('m1') + .3, 'whoosh'), (a('m2'), 'pop'), (a('m3'), 'pop'), (a('m4'), 'pop')]
    elif sid == 'outro':
        ev += [(a('c2'), 'pop'), (a('c3'), 'pop'), (a('c4'), 'pop'), (a('c5') + .2, 'ching')]
    return [(max(0, x), k) for x, k in ev]
