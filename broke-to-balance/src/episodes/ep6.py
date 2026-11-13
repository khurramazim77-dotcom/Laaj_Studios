"""Episode 6 - How to Budget on a Biweekly or Irregular Paycheck. Style: bright planner paper (light theme, tab headers, calendars), warm and practical."""
from lib import *
from engine import E

META = dict(final='Broke_to_Balance_Ep6_Biweekly_and_Irregular_Paycheck.mp4', music=5, voice_speed=1.0, gfx_speed=1.7, bg_speed=1.6,
            thumb=dict(lines=[('PAID EVERY', 110, WHITE), ('2 WEEKS?', 150, GOLD), ('BUDGET THIS WAY', 78, GREEN)], accent=GOLD, icon='check', tag='BIWEEKLY + IRREGULAR', y0=300,
                       bg=dict(kind='soft', c1=(14, 40, 60), c2=(8, 70, 80), accent=GOLD, k=4)))
STYLE = dict(theme='paper', header='tab', bg=dict(kind='paper'),
             trans=['slide', 'wipe', 'zoom', 'slide', 'wipe', 'flash', 'slide', 'zoom', 'wipe', 'slide', 'flash', 'zoom'])
INCOME = [2400, 3800, 1900, 3100, 4200, 2600, 3300, 2000, 3600, 2900, 3900, 2300]
BUFFER = [600, 1600, 700, 1000, 2400, 2200, 2700, 1900, 2700, 2800, 3900, 3400]
MON = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
EXTRA = [2, 2, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2]

