"""Episode 4 - Debt Snowball vs Debt Avalanche. Style: championship showdown. Blue-vs-coral corners, band headers, countdown, race chart."""
from lib import *
from engine import E
from debt_sim import snow, aval, mins

META = dict(final='Broke_to_Balance_Ep4_Snowball_vs_Avalanche.mp4', music=1, voice_speed=1.05, gfx_speed=1.9, bg_speed=2.2,
            thumb=dict(lines=[('SNOWBALL', 130, BLUE), ('VS', 90, WHITE), ('AVALANCHE', 118, CORAL)], accent=GOLD, icon='bolt', tag='WHICH WINS?', y0=280, bg=dict(kind='versus', k=4)))
STYLE = dict(theme='night', header='band', bg=dict(kind='versus', k=4),
             trans=['zoom', 'wipe', 'flash', 'slide', 'zoom', 'wipe', 'flash', 'zoom', 'slide', 'wipe', 'flash', 'zoom'])

SPEC = [
    dict(id='hook', lead=3.4, mood='noir', bg=dict(kind='footage', clip='ring_1', dim=.5), segs=[
        ('h1', "Ladies and gentlemen, welcome to the main event.", None),
        ('h2', "In the left corner, going after the smallest balance first: the Debt Snowball!", None),
        ('h3', "And in the right corner, going after the highest interest rate: the Debt Avalanche!", None),
        ('h4', "Two proven ways to crush debt. One saves more money. The other keeps you motivated. Who wins? Let's run the numbers.", None)],
        els=[E('title', 0.6, until='h2+1.0', region=(140, 300, 1780, 800), lines=[('THE MAIN EVENT', 52, GOLD, 'Black'), ('DEBT', 150, WHITE, 'Black'), ('SHOWDOWN', 170, CORAL, 'Black')]),
             E('compare', 'h2', region=(140, 330, 1780, 700),
               left=dict(at='h2+0.4', title='THE SNOWBALL', color=BLUE, icon='star', bullet='check', lines=[dict(text='Smallest balance first', at='h2+1.4'), dict(text='Quick wins', at='h2+2.8')]),
               right=dict(at='h3+0.4', title='THE AVALANCHE', color=CORAL, icon='bolt', bullet='check', lines=[dict(text='Highest interest rate first', at='h3+1.4'), dict(text='Saves more interest', at='h3+3.0')])),
             E('callout', 'h4+4.6', region=(140, 760, 1780, 940), lines=['Who wins?'], size=96, color=GOLD)]),
    dict(id='title', bg=dict(kind='rain', accent=BLUE, k=6), segs=[
        ('t1', "Welcome back to Broke to Balance.", None),
        ('t2', "Quick note: this is educational, not personal financial advice. And no payoff method works if you can't cover your minimum payments, so we're assuming you can. Let's go.", None)],
        els=[E('brand', 't1', sub_at='t1+1.0', pill='Debt Snowball vs Debt Avalanche: Which Pays Off Faster?', line='EPISODE 4  •  BUDGETING BASICS')]),
    dict(id='why', header=dict(tag='THE PROBLEM', title='Why debt feels so heavy', color=CORAL), segs=[
        ('w1', "First, why does debt feel like running up a down escalator?", None),
        ('w2', "Interest. Every month, your lender charges a percentage of what you still owe.", None),
        ('w3', "Say you owe five thousand dollars on a card at twenty-four percent A P R, and you pay only one hundred twenty-five dollars a month.", "Say you owe $5,000 on a card at 24% APR, and you pay only $125 a month."),
        ('w4', "It would take about eighty-two months, almost seven years, and cost roughly five thousand one hundred sixty dollars in interest. More than the original balance.", None)],
        els=[E('clip', 'w1', until='w3', region=(140, 340, 940, 760), clip='calc_0', color=CORAL, label='THE PROBLEM'),
             E('callout', 'w2+0.8', until='w3', region=(1020, 340, 1780, 760), lines=['Interest =', 'a % of what', 'you still owe'], size=62, color=CORAL, fg=WHITE),
             E('cards', 'w3', region=(140, 330, 1780, 590), items=[
                 dict(icon='cart', title='Balance', big='$5,000', color=BLUE, at='w3+0.8', tsize=30, body=[]), dict(icon='bolt', title='Interest rate', big='24%', color=CORAL, at='w3+2.6', tsize=30, body=[]),
                 dict(icon='piggy', title='Monthly payment', big='$125', color=GOLD, at='w3+5.0', tsize=30, body=[])]),
             E('counter', 'w4+2.0', region=(140, 640, 920, 940), label='MONTHS TO PAY IT OFF', to=82, fmt='int', size=140, color=CORAL, dur=1.8, note='almost 7 years'),
             E('counter', 'w4+6.0', region=(1000, 640, 1780, 940), label='INTEREST PAID', to=5159, size=130, color=CORAL, dur=1.8, note='more than the balance')]),
    dict(id='month1', header=dict(tag='ONE MONTH', title='Interest in slow motion', color=CORAL), segs=[
        ('y1', "Let's watch interest in slow motion.", None),
        ('y2', "Five thousand dollars at twenty-four percent A P R is two percent a month. That's one hundred dollars of interest in the first month alone.", "$5,000 at 24% APR is 2% a month. That's $100 of interest in the first month alone."),
        ('y3', "Your minimum payment is one hundred twenty-five dollars. So only twenty-five of it actually reduces the debt.", None),
        ('y4', "That's why paying a little extra, aimed at the right debt, makes such a big difference.", None)],
        els=[E('flow', 'y2', region=(140, 330, 1780, 640), dotcolor=GOLD, nodes=[
                 dict(id='a', x=140, y=380, w=340, h=200, title='Balance', sub='$5,000', color=BLUE, icon='cart', subsize=52, at='y2+0.2'),
                 dict(id='b', x=570, y=380, w=340, h=200, title='Interest (2%)', sub='+ $100', color=CORAL, icon='bolt', subsize=52, at='y2+3.6'),
                 dict(id='c', x=1000, y=380, w=340, h=200, title='Your payment', sub='\u2212 $125', color=GOLD, icon='piggy', subsize=52, at='y3+0.2'),
                 dict(id='d', x=1430, y=380, w=340, h=200, title='Real progress', sub='only $25', color=GREEN, icon='check', subsize=52, at='y3+4.4')],
               arrows=[('a', 'b', 'y2+3.2'), ('b', 'c', 'y3+0.0'), ('c', 'd', 'y3+4.0')]),
             E('callout', 'y4+1.0', region=(140, 700, 1780, 930), lines=['Extra dollars, aimed right, hit the debt itself'], size=54, color=GOLD)]),
    dict(id='setup', header=dict(tag='THE SETUP', title='Meet the contenders', color=GOLD), segs=[
        ('s1', "Here's our test case: three debts, totaling eight thousand three hundred dollars.", None),
        ('s2', "A store card: eight hundred dollars at twelve percent. A personal loan: twenty-five hundred at fifteen percent. And a credit card: five thousand at twenty-four percent.", None),
        ('s3', "The minimum payments add up to two hundred thirty dollars a month. We'll add an extra three hundred, for a total of five hundred thirty.", None),
        ('s4', "Both methods follow the same rules. Pay the minimum on everything. Send every extra dollar to one target debt. And when a debt is gone, roll its payment into the next one.", None)],
        els=[E('table', 's1', region=(140, 330, 1120, 800), title='Debts.xlsx', formula=('C5', '=SUM(C2:C4)'), cols=[('Debt', 3), ('Balance', 2), ('APR', 1.4), ('Min', 1.4)], rows=[
                 dict(cells=['Store card', '800', '12%', '25'], at='s2+1.2'), dict(cells=['Personal loan', '2,500', '15%', '80'], at='s2+4.4'),
                 dict(cells=['Credit card', '5,000', '24%', '125'], at='s2+7.8'), dict(cells=['TOTAL', '8,300', '', '230'], at='s3', style='total')]),
             E('counter', 's3+3.0', until='s4', region=(1200, 340, 1780, 700), label='MONTHLY BUDGET', to=530, size=130, color=GREEN, dur=1.4, note='230 minimums + 300 extra'),
             E('checklist', 's4', region=(1200, 330, 1780, 860), size=28, items=[
                 dict(text='Minimums on everything', at='s4+1.4', color=GOLD), dict(text='Extra $ to ONE target', at='s4+4.2', color=GOLD), dict(text='Roll payments forward', at='s4+8.4', color=GOLD)])]),
    dict(id='roll', header=dict(tag='THE ENGINE', title='The roll-over', color=GOLD), segs=[
        ('o1', "Here's the secret engine behind both methods: the roll-over.", None),
        ('o2', "In the snowball, the first target gets three hundred twenty-five dollars a month. When it's gone, that payment plus the loan's minimum becomes four hundred five. Then the last debt gets the full five hundred thirty.", None),
        ('o3', "The avalanche works the same way: four twenty-five, then five oh five, then five thirty.", "The avalanche works the same way: $425, then $505, then $530."),
        ('o4', "Payments snowball in size as debts disappear. That's the whole trick.", None)],
        els=[E('title', 'o1+0.8', region=(140, 300, 940, 360), lines=[('SNOWBALL: payment on the target', 32, BLUE, 'Black')]),
             E('title', 'o3-1.0', region=(980, 300, 1780, 360), lines=[('AVALANCHE: payment on the target', 32, CORAL, 'Black')]),
             E('columns', 'o1+0.8', region=(140, 360, 940, 930), max=530, items=[
                 dict(label='Debt 1', value=325, color=BLUE, display='$325', at='o2+2.0'), dict(label='Debt 2', value=405, color=BLUE, display='$405', at='o2+6.0'), dict(label='Debt 3', value=530, color=BLUE, display='$530', at='o2+9.6')]),
             E('columns', 'o3-1.0', region=(980, 360, 1780, 930), max=530, items=[
                 dict(label='Debt 1', value=425, color=CORAL, display='$425', at='o3+0.8'), dict(label='Debt 2', value=505, color=CORAL, display='$505', at='o3+2.6'), dict(label='Debt 3', value=530, color=CORAL, display='$530', at='o3+4.4')])]),
    dict(id='snowball', header=dict(tag='LEFT CORNER', title='The Debt Snowball', color=BLUE), segs=[
        ('b1', "In the left corner, the Debt Snowball.", None),
        ('b2', "You list your debts from the smallest balance to the largest, ignoring the interest rate.", None),
        ('b3', "In our test, that means the store card first, then the personal loan, then the credit card.", None),
        ('b4', "Why do people love it? Quick wins. You knock out your first debt fast, and each win builds momentum, like a snowball rolling downhill.", None)],
        els=[E('clip', 'b1', region=(140, 340, 760, 640), clip='snow_2', color=BLUE, label='SNOWBALL'),
             E('steps', 'b2+1.0', region=(840, 340, 1780, 640), items=[
                 dict(title='1. Store card', sub='$800: smallest', color=BLUE, at='b3+0.9'), dict(title='2. Loan', sub='$2,500', color=BLUE, at='b3+2.7'), dict(title='3. Credit card', sub='$5,000: largest', color=BLUE, at='b3+4.3')]),
             E('callout', 'b4+3.0', region=(140, 700, 1780, 940), lines=['Quick wins build momentum'], size=62, color=BLUE, fg=WHITE)]),
    dict(id='avalanche', header=dict(tag='RIGHT CORNER', title='The Debt Avalanche', color=CORAL), segs=[
        ('a1', "In the right corner, the Debt Avalanche.", None),
        ('a2', "You list your debts from the highest interest rate to the lowest, ignoring the balance.", None),
        ('a3', "In our test: the credit card at twenty-four percent first, then the loan at fifteen, then the store card at twelve.", None),
        ('a4', "Why do people pick it? Math. Attacking the most expensive debt first means you pay less total interest.", None)],
        els=[E('clip', 'a1', region=(1160, 340, 1780, 640), clip='aval_1', color=CORAL, label='AVALANCHE'),
             E('steps', 'a2+1.0', region=(140, 340, 1080, 640), items=[
                 dict(title='1. Credit card', sub='24%: highest', color=CORAL, at='a3+0.8'), dict(title='2. Loan', sub='15%', color=CORAL, at='a3+3.4'), dict(title='3. Store card', sub='12%: lowest', color=CORAL, at='a3+5.2')]),
             E('callout', 'a4+3.0', region=(140, 700, 1780, 940), lines=['Most expensive debt first = less interest'], size=58, color=CORAL, fg=WHITE)]),
    dict(id='ready', dur=6.4, mood='tension', bg=dict(kind='versus', k=5), els=[
        E('title', 0.4, until=2.3, lines=[('ROUND 1', 150, GOLD, 'Black'), ('THE RACE', 110, WHITE, 'Black')]),
        E('title', 2.5, until=3.6, lines=[('3', 460, WHITE, 'Black')]), E('title', 3.6, until=4.7, lines=[('2', 460, GOLD, 'Black')]),
        E('title', 4.7, until=5.8, lines=[('1', 460, CORAL, 'Black')]), E('title', 5.8, lines=[('GO!', 340, GREEN, 'Black')])],
        sfx=[(2.5, 'thud'), (3.6, 'thud'), (4.7, 'thud'), (5.8, 'cash')]),
    dict(id='race', header=dict(tag='THE RACE', title='Total debt remaining', color=GOLD), segs=[
        ('r1', "And they're off. Both fighters put in the same five hundred thirty dollars every month.", None),
        ('r2', "The snowball clears the store card by month three, and the loan by month nine.", None),
        ('r3', "But the avalanche is attacking the card with the highest interest, so its interest bill shrinks faster.", None),
        ('r4', "By month fourteen, the avalanche has wiped out the biggest, costliest debt. Meanwhile, the snowball is still carrying it.", None),
        ('r5', "And at the finish line...", None)],
        els=[E('race', 'r1+0.4', region=(140, 310, 1780, 940), dur=22.6, series=[
            dict(label='SNOWBALL', color=BLUE, balances=snow['bal'], interest=snow['ints']), dict(label='AVALANCHE', color=CORAL, balances=aval['bal'], interest=aval['ints'])])]),
    dict(id='results', header=dict(tag='RESULTS', title='The scoreboard', color=GREEN), segs=[
        ('x1', "Final scores. Both methods leave you debt-free in month nineteen.", None),
        ('x2', "The snowball paid about fifteen hundred eighty-six dollars in interest. The avalanche paid about twelve hundred ninety-six.", None),
        ('x3', "That's roughly two hundred ninety dollars saved by the avalanche.", None),
        ('x4', "But look at the first win. The snowball cleared a whole debt in month three. The avalanche took fourteen months to clear its first.", None),
        ('x5', "So the avalanche wins on money, and the snowball wins on speed to the first victory.", None),
        ('x6', "And if your interest rates are all close together, the savings shrink, so the snowball's quick wins might matter more.", None)],
        els=[E('table', 'x1+0.6', region=(140, 330, 1100, 700), title='Scoreboard.xlsx', formula=('D3', '=B3-B2'), cols=[('Method', 3), ('Interest', 2), ('1st debt gone', 2.4), ('Debt-free', 2)], rows=[
                 dict(cells=['Snowball', '$1,586', 'Month 3', 'Month 19'], at='x2+1.0'), dict(cells=['Avalanche', '$1,296', 'Month 14', 'Month 19'], at='x2+4.6')]),
             E('counter', 'x3+0.2', region=(1180, 330, 1780, 700), label='AVALANCHE SAVES', to=290, size=140, color=GREEN, dur=1.2, note='in interest'),
             E('callout', 'x5+0.4', until='x6', region=(140, 760, 1780, 950), lines=['Avalanche = more money.   Snowball = faster win.'], size=54, color=GOLD),
             E('callout', 'x6+0.6', region=(140, 760, 1780, 950), lines=['Similar rates? Quick wins matter more'], size=54, color=BLUE, fg=WHITE)]),
    dict(id='winner', dur=6.6, mood='reveal', bg=dict(kind='footage', clip='snow_0', dim=.55, grid='dots'), els=[
        E('title', 0.8, until=3.4, lines=[('AND THE WINNER IS...', 100, WHITE, 'Black')]), E('title', 3.6, lines=[('THE ONE YOU', 100, WHITE, 'Black'), ('STICK WITH', 150, GOLD, 'Black')])],
        sfx=[(3.6, 'sparkle')]),
    dict(id='choose', header=dict(tag='YOUR PICK', title='Which should you choose?', color=GOLD), segs=[
        ('c1', "So which one should you choose?", None),
        ('c2', "Choose the avalanche if you're motivated by numbers, your interest rates are very different, and you can stay disciplined for the long haul.", None),
        ('c3', "Choose the snowball if you need early wins to stay motivated, or if you've quit plans before.", None),
        ('c4', "You can even mix them: start with a tiny debt for a quick win, then switch to the highest rate.", None),
        ('c5', "The best method is the one you'll actually finish.", None)],
        els=[E('compare', 'c1+0.8', region=(140, 320, 1780, 760),
               left=dict(at='c2', title='Avalanche if...', color=CORAL, icon='bolt', bullet='check', lines=[dict(text='Numbers motivate you', at='c2+1.0'), dict(text='Rates differ a lot', at='c2+3.6'), dict(text='You stay disciplined', at='c2+5.6')]),
               right=dict(at='c3', title='Snowball if...', color=BLUE, icon='star', bullet='check', lines=[dict(text='You need early wins', at='c3+1.0'), dict(text="You've quit plans before", at='c3+3.8')])),
             E('callout', 'c4+1.4', until='c5', region=(140, 790, 1780, 950), lines=['Hybrid: one quick win, then the highest rate'], size=50, color=GOLD),
             E('callout', 'c5+0.2', region=(140, 790, 1780, 950), lines=["Finish what you start"], size=64, color=GREEN)]),
    dict(id='power', header=dict(tag='POWER-UPS', title='Pay it off even faster', color=GREEN), segs=[
        ('u1', "A few ways to speed things up.", None),
        ('u2', "Call your lenders and ask for a lower rate, or look into a balance transfer, but read the fees and promotional terms carefully.", None),
        ('u3', "Send windfalls, like tax refunds and bonuses, straight to the target debt.", None),
        ('u4', "Pick up a temporary side income, and give every extra dollar a job.", None),
        ('u5', "And stop adding new debt. You can't empty a bathtub with the tap still running.", None)],
        els=[E('clip', 'u1', region=(140, 340, 800, 880), clip='bills_2', color=GREEN, label='POWER-UPS'),
             E('bullets', 'u2', region=(880, 330, 1780, 920), size=34, items=[
                 dict(text='Ask for a lower rate', sub='Read balance-transfer fine print', icon='bolt', color=GREEN, at='u2+0.6'), dict(text='Send windfalls to the target', sub='Refunds and bonuses', icon='star', color=GREEN, at='u3+0.4'),
                 dict(text='Add temporary side income', sub='Every extra dollar has a job', icon='piggy', color=GREEN, at='u4+0.4'), dict(text='Stop adding new debt', sub='Turn off the tap', icon='x', color=CORAL, at='u5+0.4')])]),
    dict(id='fit', header=dict(tag='BIG PICTURE', title='Where this fits in your budget', color=BLUE), segs=[
        ('f1', "Where does this fit in the fifty, thirty, twenty budget?", None),
        ('f2', "Debt payoff lives in your twenty percent bucket, alongside savings.", None),
        ('f3', "First, build the starter emergency fund from our last video, so one surprise doesn't push you back onto a card.", None),
        ('f4', "Then point the rest at your target debt, and automate the payment on payday.", None),
        ('f5', "And once the debt is gone, redirect that same payment to savings and investing. You already know how to live without it.", None)],
        els=[E('donut', 'f2', until='f3', region=(140, 320, 1780, 940), legend=True, center=('20%', 90, 'savings & debt'), items=[
                 dict(label='Needs', frac=.5, color=BLUE, at='f2+0.2', display='50%'), dict(label='Wants', frac=.3, color=GOLD, at='f2+0.4', display='30%'), dict(label='Savings & debt', frac=.2, color=GREEN, at='f2+1.2', display='20%')]),
             E('steps', 'f3', region=(140, 400, 1780, 700), items=[
                 dict(title='1. Starter fund', sub='A small cushion first', color=GREEN, at='f3+0.6'), dict(title='2. Target debt', sub='Automated on payday', color=CORAL, at='f4+0.6'), dict(title='3. Invest', sub='Redirect the payment', color=BLUE, at='f5+2.4')])]),
    dict(id='mistakes', header=dict(tag='AVOID', title='Four payoff mistakes', color=CORAL), segs=[
        ('m1', "Four mistakes to avoid.", None),
        ('m2', "One: skipping the minimum payments on the other debts. That triggers late fees and can hurt your credit.", None),
        ('m3', "Two: having no starter emergency fund, so every surprise lands back on the card.", None),
        ('m4', "Three: ignoring interest rates entirely when the gap between them is huge.", None),
        ('m5', "And four: quitting after one bad month. A slip doesn't erase your progress.", None)],
        els=[E('bullets', 'm2', region=(200, 330, 1720, 940), size=40, items=[
                 dict(text='Skipping minimum payments', sub='Late fees and credit damage', icon='x', color=CORAL, at='m2+0.4'), dict(text='No starter emergency fund', sub='Surprises land back on the card', icon='x', color=CORAL, at='m3+0.4'),
                 dict(text='Ignoring a huge rate gap', sub='Know your APRs', icon='x', color=CORAL, at='m4+0.4'), dict(text='Quitting after a bad month', sub='One slip is not a failure', icon='x', color=CORAL, at='m5+0.4')])]),
    dict(id='outro', bg=dict(kind='footage', clip='cardpay_2', dim=.62, grid='dots'), segs=[
        ('r1', "Let's recap.", None),
        ('r2', "List your debts. Snowball means smallest balance first. Avalanche means highest rate first.", None),
        ('r3', "Pay the minimum on everything, and send every extra dollar to the target.", None),
        ('r4', "The avalanche saves more interest, the snowball delivers faster wins, and the best method is the one you finish.", None),
        ('r5', "Next time, we decode your credit score: the five factors that actually matter.", None),
        ('r6', "If this helped, subscribe, and tell me in the comments: snowball or avalanche?", None),
        ('r7', "This video is for education only and isn't financial advice. See you next time.", None)],
        els=[E('bullets', 'r1', until='r5', region=(220, 300, 1700, 860), size=44, items=[
                 dict(text='List your debts', icon='check', color=GOLD, at='r2'), dict(text='Minimums on all, extra to ONE target', icon='check', color=GREEN, at='r3'),
                 dict(text='Avalanche = money.  Snowball = wins.', icon='check', color=BLUE, at='r4')]),
             E('cta', 'r5+1.0', question='Snowball or avalanche?', next='Credit Score Explained: The 5 Factors'),
             E('title', 'r7', region=(140, 900, 1780, 970), lines=[('For educational purposes only. Not financial advice. Examples are illustrative. Footage: Pixabay.', 26, GREY, 'Medium')])]),
]
