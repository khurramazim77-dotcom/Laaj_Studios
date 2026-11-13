"""Episode 3 - Stop Overspending: The 30-Minute Money Audit.
Style: punchy 'money detective' case file. Dotted investigation-board background, stamped case headers, fast cuts, footage panels."""
from lib import *
from engine import E

META = dict(final='Broke_to_Balance_Ep3_Stop_Overspending.mp4', music=3, voice_speed=1.06, gfx_speed=1.9, bg_speed=2.4,
            thumb=dict(lines=[('WHERE DID', 140, WHITE), ('MY MONEY', 150, CORAL), ('GO?', 190, GOLD)], accent=CORAL, icon='cart', tag='30-MIN AUDIT', y0=290,
                       bg=dict(kind='dots', accent=CORAL, k=2)))
STYLE = dict(theme='night', header='stamp', bg=dict(kind='dots', accent=CORAL, k=2),
             trans=['wipe', 'flash', 'zoom', 'slide', 'wipe', 'zoom', 'flash', 'slide', 'wipe', 'zoom', 'flash'])

SPEC = [
    dict(id='hook', lead=4.2, mood='noir', bg=dict(kind='footage', clip='city_night_0', dim=.5), segs=[
        ('h1', "Case file number one: the vanishing paycheck.", None),
        ('h2', "Every month, the same money walks in the front door, and somehow it slips out the back.", None),
        ('h3', "You don't have an income problem. You have a leak problem.", None),
        ('h4', "Today, we're going to find every leak in thirty minutes.", None)],
        els=[E('title', 0.8, until='h3', region=(140, 300, 1780, 800), lines=[('CASE FILE #1', 44, CORAL, 'Black'), ('THE VANISHING', 120, WHITE, 'Black'), ('PAYCHECK', 150, GOLD, 'Black')]),
             E('callout', 'h3+0.5', until='h4', region=(140, 350, 1780, 750), lines=['Not an income problem.', 'A LEAK problem.'], size=84, color=CORAL, fg=WHITE),
             E('callout', 'h4+0.2', region=(140, 350, 1780, 750), lines=['Every leak.', '30 minutes.'], size=96, color=GOLD)]),
    dict(id='title', bg=dict(kind='rain', accent=CORAL, k=3), segs=[
        ('t1', "Welcome to Broke to Balance. I'm your guide on this case.", None),
        ('t2', "A quick note before we start: this is educational, not personal financial advice. Now, let's open the file.", None)],
        els=[E('brand', 't1', sub_at='t1+1.5', pill='Stop Overspending: The 30-Minute Money Audit', line='EPISODE 3  •  BUDGETING BASICS')]),
    dict(id='evidence', header=dict(tag='STEP 1', title='Gather the evidence', color=CORAL), segs=[
        ('e1', "Step one: gather the evidence.", None),
        ('e2', "Download the last sixty to ninety days of transactions from your bank accounts and credit cards.", None),
        ('e3', "Most banks let you export a spreadsheet. If yours doesn't, copy the lines into one yourself.", None),
        ('e4', "Why sixty to ninety days? Because one month can be unusual. Three months shows your real patterns.", None)],
        els=[E('clip', 'e1', region=(140, 340, 900, 760), clip='laptop_1', color=CORAL, label='EVIDENCE'),
             E('checklist', 'e2', region=(980, 340, 1780, 760), size=34, items=[
                 dict(text='Bank accounts', at='e2+3.4', color=CORAL), dict(text='Credit cards', at='e2+4.9', color=CORAL), dict(text='Export to a spreadsheet', at='e3+1.2', color=CORAL)]),
             E('callout', 'e4+0.4', region=(140, 790, 1780, 950), lines=['60 to 90 days shows your real patterns'], size=50, color=GOLD)]),
    dict(id='sort', header=dict(tag='STEP 2', title='Sort every line into 3 buckets', color=CORAL), segs=[
        ('so1', "Step two: sort every line into three buckets, the same ones from our first video: needs, wants, and savings.", None),
        ('so2', "In our example, take-home pay is three thousand dollars.", None),
        ('so3', "The audit finds needs at sixteen hundred forty dollars, wants at eleven hundred eighty, and savings at just one hundred eighty.", None),
        ('so4', "Compare that to the fifty, thirty, twenty targets: fifteen hundred, nine hundred, and six hundred.", None),
        ('so5', "The gap: needs are one hundred forty over, wants are two hundred eighty over, and savings are four hundred twenty short.", None),
        ('so6', "That's the story the numbers tell. Now let's find the culprits.", None)],
        els=[E('donut', 'so2', region=(140, 320, 1000, 930), legend=False, center=('$3,000', 66, 'take-home'), items=[
                 dict(label='Needs', frac=1640 / 3000, color=BLUE, at='so3+1.8'), dict(label='Wants', frac=1180 / 3000, color=GOLD, at='so3+4.2'), dict(label='Savings', frac=180 / 3000, color=GREEN, at='so3+6.6')]),
             E('table', 'so3+0.5', region=(1060, 340, 1780, 760), title='Audit.xlsx', formula=('D2', '=B2-C2'), cols=[('Bucket', 3), ('Actual', 2), ('Target', 2), ('Gap', 2)], rows=[
                 dict(cells=['Needs', '1,640', '1,500', '+140'], at='so3+1.8'), dict(cells=['Wants', '1,180', '900', '+280'], at='so3+4.2'), dict(cells=['Savings', '180', '600', '−420'], at='so3+6.6', style='bad')]),
             E('callout', 'so5+1.0', region=(1060, 790, 1780, 950), lines=['$420 short of the savings goal'], size=38, color=CORAL, fg=WHITE)]),
    dict(id='suspects', dur=7.6, mood='tension', bg=dict(kind='soft'), els=[
        E('montage', 0.2, clips=['phone_0', 'coffee_1', 'shopping_1', 'mall_0'], words=['SUBSCRIPTIONS', 'THE SMALL STUFF', 'IMPULSE BUYS', 'HIDDEN FEES'], step=1.8, label='THE SUSPECTS')],
        sfx=[(0.2, 'thud'), (2.0, 'thud'), (3.8, 'thud'), (5.6, 'thud')]),
    dict(id='exA', header=dict(tag='EXHIBIT A', title='The subscription lineup', color=GOLD), segs=[
        ('a1', "Exhibit A: subscriptions. These are the quiet leaks, because they bill you while you're not looking.", None),
        ('a2', "List every recurring charge, then multiply the monthly price by twelve. That's the real cost.", None),
        ('a3', "In our example, five subscriptions add up to sixty-eight dollars a month. That's about eight hundred fifteen dollars a year.", None),
        ('a4', "Now ask three questions about each one. Did I use it this month? Would I sign up again today? Is there a cheaper plan?", None),
        ('a5', "Cancel, pause, or downgrade anything that fails.", None)],
        els=[E('table', 'a1+2.0', region=(140, 320, 1100, 900), title='Subscriptions.xlsx', formula=('C7', '=SUM(C2:C6)'), cols=[('Service', 4), ('Monthly', 2), ('Per year', 2)], rows=[
                 dict(cells=['Streaming', '15.99', '191.88'], at='a2+3.0'), dict(cells=['Music', '10.99', '131.88'], at='a2+4.2'), dict(cells=['Cloud storage', '2.99', '35.88'], at='a2+5.4'),
                 dict(cells=['Gym (unused)', '29.99', '359.88'], at='a2+6.6', style='bad'), dict(cells=['Forgotten app', '7.99', '95.88'], at='a2+7.8', style='bad'),
                 dict(cells=['TOTAL', '67.95', '815.40'], at='a3', style='total')]),
             E('counter', 'a3+2.0', until='a4', region=(1180, 340, 1780, 720), label='PER YEAR', to=815, size=140, color=CORAL, dur=1.6),
             E('checklist', 'a4', region=(1180, 330, 1780, 700), size=30, items=[
                 dict(text='Used it this month?', at='a4+1.0', color=GOLD), dict(text='Sign up again today?', at='a4+4.0', color=GOLD), dict(text='Cheaper plan available?', at='a4+6.6', color=GOLD)]),
             E('callout', 'a5+0.2', region=(1180, 740, 1780, 920), lines=['Cancel. Pause.', 'Downgrade.'], size=54, color=CORAL, fg=WHITE)]),
    dict(id='exB', header=dict(tag='EXHIBIT B', title='The small stuff', color=GOLD), segs=[
        ('b1', "Exhibit B: the small stuff. Coffee, snacks, delivery fees.", None),
        ('b2', "Nobody feels a seven dollar purchase. But seven dollars, three times a week, is about one thousand ninety dollars a year.", None),
        ('b3', "That's not a reason to give up coffee. It's a reason to choose the small purchases you truly love, and cut the ones you barely notice.", None)],
        els=[E('clip', 'b1', region=(140, 340, 840, 700), clip='coffee_1', color=GOLD, label='EXHIBIT B'),
             E('flow', 'b2', region=(900, 340, 1780, 700), dotcolor=GOLD, nodes=[
                 dict(id='a', x=900, y=370, w=290, h=190, title='One coffee run', sub='$7', color=GOLD, size=26, subsize=56, at='b2+0.6'),
                 dict(id='b', x=1240, y=370, w=250, h=190, title='3 a week', sub='$21', color=GOLD, size=26, subsize=56, at='b2+2.6'),
                 dict(id='c', x=1560, y=370, w=220, h=190, title='A year', sub='$1,092', color=CORAL, size=26, subsize=44, at='b2+5.2')],
               arrows=[('a', 'b', 'b2+2.2'), ('b', 'c', 'b2+4.6')]),
             E('callout', 'b3+0.4', region=(140, 740, 1780, 950), lines=['Keep what you love.  Cut what you barely notice.'], size=54, color=GREEN)]),
    dict(id='exC', header=dict(tag='EXHIBIT C', title='Impulse purchases', color=GOLD), segs=[
        ('c1', "Exhibit C: impulse purchases. The fix isn't willpower, it's friction.", None),
        ('c2', "Rule one: the twenty-four hour rule. Put it in the cart, and wait a day before you buy.", None),
        ('c3', "Rule two: for bigger items, keep a thirty-day wish list. If you still want it after a month, it's probably a real want.", None),
        ('c4', "Rule three: remove saved cards from shopping sites and apps, so buying takes a few extra steps.", None),
        ('c5', "And rule four: unsubscribe from promotional emails and turn off shopping notifications. If you can't see the sale, it can't tempt you.", None)],
        els=[E('clip', 'c1', region=(140, 340, 840, 800), clip='shopping_1', color=GOLD, label='EXHIBIT C'),
             E('bullets', 'c2', region=(920, 330, 1780, 930), size=34, items=[
                 dict(text='24-hour rule', sub='Cart it, then wait a day', icon='bolt', color=GOLD, at='c2+0.4'), dict(text='30-day wish list', sub='Still want it next month?', icon='star', color=GOLD, at='c3+0.4'),
                 dict(text='Remove saved cards', sub='Add a few steps to checkout', icon='shield', color=GOLD, at='c4+0.4'), dict(text='Mute the promos', sub='No sale seen, no sale chased', icon='bag', color=GOLD, at='c5+0.4')])]),
    dict(id='exD', header=dict(tag='EXHIBIT D', title='The fee leaks', color=GOLD), segs=[
        ('y1', "Exhibit D: fees. These are the leaks nobody chooses.", None),
        ('y2', "Late fees, overdraft fees, ATM fees, and credit card interest can quietly drain your account.", None),
        ('y3', "Set up autopay for at least the minimum payment, and turn on low-balance alerts.", None),
        ('y4', "Use your bank's own ATMs, and if you do get hit with a fee, call and ask for a one-time waiver. Many banks will say yes.", None)],
        els=[E('checklist', 'y2', until='y3', region=(300, 330, 1620, 800), size=40, items=[
                 dict(text='Late fees', ok=False, at='y2+1.2'), dict(text='Overdraft fees', ok=False, at='y2+2.4'), dict(text='ATM fees', ok=False, at='y2+3.6'), dict(text='Credit card interest', ok=False, at='y2+4.9')]),
             E('checklist', 'y3', region=(300, 330, 1620, 800), size=40, items=[
                 dict(text='Autopay the minimum', at='y3+1.0', color=GREEN), dict(text='Low-balance alerts', at='y3+3.4', color=GREEN),
                 dict(text="Use your bank's ATMs", at='y4+0.8', color=GREEN), dict(text='Ask for a one-time waiver', at='y4+3.4', color=GREEN)])]),
    dict(id='exE', header=dict(tag='EXHIBIT E', title='Needs you can negotiate', color=GOLD), segs=[
        ('d1', "Exhibit D: the needs you can negotiate.", None),
        ('d2', "Needs aren't always fixed. Insurance, phone, internet, and even some utilities can often be shopped around.", None),
        ('d3', "Call your providers, ask what discounts or cheaper plans they offer, and compare quotes.", None),
        ('d4', "If you trim just twenty dollars from three bills, that's sixty dollars a month, or seven hundred twenty dollars a year.", None)],
        els=[E('cards', 'd1+1.0', region=(140, 320, 1780, 700), items=[
                 dict(icon='shield', title='Insurance', color=BLUE, at='d2+1.0', body=['Compare quotes at renewal time.']),
                 dict(icon='bolt', title='Phone & internet', color=GOLD, at='d2+3.2', body=['Ask for a cheaper plan or a loyalty discount.']),
                 dict(icon='house', title='Utilities', color=GREEN, at='d2+5.0', body=['Check for discounts and budget-billing options.'])]),
             E('counter', 'd4+1.6', region=(140, 730, 1780, 960), label='3 BILLS x $20 LESS', to=720, size=120, color=GREEN, dur=1.5, note='saved per year')]),
    dict(id='plan', header=dict(tag='STEP 3', title='Decide, then automate', color=CORAL), segs=[
        ('p1', "Step three: decide where the recovered money goes before you spend it again.", None),
        ('p2', "Say you cancel two subscriptions for about thirty-eight dollars a month, and trim small purchases by sixty. That's roughly one hundred dollars a month.", None),
        ('p3', "Set an automatic transfer on payday: straight into your emergency fund, or toward debt.", None),
        ('p4', "Over a year, that's about twelve hundred dollars, from a thirty-minute audit.", None)],
        els=[E('flow', 'p2', region=(140, 320, 1780, 650), dotcolor=GREEN, nodes=[
                 dict(id='a', x=160, y=360, w=480, h=200, title='Leaks found', sub='~$100 / month', color=CORAL, icon='x', subsize=44, at='p2+7.0'),
                 dict(id='b', x=720, y=360, w=480, h=200, title='Auto-transfer', sub='on payday', color=GOLD, icon='bolt', subsize=44, at='p3+0.4'),
                 dict(id='c', x=1280, y=360, w=480, h=200, title='Emergency fund', sub='or debt payoff', color=GREEN, icon='shield', subsize=40, at='p3+2.6')],
               arrows=[('a', 'b', 'p3+0.2'), ('b', 'c', 'p3+2.2')]),
             E('counter', 'p4+0.4', region=(140, 690, 1780, 950), label='ABOUT', to=1200, size=130, color=GREEN, dur=1.4, note='per year, from one audit')]),
    dict(id='reveal', dur=6.8, mood='reveal', bg=dict(kind='footage', clip='money_1', dim=.62, grid='dots'), els=[
        E('title', 0.9, lines=[('ONE AUDIT', 120, WHITE, 'Black'), ('LATER...', 170, GOLD, 'Black')])], sfx=[(1.0, 'sparkle')]),
    dict(id='results', header=dict(tag='RESULTS', title='What one audit can do', color=GREEN), segs=[
        ('z1', "Let's see what one audit can do.", None),
        ('z2', "After trimming sixty dollars from negotiated bills, and ninety-eight dollars from subscriptions and small purchases, our example frees up one hundred fifty-eight dollars a month.", None),
        ('z3', "Savings jump from one hundred eighty to three hundred thirty-eight dollars a month. That's nearly double, with no new income.", None),
        ('z4', "It's still short of the six hundred dollar target, and that's fine. The first audit is always the biggest win, and you can run it again next quarter.", None)],
        els=[E('table', 'z1+0.8', region=(140, 320, 1000, 760), title='After the audit.xlsx', formula=('B4', '=SUM(B2:B3)'), cols=[('What changed', 4), ('Per month', 2)], rows=[
                 dict(cells=['Negotiated bills', '60'], at='z2+3.0'), dict(cells=['Subscriptions + small buys', '98'], at='z2+7.0'), dict(cells=['FREED UP', '158'], at='z2+10.6', style='total')]),
             E('columns', 'z3', region=(1080, 310, 1780, 940), max=600, items=[
                 dict(label='Before', value=180, color=CORAL, at='z3+0.8'), dict(label='After', value=338, color=GREEN, at='z3+3.0'), dict(label='Target', value=600, color=GOLD, at='z4+0.6')])]),
    dict(id='fun', header=dict(tag='BONUS', title='Give your fun money a home', color=GREEN), segs=[
        ('u1', "Here's the part most audits miss: don't cut all the fun.", None),
        ('u2', "A budget with zero fun gets abandoned fast. Instead, give your wants a home.", None),
        ('u3', "Set a monthly fun budget, move it to a separate account or card, and spend from that and nothing else.", None),
        ('u4', "When the fun money runs out, you're done until next month. And while it lasts, you can spend it with zero guilt.", None)],
        els=[E('gauge', 'u2', region=(140, 320, 900, 930), frac=0.39, color=GOLD, valtext='$350', size=100, label='fun money left (of $900)', dur=2.0),
             E('bullets', 'u3', region=(1000, 340, 1780, 880), size=36, items=[
                 dict(text='Set a fun budget', icon='star', color=GOLD, at='u3+0.4'), dict(text='Separate card or account', icon='shield', color=BLUE, at='u3+3.0'),
                 dict(text='Spend it guilt-free', icon='check', color=GREEN, at='u4+3.2')])]),
    dict(id='freeze', header=dict(tag='CHALLENGE', title='The 7-day spending freeze', color=GREEN), segs=[
        ('f1', "Here's a fun challenge: a seven day spending freeze.", None),
        ('f2', "For one week, spend only on needs: rent, groceries, utilities, transportation, and insurance.", None),
        ('f3', "Each day, write down what you almost bought. Those notes are pure gold.", None),
        ('f4', "At the end of the week, you'll know which wants you actually missed, and which ones you never thought about again.", None)],
        els=[E('calendar', 'f1+0.4', region=(140, 310, 1080, 940), title='The freeze week', days=14, start=1, color=GREEN, marks=[
                 dict(day=d, color=GREEN, label='needs', at=f'f2+{0.8 + 0.7 * (d - 1)}') for d in range(1, 8)]),
             E('bullets', 'f2', region=(1180, 330, 1780, 900), size=34, items=[
                 dict(text='Needs only', icon='house', color=GREEN, at='f2+0.4'), dict(text='Log what you almost bought', icon='dots', color=GOLD, at='f3+0.4'),
                 dict(text='Keep the wants you missed', icon='star', color=CORAL, at='f4+0.4')])]),
    dict(id='tools', header=dict(tag='TOOLKIT', title='Spreadsheet or app?', color=BLUE), segs=[
        ('k1', "What should you use to track all this? There's no single right answer.", None),
        ('k2', "A spreadsheet is free, flexible, and shows you exactly how the numbers work.", None),
        ('k3', "Budgeting apps can import transactions automatically, but check their fees and privacy policies before connecting your accounts.", None),
        ('k4', "And plain pen and paper works too. The best tool is the one you'll actually open every week.", None)],
        els=[E('compare', 'k1+1.0', region=(140, 320, 1780, 800),
               left=dict(at='k2', title='Spreadsheet', color=BLUE, icon='check', lines=[dict(text='Free', at='k2+0.8'), dict(text='Total control', at='k2+2.0'), dict(text='Manual entry', at='k2+3.4')], bullet='check'),
               right=dict(at='k3', title='Budgeting app', color=GOLD, icon='bolt', lines=[dict(text='Auto-imports transactions', at='k3+0.8'), dict(text='Quick charts', at='k3+3.0'), dict(text='Check fees & privacy', at='k3+5.0')], bullet='check')),
             E('callout', 'k4+1.0', region=(140, 820, 1780, 960), lines=['The best tool is the one you open every week'], size=46, color=GREEN)]),
    dict(id='mistakes', header=dict(tag='AVOID', title='Four audit mistakes', color=CORAL), segs=[
        ('m1', "A few audit mistakes to avoid.", None),
        ('m2', "Don't turn it into a shame spiral. You're an investigator, not a judge. The goal is information.", None),
        ('m3', "Don't cut everything at once. Pick two or three leaks, fix them, and build from there.", None),
        ('m4', "Watch for annual charges, like insurance or memberships, which hide between monthly statements.", None),
        ('m5', "And repeat the audit every quarter. Leaks grow back.", None)],
        els=[E('bullets', 'm2', region=(200, 330, 1720, 940), size=40, items=[
                 dict(text='The shame spiral', sub='Investigator, not judge', icon='x', color=CORAL, at='m2+0.4'), dict(text='Cutting everything at once', sub='Fix two or three leaks first', icon='x', color=CORAL, at='m3+0.4'),
                 dict(text='Missing annual charges', sub='They hide between statements', icon='x', color=CORAL, at='m4+0.4'), dict(text='Doing it once', sub='Repeat every quarter', icon='x', color=CORAL, at='m5+0.4')])]),
    dict(id='verdict', dur=6.4, mood='verdict', bg=dict(kind='footage', clip='money_0', dim=.7, grid='dots'), els=[
        E('title', 0.2, region=(140, 190, 1780, 330), lines=[('THE VERDICT', 96, GOLD, 'Black')]),
        E('stamps', 0.9, region=(240, 340, 1680, 940), size=64, items=[
            dict(text='Forgotten subscriptions', at=1.0), dict(text='Daily small stuff', at=2.1), dict(text='Impulse buys', at=3.2), dict(text='Surprise fees', at=4.3)])],
        sfx=[(1.0, 'thud'), (2.1, 'thud'), (3.2, 'thud'), (4.3, 'thud')]),
    dict(id='outro', bg=dict(kind='footage', clip='money_2', dim=.62, grid='dots'), segs=[
        ('r1', "Let's close the case.", None),
        ('r2', "Gather ninety days of evidence.", None),
        ('r3', "Sort it into needs, wants, and savings.", None),
        ('r4', "Hunt the subscriptions, the small stuff, and the impulse buys.", None),
        ('r5', "Then automate what you recover.", None),
        ('r6', "Next time, we go head to head: debt snowball versus debt avalanche.", None),
        ('r7', "If this helped, subscribe, and tell me in the comments: what was your biggest leak?", None),
        ('r7b', "And if you learned something from this video, don't forget to watch our next video.", None),
        ('r8', "This video is for education only and isn't financial advice. Case closed.", None)],
        els=[E('checklist', 'r1', until='r6', region=(300, 300, 1620, 900), size=40, items=[
                 dict(text='Gather 90 days of evidence', at='r2', color=GREEN), dict(text='Sort: needs, wants, savings', at='r3', color=GREEN),
                 dict(text='Hunt subscriptions, small stuff, impulse buys', at='r4', color=GREEN), dict(text='Automate what you recover', at='r5', color=GREEN)]),
             E('cta', 'r6+3.0', question='What was your biggest leak?', next='Debt Snowball vs Debt Avalanche'),
             E('title', 'r8', region=(140, 900, 1780, 970), lines=[('For educational purposes only. Not financial advice. Examples are illustrative. Footage: Pixabay.', 26, GREY, 'Medium')])]),
]