SPEC = [
    dict(id='hook', lead=1.6, segs=[
        ('h1', "Your rent is due on the first. Your paycheck lands on a Friday. Every other Friday.", None),
        ('h2', "Or maybe you're a freelancer, and your income looks like a roller coaster.", None),
        ('h3', "The monthly budget advice you've seen probably doesn't fit. This will.", None),
        ('h4', "Today, you'll learn how to budget when you're paid every two weeks, and when your income changes every month.", None)],
        els=[E('calendar', 0.8, region=(140, 220, 1060, 960), title='A biweekly month', days=31, start=3, color=GREEN, marks=[
                 dict(day=1, color=CORAL, label='rent', at='h1+1.4'), dict(day=3, color=GREEN, label='pay', at='h1+3.0'), dict(day=15, color=CORAL, label='car', at='h1+3.6'),
                 dict(day=17, color=GREEN, label='pay', at='h1+4.4'), dict(day=31, color=GREEN, label='pay!', at='h1+5.6')]),
             E('callout', 'h2+0.6', until='h4', region=(1160, 300, 1780, 700), lines=['Biweekly?', 'Irregular?'], size=80, color=GOLD),
             E('callout', 'h4+1.0', region=(1160, 300, 1780, 700), lines=['Two paycheck', 'rhythms.', 'One plan.'], size=64, color=GREEN)]),
    dict(id='title', bg=dict(kind='paper'), segs=[
        ('t1', "Welcome back to Broke to Balance.", None),
        ('t2', "Quick note: this is educational, not personal financial advice. Let's get organized.", None)],
        els=[E('brand', 't1', sub_at='t1+1.0', pill='How to Budget on a Biweekly or Irregular Paycheck', line='EPISODE 6  •  BUDGETING BASICS')]),
    dict(id='rhythm', header=dict(tag='STEP 1', title='Know your pay rhythm', color=GOLD), segs=[
        ('r1', "First, know your pay rhythm. It changes your math.", None),
        ('r2', "Paid monthly? That's twelve paychecks a year. Paid twice a month, like the first and fifteenth? That's twenty-four.", None),
        ('r3', "Paid every two weeks? That's twenty-six. And paid weekly? Fifty-two.", None),
        ('r4', "Twice a month and every two weeks sound the same. They're not.", None)],
        els=[E('columns', 'r1+1.0', region=(140, 310, 1780, 940), max=52, items=[
                 dict(label='Monthly', value=12, color=BLUE, display='12', at='r2+0.8'), dict(label='Twice a month', value=24, color=BLUE, display='24', at='r2+3.6'),
                 dict(label='Every 2 weeks', value=26, color=GOLD, display='26', at='r3+0.6'), dict(label='Weekly', value=52, color=GREEN, display='52', at='r3+3.4')]),
             E('callout', 'r4+0.6', region=(300, 330, 1620, 520), lines=['24 ≠ 26'], size=90, color=CORAL, fg=WHITE)]),
    dict(id='twist', dur=6.8, mood='reveal', bg=dict(kind='footage', clip='calendar_0', dim=.5), els=[
        E('title', 0.7, lines=[('26 ≠ 24', 230, WHITE, 'Black'), ('2 EXTRA PAYCHECKS A YEAR', 66, GOLD, 'Black')])], sfx=[(1.0, 'sparkle')]),
    dict(id='bonus', header=dict(tag='THE BONUS', title='Two months a year, you get three', color=GREEN), segs=[
        ('b1', "Here's the secret. With twenty-six paychecks, most months have two paychecks, but two months a year have three.", None),
        ('b2', "Those are your bonus months. Not a bonus from your boss, just a quirk of the calendar.", None),
        ('b3', "Let's use an example: fourteen hundred dollars take-home per paycheck. Budgeting on two paychecks a month is twenty-eight hundred dollars.", None),
        ('b4', "The two extra checks add up to another twenty-eight hundred dollars a year. That's real money, if you plan for it.", None)],
        els=[E('columns', 'b1+1.0', region=(140, 310, 1780, 760), max=3, items=[
                 dict(label=MON[i], value=EXTRA[i], color=GREEN if EXTRA[i] == 3 else BLUE, display=str(EXTRA[i]), at=f'b1+{2.4 + 0.35 * i}') for i in range(12)]),
             E('callout', 'b2+0.4', region=(140, 780, 1780, 950), lines=['Paychecks per month: two... and sometimes three'], size=44, color=GREEN, fg=WHITE),
             E('counter', 'b4+0.6', region=(140, 780, 1780, 960), label='TWO EXTRA CHECKS', to=2800, size=84, color=GREEN, dur=1.4, note='per year (example: $1,400 each)')]),
    dict(id='planA', header=dict(tag='STRATEGY 1', title='Budget on two paychecks a month', color=GREEN), segs=[
        ('a1', "Strategy one: build your monthly budget around just two paychecks.", None),
        ('a2', "Pay your bills and live on those two. In the three-paycheck months, the third check is a bonus, and it gets a job.", None),
        ('a3', "Send it to your emergency fund, extra debt payments, or a sinking fund for annual bills.", None),
        ('a4', "That way, you never get used to money that only shows up twice a year.", None)],
        els=[E('flow', 'a1+0.8', region=(140, 320, 1780, 700), dotcolor=GREEN, nodes=[
                 dict(id='a', x=140, y=380, w=500, h=200, title='Two paychecks', sub='$2,800 budget', color=BLUE, icon='check', subsize=44, at='a1+1.6'),
                 dict(id='b', x=720, y=380, w=500, h=200, title='Third paycheck', sub='$1,400 bonus', color=GOLD, icon='star', subsize=44, at='a2+3.0'),
                 dict(id='c', x=1300, y=380, w=480, h=200, title='Gets a job', sub='fund / debt', color=GREEN, icon='piggy', subsize=44, at='a3+0.6')],
               arrows=[('a', 'b', 'a2+2.6'), ('b', 'c', 'a3+0.2')]),
             E('bullets', 'a3+1.0', region=(300, 700, 1620, 940), size=32, rowh=80, items=[
                 dict(text='Emergency fund   •   Extra debt payoff   •   Annual-bill fund', icon='check', color=GREEN, at='a3+2.6')])]),
    dict(id='extra', header=dict(tag='EXAMPLE', title='What $2,800 of extra checks can do', color=GREEN), segs=[
        ('w1', "So what could twenty-eight hundred dollars of extra paychecks do in one year?", None),
        ('w2', "Put one thousand dollars into your emergency fund. Put another one thousand toward debt. And put eight hundred into a fund for annual bills.", None),
        ('w3', "All without touching your normal monthly budget.", None),
        ('w4', "That's the power of treating a calendar quirk as a feature, not an afterthought.", None)],
        els=[E('donut', 'w2', region=(140, 320, 1780, 940), center=('$2,800', 64, 'extra per year'), items=[
                 dict(label='Emergency fund', frac=1000 / 2800, color=GREEN, display='$1,000', at='w2+0.8'), dict(label='Extra debt payment', frac=1000 / 2800, color=BLUE, display='$1,000', at='w2+3.6'),
                 dict(label='Annual-bill fund', frac=800 / 2800, color=GOLD, display='$800', at='w2+6.8')])]),
    dict(id='planB', header=dict(tag='STRATEGY 2', title='Make a bill map', color=BLUE), segs=[
        ('m1', "Strategy two: make a bill map.", None),
        ('m2', "List every bill with its due date. Then match each bill to the paycheck that arrives before it.", None),
        ('m3', "Say your first paycheck of the month covers rent and utilities. The second covers the car, the phone, and insurance.", None),
        ('m4', "And if a due date is awkward, call the company. Many will let you move it to match your payday.", None)],
        els=[E('table', 'm1+0.8', region=(140, 320, 1100, 880), title='Bill map.xlsx', formula=('C2', 'Paycheck A'), cols=[('Bill', 3), ('Due', 1.4), ('Pay from', 2.2)], rows=[
                 dict(cells=['Rent', '1st', 'Paycheck A'], at='m3+1.4'), dict(cells=['Utilities', '5th', 'Paycheck A'], at='m3+3.0'),
                 dict(cells=['Car payment', '15th', 'Paycheck B'], at='m3+5.4'), dict(cells=['Phone', '20th', 'Paycheck B'], at='m3+6.8'), dict(cells=['Insurance', '28th', 'Paycheck B'], at='m3+7.8')]),
             E('callout', 'm4+0.8', region=(1200, 380, 1780, 780), lines=['Awkward due date?', 'Ask to move it.'], size=52, color=GOLD)]),
    dict(id='planC', header=dict(tag='STRATEGY 3', title='Split the 50/30/20 by paycheck', color=GOLD), segs=[
        ('c1', "Strategy three: run the fifty, thirty, twenty rule on every paycheck.", None),
        ('c2', "On fourteen hundred dollars, that's seven hundred for needs, four twenty for wants, and two eighty for savings and debt.", None),
        ('c3', "It's simple, it's automatic, and it works no matter which week the paycheck lands.", None)],
        els=[E('donut', 'c1+0.6', region=(140, 320, 1780, 940), center=('$1,400', 64, 'per paycheck'), items=[
                 dict(label='Needs', frac=.5, color=BLUE, display='$700', at='c2+1.0'), dict(label='Wants', frac=.3, color=GOLD, display='$420', at='c2+3.8'), dict(label='Savings & debt', frac=.2, color=GREEN, display='$280', at='c2+6.4')])]),
    dict(id='accounts', header=dict(tag='AUTOMATE', title='Give each paycheck a route', color=GREEN), segs=[
        ('o1', "Now let's automate it, so you don't have to remember.", None),
        ('o2', "Open a separate bills account. Each payday, move that paycheck's share of the bills into it.", None),
        ('o3', "Send your savings the same day. What's left in checking is your spending money, and it's safe to spend.", None)],
        els=[E('flow', 'o1+1.0', region=(140, 320, 1780, 940), dotcolor=GREEN, nodes=[
                 dict(id='p', x=140, y=520, w=420, h=200, title='Paycheck', sub='payday', color=GOLD, icon='check', subsize=44, at='o2+0.4'),
                 dict(id='a', x=760, y=340, w=700, h=170, title='Bills account', sub='bills covered', color=BLUE, icon='house', subsize=40, at='o2+3.0'),
                 dict(id='b', x=760, y=550, w=700, h=170, title='Savings', sub='moved same day', color=GREEN, icon='piggy', subsize=40, at='o3+0.6'),
                 dict(id='c', x=760, y=760, w=700, h=170, title='Checking = spending', sub='safe to spend', color=GOLD, icon='cart', subsize=40, at='o3+3.0')],
               arrows=[('p', 'a', 'o2+2.6'), ('p', 'b', 'o3+0.2'), ('p', 'c', 'o3+2.6')])]),
    dict(id='routine', header=dict(tag='PAYDAY ROUTINE', title='Your five-minute payday routine', color=GOLD), segs=[
        ('y1', "Let's turn all of this into a five-minute payday routine.", None),
        ('y2', "One: move this paycheck's share of the bills into your bills account.", None),
        ('y3', "Two: send your savings and your debt payment the same day.", None),
        ('y4', "Three: check which bills are due before your next payday.", None),
        ('y5', "Four: glance at what you spent last pay period. Then you're done, until the next payday.", None)],
        els=[E('checklist', 'y2', region=(260, 340, 1660, 940), size=40, items=[
                 dict(text='1. Move the bills share', at='y2+0.4', color=GOLD), dict(text='2. Savings + debt payment, same day', at='y3+0.4', color=GOLD),
                 dict(text='3. Check bills due before next payday', at='y4+0.4', color=GOLD), dict(text='4. Glance at last pay period', at='y5+0.4', color=GOLD)])]),
    dict(id='coaster', dur=7.0, mood='tension', bg=dict(kind='soft'), els=[
        E('montage', 0.2, clips=['coaster_2', 'money_0', 'desk_0', 'freelance_1'], words=['THE ROLLER COASTER', 'BIG MONTH', 'SLOW MONTH', 'LATE PAYMENT'], step=1.75, label='IRREGULAR INCOME')],
        sfx=[(0.2, 'thud'), (1.95, 'thud'), (3.7, 'thud'), (5.45, 'thud')]),
    dict(id='irregular', header=dict(tag='IRREGULAR', title='Pay yourself a steady salary', color=CORAL), segs=[
        ('i1', "Now, irregular income. Never budget off your best month.", None),
        ('i2', "Look at the last six to twelve months, and build your budget around a conservative number, not your highest one.", None),
        ('i3', "Then pay yourself a salary. All income lands in one account, and you pay yourself the same amount every month.", None),
        ('i4', "Say your income swings between nineteen hundred and forty-two hundred dollars, averaging three thousand. You pay yourself twenty-eight hundred, with a starter buffer of one thousand.", None),
        ('i5', "Slow months dip into the buffer. Good months refill it. In this example, the buffer never drops below six hundred dollars, and ends the year at thirty-four hundred.", None)],
        els=[E('line', 'i4+1.0', region=(140, 310, 1780, 940), dur=11.0, ymax=4500, ystep=1500, rightpad=360,
               xlabels=[(0, 'Jan'), (3, 'Apr'), (6, 'Jul'), (9, 'Oct'), (11, 'Dec')], series=[
                   dict(name='income', color=CORAL, values=INCOME, width=7),
                   dict(name='salary', color=GREEN, values=[2800] * 12, width=7, endlabel='$2,800', endsub='your salary'),
                   dict(name='buffer', color=BLUE, values=BUFFER, width=7, endlabel='$3,400', endsub='buffer, Dec')],
               markers=[dict(x=2, series=0, label='slow month', at='i5+1.0', dx=110, dy=60, color=CORAL), dict(x=4, series=0, label='great month', at='i5+4.0', dx=-130, dy=-70, color=CORAL)]),
             E('callout', 'i1+0.8', until='i4', region=(300, 340, 1620, 820), lines=['Budget off a conservative number', 'not your best month'], size=62, color=CORAL, fg=WHITE)]),
    dict(id='buffer', header=dict(tag='BUILD IT', title='Start a buffer from zero', color=BLUE), segs=[
        ('u1', "How do you build that starter buffer?", None),
        ('u2', "Use your bonus paychecks, or your best month of the year, and leave that money in the buffer instead of spending it.", None),
        ('u3', "Aim first for one month of essential expenses. Then keep growing it toward three.", None),
        ('u4', "Once it's full, your slow months stop being scary.", None)],
        els=[E('steps', 'u1+0.8', region=(140, 360, 1780, 640), items=[
                 dict(title='1. Seed it', sub='Bonus check or best month', color=GOLD, at='u2+2.0'), dict(title='2. One month', sub='Of essential expenses', color=GREEN, at='u3+0.6'),
                 dict(title='3. Three months', sub='Slow months stop being scary', color=BLUE, at='u3+4.2')]),
             E('callout', 'u4+0.4', region=(140, 720, 1780, 930), lines=['A full buffer = calm slow months'], size=60, color=GREEN, fg=WHITE)]),
    dict(id='sinking', header=dict(tag='SINKING FUNDS', title='Divide big bills by twelve', color=GOLD), segs=[
        ('s1', "Irregular costs need a plan too. Annual insurance, holiday gifts, car maintenance.", None),
        ('s2', "Take each yearly cost and divide it by twelve. Six hundred dollars of insurance is fifty a month. Four eighty of gifts is forty. Nine hundred for the car is seventy-five.", None),
        ('s3', "Together, that's one hundred sixty-five dollars a month in sinking funds, so those bills never ambush you.", None)],
        els=[E('bars', 's2+0.6', region=(140, 330, 1300, 740), labelw=380, max=75, items=[
                 dict(label='Insurance ($600/yr)', value=50, color=BLUE, icon='shield', display='$50/mo', at='s2+3.4'), dict(label='Gifts ($480/yr)', value=40, color=GOLD, icon='star', display='$40/mo', at='s2+7.2'),
                 dict(label='Car ($900/yr)', value=75, color=GREEN, icon='car', display='$75/mo', at='s2+10.6')]),
             E('counter', 's3+0.8', region=(140, 760, 1780, 960), label='SINKING FUNDS', to=165, size=96, color=GREEN, dur=1.4, note='per month')]),
    dict(id='taxes', header=dict(tag='SELF-EMPLOYED?', title='Set money aside for taxes', color=BLUE), segs=[
        ('x1', "If you're self-employed, there's one more step: taxes.", None),
        ('x2', "Nobody withholds them for you. So from every payment, move a portion into a separate tax account before you touch it.", None),
        ('x3', "How much depends on where you live and your situation, so ask a tax professional for your number.", None)],
        els=[E('flow', 'x1+0.8', region=(140, 320, 1780, 900), dotcolor=BLUE, nodes=[
                 dict(id='p', x=140, y=520, w=440, h=200, title='Client pays you', sub='income in', color=GOLD, icon='check', subsize=44, at='x1+1.2'),
                 dict(id='a', x=780, y=340, w=740, h=170, title='Tax account', sub='ask a tax pro how much', color=BLUE, icon='shield', subsize=36, at='x2+2.0'),
                 dict(id='b', x=780, y=550, w=740, h=170, title='Buffer', sub='fills in good months', color=GREEN, icon='piggy', subsize=36, at='x2+6.0'),
                 dict(id='c', x=780, y=760, w=740, h=170, title='Your salary', sub='the same every month', color=GOLD, icon='cart', subsize=36, at='x3+0.4')],
               arrows=[('p', 'a', 'x2+1.6'), ('p', 'b', 'x2+5.6'), ('p', 'c', 'x3+0.0')])]),
    dict(id='qa', header=dict(tag='QUESTIONS', title='Common questions', color=GOLD), segs=[
        ('q1', "A few common questions.", None),
        ('q2', "Can I spend any of the bonus paychecks? Sure, if your goals are on track. Many people split it: most to goals, a little for fun.", None),
        ('q3', "What if I have two jobs, or a side hustle? Put it all in one budget, and base your fixed bills on the steadier income.", None),
        ('q4', "And what if my pay changes mid-year? Update your numbers right away. A budget is a living document, not a contract.", None)],
        els=[E('cards', 'q2', region=(140, 330, 1780, 800), items=[
                 dict(icon='star', title='Spend the bonus?', color=GOLD, at='q2+0.4', body=['If goals are on track, split it: most to goals, a little for fun.']),
                 dict(icon='bolt', title='Two jobs?', color=BLUE, at='q3+0.4', body=['One budget. Base fixed bills on the steadier income.']),
                 dict(icon='check', title='Pay changed?', color=GREEN, at='q4+0.4', body=['Update your numbers right away. A budget is a living document.'])])]),
    dict(id='mistakes', header=dict(tag='AVOID', title='Four paycheck-planning mistakes', color=CORAL), segs=[
        ('e1', "Four mistakes to avoid.", None),
        ('e2', "One: spending the third paycheck without a plan.", None),
        ('e3', "Two: budgeting off your best month when your income is irregular.", None),
        ('e4', "Three: having no buffer, so every slow month becomes a crisis.", None),
        ('e5', "And four: ignoring due dates, which leads to late fees. A bill map fixes that.", None)],
        els=[E('bullets', 'e2', region=(200, 330, 1720, 940), size=40, items=[
                 dict(text='Spending the third paycheck', sub='Give it a job first', icon='x', color=CORAL, at='e2+0.3'), dict(text='Budgeting off your best month', sub='Use a conservative number', icon='x', color=CORAL, at='e3+0.3'),
                 dict(text='No buffer', sub='Slow months become crises', icon='x', color=CORAL, at='e4+0.3'), dict(text='Ignoring due dates', sub='A bill map prevents late fees', icon='x', color=CORAL, at='e5+0.3')])]),
    dict(id='outro', theme='night', bg=dict(kind='footage', clip='planner_1', dim=.6), segs=[
        ('f1', "Let's recap.", None),
        ('f2', "Biweekly means twenty-six paychecks. Budget on two a month, and give the extra checks a job.", None),
        ('f3', "Make a bill map, and automate each payday.", None),
        ('f4', "With irregular income, pay yourself a steady salary from a buffer, and set aside money for annual bills and taxes.", None),
        ('f4b', "Remember: the best budget is the one that matches how you actually get paid.", None),
        ('f5', "If this helped, subscribe, and tell me in the comments: how often do you get paid?", None),
        ('f6', "And if you learned something from this video, don't forget to watch our next video.", None),
        ('f7', "This video is for education only and isn't financial advice. See you next time.", None)],
        els=[E('bullets', 'f1', until='f5', region=(220, 300, 1700, 860), size=40, items=[
                 dict(text='26 paychecks: budget on two a month', icon='check', color=GREEN, at='f2'), dict(text='Bill map + automation', icon='check', color=BLUE, at='f3'),
                 dict(text='Irregular? Salary + buffer + tax account', icon='check', color=GOLD, at='f4')]),
             E('callout', 'f4b+0.2', until='f5', region=(220, 740, 1700, 900), lines=['Match the budget to how you get paid'], size=46, color=GOLD),
             E('cta', 'f5+0.5', question='How often do you get paid?', next='Watch the Budgeting Basics playlist'),
             E('title', 'f7', region=(140, 900, 1780, 970), lines=[('For educational purposes only. Not financial advice. Examples are illustrative. Footage: Pixabay.', 26, GREY, 'Medium')])]),
]
