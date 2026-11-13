"""Episode 5 - Credit Score Explained: The 5 Factors. Style: game HUD / 'level up' (indigo grid, LEVEL chips, boss fight, level-up reveal)."""
from lib import *
from engine import E

CYAN = (80, 200, 255); VIOLET = (150, 125, 255); ORANGE = (255, 160, 70); LIME = (140, 220, 110)
META = dict(final='Broke_to_Balance_Ep5_Credit_Score_Explained.mp4', music=4, voice_speed=1.04, gfx_speed=1.9, bg_speed=2.2,
            thumb=dict(lines=[('CREDIT', 150, WHITE), ('SCORE', 150, CYAN), ('LEVEL UP', 96, GOLD)], accent=VIOLET, icon='shield', tag='5 FACTORS', y0=280, bg=dict(kind='hud', k=3)))
STYLE = dict(theme='night', header='hud', bg=dict(kind='hud', k=3),
             trans=['flash', 'wipe', 'zoom', 'slide', 'flash', 'wipe', 'zoom', 'flash', 'slide', 'wipe', 'zoom', 'flash'])
ZONES = [(0, .507, CORAL), (.509, .671, ORANGE), (.673, .798, GOLD), (.800, .907, LIME), (.909, 1.0, GREEN)]


def lvl(n, title, col=CYAN):
    return dict(tag=f'LEVEL {n}', title=title, color=col, segs=5, on=n)


SPEC = [
    dict(id='hook', lead=3.2, mood='noir', bg=dict(kind='footage', clip='arcade_1', dim=.55), segs=[
        ('h1', "Player one, you're about to enter a game you didn't know you were playing.", None),
        ('h2', "It's called credit. And your score decides whether lenders, landlords, and insurers say yes, and what it costs you when they do.", None),
        ('h3', "Most people never learn the rules. Today, you'll learn all five.", None)],
        els=[E('title', 0.6, until='h2', region=(140, 300, 1780, 800), lines=[('PLAYER ONE', 150, CYAN, 'Black'), ('PRESS START', 70, WHITE, 'Black')]),
             E('callout', 'h2+3.0', until='h3', region=(140, 330, 1780, 800), lines=['The score decides:', 'yes or no, and the price'], size=76, color=VIOLET, fg=WHITE),
             E('callout', 'h3+0.5', region=(140, 330, 1780, 800), lines=['5 levels.', '5 factors.'], size=110, color=CYAN)]),
    dict(id='title', bg=dict(kind='rain', accent=VIOLET, k=7), segs=[
        ('t1', "Welcome back to Broke to Balance.", None),
        ('t2', "Quick note: this is educational, not personal financial advice. I'll use the common U.S. FICO scale as the example, and other scoring models and countries differ.", None)],
        els=[E('brand', 't1', sub_at='t1+1.0', pill='Credit Score Explained: The 5 Factors That Matter', line='EPISODE 5  •  BUDGETING BASICS')]),
    dict(id='score', header=lvl(0, 'What is a credit score?'), segs=[
        ('s1', "First, what is a credit score?", None),
        ('s2', "It's a three-digit number that summarizes how risky you look to a lender. On the most common scale, it runs from three hundred to eight hundred fifty.", None),
        ('s3', "Lenders use it to decide whether to approve you, and what interest rate to charge. Landlords and some insurers may look at your credit too.", None),
        ('s4', "A higher score can mean lower interest rates, and over the years, that can save you thousands of dollars.", None)],
        els=[E('gauge', 's1+0.6', region=(100, 310, 1020, 940), full=False, frac=.7636, zones=ZONES, valtext='720', size=130, label='GOOD', dur=2.4),
             E('bullets', 's3', region=(1100, 340, 1780, 900), size=34, items=[
                 dict(text='Loan approval', icon='check', color=CYAN, at='s3+0.6'), dict(text='Interest rate', icon='bolt', color=VIOLET, at='s3+2.0'),
                 dict(text='Rental applications', icon='house', color=GOLD, at='s3+5.6'), dict(text='Some insurance prices', icon='shield', color=GREEN, at='s3+7.4')])]),
    dict(id='bands', header=lvl(0, 'The score ranges'), segs=[
        ('b1', "Here are the FICO ranges.", None),
        ('b2', "Three hundred to five seventy-nine is poor. Five eighty to six sixty-nine is fair. Six seventy to seven thirty-nine is good.", None),
        ('b3', "Seven forty to seven ninety-nine is very good. And eight hundred and up is exceptional.", None),
        ('b4', "If you're lower than you'd like, don't panic. Scores move, and you're about to learn the levers.", None)],
        els=[E('table', 'b1', region=(140, 330, 1100, 800), title='FICO ranges.xlsx', formula=('A1', 'Score'), cols=[('Score range', 3), ('Rating', 3)], rows=[
                 dict(cells=['300 – 579', 'Poor'], at='b2+0.8', style='bad'), dict(cells=['580 – 669', 'Fair'], at='b2+3.2'), dict(cells=['670 – 739', 'Good'], at='b2+5.4'),
                 dict(cells=['740 – 799', 'Very good'], at='b3+0.6'), dict(cells=['800 – 850', 'Exceptional'], at='b3+3.6', style='total')]),
             E('callout', 'b4+0.6', region=(1200, 380, 1780, 780), lines=['Scores move.', 'You have levers.'], size=64, color=VIOLET, fg=WHITE)]),
    dict(id='tale', header=lvl(0, 'Why it matters: two scores'), segs=[
        ('w1', "Why does this matter? Let's compare two borrowers taking the same twenty thousand dollar car loan over five years.", None),
        ('w2', "Sam has a score around seven sixty, and gets a six percent rate. Alex has a score around six forty, and gets twelve percent. Those rates are illustrative, but the pattern is real.", None),
        ('w3', "Sam pays about three hundred eighty-seven dollars a month, and about thirty-two hundred in total interest. Alex pays about four hundred forty-five a month, and about sixty-seven hundred in interest.", None),
        ('w4', "Same car. Same loan. A score gap that costs Alex roughly thirty-five hundred dollars more.", None)],
        els=[E('compare', 'w1+1.0', region=(140, 320, 1100, 800),
               left=dict(at='w2', title='Sam: score ~760', color=GREEN, icon='check', bullet='check', lines=[dict(text='6% APR (illustrative)', at='w2+1.6'), dict(text='$387 a month', at='w3+0.8'), dict(text='~$3,200 interest', at='w3+3.0')]),
               right=dict(at='w2+4.4', title='Alex: score ~640', color=CORAL, icon='x', bullet='x', lines=[dict(text='12% APR (illustrative)', at='w2+5.6'), dict(text='$445 a month', at='w3+4.8'), dict(text='~$6,700 interest', at='w3+7.4')])),
             E('counter', 'w4+1.8', region=(1180, 340, 1780, 780), label='THE SCORE GAP COSTS', to=3494, size=120, color=CORAL, dur=1.6, note='in extra interest')]),
    dict(id='five', header=lvl(0, 'The scoring recipe'), segs=[
        ('v1', "Here's the recipe behind a FICO score.", None),
        ('v2', "Payment history is thirty-five percent. Amounts owed is thirty. Length of credit history is fifteen. New credit is ten. And credit mix is ten.", None),
        ('v3', "Other models, like VantageScore, weigh things a little differently, but the big ideas are the same.", None),
        ('v4', "Five factors. Five levels. Let's play.", None)],
        els=[E('donut', 'v2', region=(140, 320, 1780, 940), center=('FICO', 70, 'score recipe'), items=[
                 dict(label='Payment history', frac=.35, color=GREEN, at='v2+0.8'), dict(label='Amounts owed', frac=.30, color=GOLD, at='v2+3.0'), dict(label='Length of history', frac=.15, color=CYAN, at='v2+5.6'),
                 dict(label='New credit', frac=.10, color=CORAL, at='v2+8.0'), dict(label='Credit mix', frac=.10, color=VIOLET, at='v2+9.4')])]),
    dict(id='l1', header=lvl(1, 'Payment history: 35%', GREEN), segs=[
        ('p1', "Level one, the biggest boss: payment history, thirty-five percent of your score.", None),
        ('p2', "The question is simple: do you pay on time? Even one payment that's thirty days late can hurt, and late payments can stay on your report for up to seven years.", None),
        ('p3', "The fix is easy. Set up autopay for at least the minimum, and add a calendar reminder for the due date.", None)],
        els=[E('calendar', 'p1+1.0', region=(140, 310, 1100, 930), title='Due dates', days=30, start=3, color=GREEN, marks=[
                 dict(day=5, color=GREEN, label='paid', at='p2+1.0'), dict(day=15, color=GREEN, label='paid', at='p2+2.2'), dict(day=25, color=GREEN, label='paid', at='p2+3.4'),
                 dict(day=28, color=CORAL, label='late!', at='p2+6.0')]),
             E('bullets', 'p3', region=(1180, 340, 1780, 800), size=34, items=[
                 dict(text='Autopay the minimum', icon='check', color=GREEN, at='p3+1.8'), dict(text='Calendar reminder', icon='bolt', color=GOLD, at='p3+4.6')])]),
    dict(id='boss', dur=5.6, mood='tension', bg=dict(kind='hud', k=5), els=[
        E('title', 0.5, until=2.6, lines=[('BOSS FIGHT', 150, CORAL, 'Black'), ('LEVEL 2', 70, WHITE, 'Black')]), E('title', 2.8, lines=[('CREDIT', 120, WHITE, 'Black'), ('UTILIZATION', 150, GOLD, 'Black')])],
        sfx=[(0.5, 'thud'), (2.8, 'thud')]),
    dict(id='l2', header=lvl(2, 'Amounts owed: 30%', GOLD), segs=[
        ('u1', "Level two: amounts owed, thirty percent. The big idea here is credit utilization.", None),
        ('u2', "That's how much of your available credit you're using. If your limit is three thousand dollars and you carry nine hundred, that's thirty percent.", None),
        ('u3', "A common guideline is to stay under thirty percent, and lower is generally better.", None),
        ('u4', "Two tips. Pay down balances before the statement closes. And if you ask for a higher limit, don't spend more because of it.", None)],
        els=[E('gauge', 'u2', region=(100, 310, 920, 940), frac=.30, color=GOLD, valtext='30%', size=110, label='$900 of $3,000', dur=2.0),
             E('callout', 'u3+0.4', region=(1000, 340, 1780, 640), lines=['Under 30%', 'Lower is better'], size=64, color=GOLD),
             E('bullets', 'u4', region=(1000, 340, 1780, 820), size=32, items=[
                 dict(text='Pay down before the statement closes', icon='piggy', color=GOLD, at='u4+1.4'), dict(text='Higher limit? Do not spend more', icon='shield', color=GREEN, at='u4+5.6')])]),
    dict(id='l3', header=lvl(3, 'Length of history: 15%', CYAN), segs=[
        ('g1', "Level three: length of credit history, fifteen percent.", None),
        ('g2', "Lenders like a long track record. The average age of your accounts matters, and so does how long your oldest one has been open.", None),
        ('g3', "So keep old accounts open if they have no annual fee, and use them for a small purchase now and then to keep them active.", None)],
        els=[E('steps', 'g1+1.0', region=(140, 330, 1780, 600), items=[
                 dict(title='Open', sub='Day one', color=CYAN, at='g2+0.6'), dict(title='Year 3', sub='History builds', color=CYAN, at='g2+3.0'), dict(title='Year 7', sub='Stronger', color=VIOLET, at='g2+5.0'), dict(title='Year 10+', sub='Strong track record', color=GREEN, at='g2+7.0')]),
             E('bullets', 'g3', region=(300, 640, 1620, 930), size=34, items=[
                 dict(text='Keep old, no-fee accounts open', icon='check', color=CYAN, at='g3+0.8'), dict(text='Use them occasionally', icon='bag', color=CYAN, at='g3+4.8')])]),
    dict(id='l4', header=lvl(4, 'New credit: 10%', CORAL), segs=[
        ('n1', "Level four: new credit, ten percent.", None),
        ('n2', "When you apply for credit, the lender does a hard inquiry, which can dip your score a little. Several applications in a short time can add up.", None),
        ('n3', "Checking your own score is a soft inquiry, and it doesn't hurt. So check as often as you like.", None)],
        els=[E('compare', 'n1+0.6', region=(140, 320, 1780, 900),
               left=dict(at='n2', title='Hard inquiry', color=CORAL, icon='x', bullet='x', lines=[dict(text='You apply for new credit', at='n2+1.0'), dict(text='Small, temporary dip', at='n2+4.4'), dict(text='Many at once adds up', at='n2+7.4')]),
               right=dict(at='n3', title='Soft inquiry', color=GREEN, icon='check', bullet='check', lines=[dict(text='You check your own score', at='n3+1.0'), dict(text='No impact on your score', at='n3+4.0')]))]),
    dict(id='l5', header=lvl(5, 'Credit mix: 10%', VIOLET), segs=[
        ('m1', "Level five: credit mix, ten percent.", None),
        ('m2', "Lenders like to see you can handle different kinds of credit: revolving credit, like credit cards, and installment loans, like a car loan or student loan.", None),
        ('m3', "But please don't take out a loan just to improve your mix. It's only ten percent, and debt you don't need isn't worth it.", None)],
        els=[E('cards', 'm2', region=(140, 330, 1780, 700), items=[
                 dict(icon='cart', title='Revolving', color=VIOLET, at='m2+1.6', body=['Credit cards. The balance can go up and down each month.']),
                 dict(icon='car', title='Installment', color=CYAN, at='m2+5.6', body=['Car loans, student loans, mortgages. Fixed payments over time.'])]),
             E('callout', 'm3+1.0', region=(140, 760, 1780, 940), lines=["Never borrow just to improve your mix"], size=50, color=GOLD)]),
    dict(id='levelup', dur=6.0, mood='reveal', bg=dict(kind='footage', clip='arcade_1', dim=.62), els=[
        E('title', 0.8, lines=[('LEVEL UP!', 190, GOLD, 'Black'), ('5 factors unlocked', 70, WHITE, 'Black')])], sfx=[(1.0, 'sparkle')]),
    dict(id='plan', header=dict(tag='GAME PLAN', title='How to raise your score', color=GREEN, segs=5, on=5), segs=[
        ('i1', "So how do you raise your score? Think of it as a game plan, not a trick.", None),
        ('i2', "Start with autopay, so every payment is on time.", None),
        ('i3', "Next, bring your balances down, so your utilization drops.", None),
        ('i4', "Avoid opening several accounts at once, and dispute any errors you find.", None),
        ('i5', "Then be patient. Most changes take months, not days, and good habits compound.", None)],
        els=[E('steps', 'i1+1.0', region=(140, 360, 1780, 640), items=[
                 dict(title='1. Autopay', sub='Every payment on time', color=GREEN, at='i2+0.4'), dict(title='2. Lower balances', sub='Utilization drops', color=GOLD, at='i3+0.4'),
                 dict(title='3. Stay steady', sub='Few new accounts, fix errors', color=CYAN, at='i4+0.4'), dict(title='4. Be patient', sub='Habits compound', color=VIOLET, at='i5+0.4')]),
             E('callout', 'i5+1.6', region=(140, 720, 1780, 930), lines=['Months, not days'], size=96, color=GOLD)]),
    dict(id='protect', header=dict(tag='SHIELD UP', title='Protect your credit', color=CYAN, segs=5, on=5), segs=[
        ('d1', "One more power-up: protect your credit from fraud.", None),
        ('d2', "In the U.S., you can freeze your credit with each bureau for free, which stops new accounts from being opened in your name.", None),
        ('d3', "You can also set up fraud alerts, and review your statements and reports regularly.", None),
        ('d4', "If you spot something you didn't do, report it right away.", None)],
        els=[E('cards', 'd2', region=(140, 340, 1780, 760), items=[
                 dict(icon='shield', title='Credit freeze', color=CYAN, at='d2+1.0', body=['Free in the U.S. Blocks new accounts in your name.']), dict(icon='bolt', title='Fraud alerts', color=GOLD, at='d3+0.4', body=['Get notified of suspicious activity.']),
                 dict(icon='check', title='Regular reviews', color=GREEN, at='d3+3.2', body=['Check statements and reports often.'])]),
             E('callout', 'd4+0.4', region=(140, 800, 1780, 950), lines=['See something odd? Report it right away'], size=50, color=CORAL, fg=WHITE)]),
    dict(id='check', header=dict(tag='CHECKPOINT', title='See where you stand', color=CYAN, segs=5, on=5), segs=[
        ('k1', "Now, how do you see where you stand?", None),
        ('k2', "In the U.S., you can get free credit reports from the three major bureaus at annual credit report dot com.", "In the U.S., you can get free credit reports from the three major bureaus at AnnualCreditReport.com."),
        ('k3', "Read them for mistakes, like accounts that aren't yours, and dispute anything wrong.", None),
        ('k4', "Many banks and card issuers also show a free score in their app.", None)],
        els=[E('clip', 'k1', region=(140, 340, 840, 760), clip='banking_2', color=CYAN, label='CHECKPOINT'),
             E('checklist', 'k2', region=(920, 330, 1780, 900), size=32, items=[
                 dict(text='Get your free reports', at='k2+2.0', color=CYAN), dict(text='Look for errors', at='k3+0.8', color=CYAN), dict(text='Dispute anything wrong', at='k3+3.0', color=CYAN),
                 dict(text='Check the score in your app', at='k4+1.0', color=CYAN)])]),
    dict(id='build', header=dict(tag='SIDE QUEST', title='Building credit from zero', color=GOLD, segs=5, on=5), segs=[
        ('q1', "What if you're starting from scratch?", None),
        ('q2', "Three common ways to start: a secured card, where you put down a deposit. A credit-builder loan. Or becoming an authorized user on a trusted person's card.", None),
        ('q3', "Whatever you choose, put one small recurring bill on it, and pay the full statement every month.", None)],
        els=[E('cards', 'q2', region=(140, 330, 1780, 700), items=[
                 dict(icon='shield', title='Secured card', color=GOLD, at='q2+3.2', body=['You put down a deposit as the limit.']), dict(icon='piggy', title='Credit-builder loan', color=CYAN, at='q2+5.6', body=['Small loan; payments are reported.']),
                 dict(icon='check', title='Authorized user', color=VIOLET, at='q2+8.8', body=['Piggyback on a trusted person card (their habits matter).'])]),
             E('callout', 'q3+0.6', region=(140, 760, 1780, 940), lines=['Small bill + pay in full = history'], size=54, color=GREEN)]),
    dict(id='myths', header=dict(tag='MYTHBUSTERS', title='Four credit myths', color=CORAL, segs=5, on=5), segs=[
        ('y1', "Before we finish, four myths.", None),
        ('y2', "Myth one: carrying a balance helps your score. It doesn't. It only costs you interest. Pay in full when you can.", None),
        ('y3', "Myth two: checking your own score hurts it. That's a soft inquiry, so it doesn't.", None),
        ('y4', "Myth three: closing old cards always helps. It can shorten your history and raise your utilization.", None),
        ('y5', "And myth four: your income is part of your score. It isn't. Your credit report doesn't include income.", None)],
        els=[E('bullets', 'y2', region=(160, 330, 1760, 940), size=36, items=[
                 dict(text='MYTH: A balance helps your score', sub='FACT: It only costs interest. Pay in full.', icon='x', color=CORAL, at='y2+0.4'), dict(text='MYTH: Checking your score hurts it', sub='FACT: Soft inquiry. No impact.', icon='x', color=CORAL, at='y3+0.4'),
                 dict(text='MYTH: Closing old cards always helps', sub='FACT: It can shorten history, raise utilization.', icon='x', color=CORAL, at='y4+0.4'), dict(text='MYTH: Income is in your score', sub='FACT: Credit reports do not include income.', icon='x', color=CORAL, at='y5+0.4')])]),
    dict(id='outro', bg=dict(kind='footage', clip='gaming_1', dim=.66, grid='hud'), segs=[
        ('r1', "Let's recap.", None),
        ('r2', "Your score has five factors: payment history, amounts owed, length of history, new credit, and credit mix.", None),
        ('r3', "Pay on time, keep balances low, and be patient. Time is on your side.", None),
        ('r4', "If this helped, subscribe, and tell me in the comments: which level is toughest for you?", None),
        ('r5', "And if you learned something from this video, don't forget to watch our next one: how to budget when you're paid every two weeks, or your income changes.", None),
        ('r6', "This video is for education only and isn't financial advice. See you next time.", None)],
        els=[E('bullets', 'r1', until='r4', region=(220, 300, 1700, 860), size=44, items=[
                 dict(text='5 factors: pay on time, keep balances low', icon='check', color=GREEN, at='r2'), dict(text='Be patient: time is on your side', icon='check', color=CYAN, at='r3')]),
             E('cta', 'r4+0.5', question='Which level is toughest for you?', next='How to Budget on a Biweekly or Irregular Paycheck'),
             E('title', 'r6', region=(140, 900, 1780, 970), lines=[('For educational purposes only. Not financial advice. Examples are illustrative. Footage: Pixabay.', 26, GREY, 'Medium')])]),
]
