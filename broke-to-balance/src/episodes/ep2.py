"""Episode 2 - Emergency Fund. Style: calm, reassuring 'safety net' (deep teal night, soft pill headers, gentle fades)."""
from lib import *
from engine import E

META = dict(final='Broke_to_Balance_Ep2_Emergency_Fund.mp4', music=2, voice_speed=0.97, gfx_speed=1.45, bg_speed=1.5,
            thumb=dict(lines=[('HOW MUCH', 150, WHITE), ('EMERGENCY', 112, GOLD), ('FUND?', 150, GREEN)], accent=GREEN, icon='shield', tag='3-6 MONTHS?', y0=300))
STYLE = dict(theme='night', header='pill', bg=dict(kind='soft', c1=(6, 26, 46), c2=(8, 62, 74), accent=GREEN, k=5),
             trans=['fade', 'slide', 'fade', 'zoom', 'fade', 'slide', 'fade', 'zoom', 'fade', 'slide'])

mo = [600 * i for i in range(16)]
SPEC = [
    dict(id='hook', bg=dict(kind='city'), segs=[
        ('h1', "Your car breaks down on Monday. Your phone screen cracks on Tuesday. And on Wednesday, the rent is due.", None),
        ('h2', "If one surprise bill can wreck your month, you don't have a spending problem. You have a cushion problem.", None),
        ('h3', "In this video, you'll learn exactly how big your emergency fund should be, where to keep it, and how to build it, even on a tight budget.", None)],
        els=[E('bars', 'h1', until='h3', region=(140, 320, 1170, 700), labelw=330, size=32, max=1000, items=[
                 dict(label='Car repair', value=650, color=CORAL, icon='car', at='h1+0.9'), dict(label='Cracked phone', value=180, color=GOLD, icon='bolt', at='h1+2.7'),
                 dict(label='Rent due', value=1000, color=BLUE, icon='house', at='h1+4.5')]),
             E('counter', 'h1+0.4', until='h3', region=(1330, 320, 1780, 700), label='YOUR SAVINGS', text='$0', color=CORAL, size=130, dur=0, note='Example amounts'),
             E('callout', 'h2+1.2', until='h3', region=(140, 740, 1780, 940), lines=['Not a spending problem. A cushion problem.'], size=52, color=GOLD),
             E('bullets', 'h3', region=(300, 330, 1620, 900), size=50, items=[
                 dict(text='How big it should be', icon='star', color=GREEN, at='h3+0.6'), dict(text='Where to keep it', icon='shield', color=BLUE, at='h3+2.6'),
                 dict(text='How to build it', icon='piggy', color=GOLD, at='h3+4.4')])]),
    dict(id='title', bg=dict(kind='rain', accent=GREEN, k=2), segs=[
        ('t1', "Welcome back to Broke to Balance. I'm glad you're here.", None), ('t2', "Let's build your safety net.", None),
        ('t3', "Quick note: this is educational, not personal financial advice. Let's get into it.", None)],
        els=[E('brand', 't1', sub_at='t2', pill='Emergency Fund: How Much Do You Really Need?', line='EPISODE 2  •  BUDGETING BASICS')]),
    dict(id='what', header=dict(tag='WHAT IT IS', title='Your safety net', color=GREEN), segs=[
        ('w1', "An emergency fund is money set aside for true surprises, and nothing else.", None),
        ('w2', "It's not a vacation fund. It's not a new phone fund. It's your protection against job loss, medical bills, and urgent car or home repairs.", None),
        ('w3', "Without one, a surprise bill goes on a credit card. And that's how a one-time problem turns into months of interest.", None),
        ('w4', "With one, a surprise is just an annoying afternoon.", None)],
        els=[E('compare', 'w1+1.5', until='w3', region=(140, 310, 1780, 930),
               left=dict(at='w2+4.2', title="IS an emergency", color=GREEN, icon='shield', lines=['Job loss', 'A medical bill', 'Urgent car or home repair', 'Emergency travel']),
               right=dict(at='w2+0.2', title="ISN'T an emergency", color=CORAL, icon='x', lines=['A big sale', 'A vacation', 'A phone upgrade', 'Gift shopping'], bullet='x')),
             E('flow', 'w3', until='w4', dotcolor=CORAL, nodes=[
                 dict(id='a', x=160, y=420, w=500, h=190, title='Surprise bill', sub='$800', color=CORAL, icon='bolt', at='w3'),
                 dict(id='b', x=710, y=420, w=500, h=190, title='Credit card', sub='borrowed', color=GOLD, icon='cart', at='w3+2.0'),
                 dict(id='c', x=1260, y=420, w=500, h=190, title='Months of interest', sub='ugh', color=CORAL, icon='x', at='w3+4.0')],
               arrows=[('a', 'b', 'w3+1.6'), ('b', 'c', 'w3+3.6')]),
             E('flow', 'w4', dotcolor=GREEN, nodes=[
                 dict(id='a', x=160, y=420, w=500, h=190, title='Surprise bill', sub='$800', color=CORAL, icon='bolt', at='w4'),
                 dict(id='b', x=710, y=420, w=500, h=190, title='Emergency fund', sub='covers it', color=GREEN, icon='shield', at='w4+0.8'),
                 dict(id='c', x=1260, y=420, w=500, h=190, title='Problem solved', sub='back to normal', color=GREEN, icon='check', at='w4+1.6')],
               arrows=[('a', 'b', 'w4+0.6'), ('b', 'c', 'w4+1.4')])]),
    dict(id='example', header=dict(tag='REAL LIFE', title='Same surprise, different outcome', color=GOLD), segs=[
        ('x1', "Let's make this real with two people facing the same eight hundred dollar surprise.", None),
        ('x2', "Alex has no emergency fund, so the bill goes on a credit card at twenty-four percent A P R.", "Alex has no emergency fund, so the bill goes on a credit card at 24% APR."),
        ('x3', "Paying fifty dollars a month, it takes about twenty months to clear, and costs roughly one hundred seventy-four dollars in interest.", None),
        ('x4', "Sam has a starter fund. Sam pays the bill from savings, then pauses wants spending and refills the account within two months, with no interest at all.", None),
        ('x5', "Same surprise, completely different outcome. That's what a cushion buys you: not wealth, but calm.", None)],
        els=[E('compare', 'x1+1.0', region=(140, 310, 1780, 850),
               left=dict(at='x2', title='Alex: no fund', color=CORAL, icon='x', bullet='x', lines=[dict(text='$800 bill goes on a card', at='x2+1.0'), dict(text='24% APR', at='x2+3.2'),
                         dict(text='$50 a month for ~20 months', at='x3+0.6'), dict(text='~$174 in interest', at='x3+4.4')]),
               right=dict(at='x4', title='Sam: starter fund', color=GREEN, icon='shield', bullet='check', lines=[dict(text='Pays the $800 from savings', at='x4+0.6'), dict(text='Pauses wants spending', at='x4+3.4'),
                         dict(text='Refilled within 2 months', at='x4+5.6'), dict(text='$0 in interest', at='x4+8.0')])),
             E('callout', 'x5+0.8', region=(140, 870, 1780, 970), lines=['A cushion buys you calm'], size=52, color=GOLD)]),
    dict(id='starter', header=dict(tag='STEP 1', title='Start with a starter fund', color=GREEN), segs=[
        ('s1', "Step one is a starter emergency fund.", None),
        ('s2', "A common goal is five hundred to one thousand dollars. That covers many everyday surprises, like a tire, a copay, or a broken laptop.", None),
        ('s3', "Start here before anything else, even before aggressive debt payoff, because it stops new debt from piling up.", None),
        ('s4', "At six hundred dollars a month from your twenty percent bucket, a one thousand dollar starter fund takes less than two months.", None)],
        els=[E('gauge', 's1', region=(140, 300, 900, 940), frac=1.0, color=GREEN, valtext='$1,000', size=96, label='starter goal', dur=2.0),
             E('bullets', 's2+1.5', until='s3', region=(1000, 340, 1780, 800), size=38, items=[
                 dict(text='A flat tire', icon='car', color=BLUE, at='s2+6.4'), dict(text='A doctor copay', icon='shield', color=GREEN, at='s2+7.8'),
                 dict(text='A broken laptop', icon='bolt', color=GOLD, at='s2+9.0')]),
             E('callout', 's3+0.4', until='s4', region=(1000, 400, 1780, 800), lines=['Starter fund first', 'Stops new debt'], size=56, color=GOLD),
             E('columns', 's4+0.5', region=(1000, 330, 1780, 930), max=1000, items=[
                 dict(label='Month 1', value=600, color=GREEN, at='s4+3.0'), dict(label='Month 2', value=1000, color=GOLD, display='$1,000 ✓', at='s4+5.0')])]),
    dict(id='full', header=dict(tag='STEP 2', title='Build a full emergency fund', color=BLUE), segs=[
        ('f1', "Step two is a full emergency fund: three to six months of essential expenses.", None),
        ('f2', "Notice the word essential. We're counting only the bills you must pay to stay housed, fed, and working.", None),
        ('f3', "Let's use our example from the fifty, thirty, twenty video. Rent, one thousand dollars. Groceries, two fifty. Utilities, one hundred. Transportation, one hundred. Insurance and minimum payments, fifty.", None),
        ('f4', "That's fifteen hundred dollars a month.", None),
        ('f5', "Three months is forty-five hundred dollars. Six months is nine thousand.", None)],
        els=[E('callout', 'f1+0.6', until='f3', region=(140, 300, 1780, 700), lines=['3 to 6 months', 'of ESSENTIAL expenses'], size=84, color=BLUE, fg=WHITE),
             E('table', 'f3', region=(140, 310, 1060, 840), title='Essential Expenses.xlsx', formula=('B7', '=SUM(B2:B6)'), cols=[('Essential bill', 3), ('Monthly', 2)], rows=[
                 dict(cells=['Rent', '1,000'], at='f3+4.0'), dict(cells=['Groceries', '250'], at='f3+6.0'), dict(cells=['Utilities', '100'], at='f3+7.8'),
                 dict(cells=['Transportation', '100'], at='f3+9.4'), dict(cells=['Insurance & minimums', '50'], at='f3+11.2'),
                 dict(cells=['TOTAL / MONTH', '1,500'], at='f4', style='total')]),
             E('counter', 'f4', until='f5', region=(1150, 330, 1780, 760), label='ESSENTIALS', to=1500, size=120, color=GREEN, dur=1.2, note='per month'),
             E('columns', 'f5', region=(1150, 310, 1780, 930), max=9000, items=[
                 dict(label='3 months', value=4500, color=BLUE, at='f5+0.6'), dict(label='6 months', value=9000, color=GOLD, at='f5+2.4')])]),
    dict(id='howmuch', header=dict(tag='HOW MUCH?', title='Three months... or six?', color=GOLD), segs=[
        ('c1', "So should you aim for three months or six, or more?", None),
        ('c2', "Lean toward three months if you have stable income, a second earner, and few dependents.", None),
        ('c3', "Lean toward six months or more if your income is irregular, you're self-employed, you're the only earner, or you work in a volatile industry.", None),
        ('c4', "There's no perfect number. Pick a target you can actually reach, and adjust it as your life changes.", None)],
        els=[E('compare', 'c1+1.0', region=(140, 310, 1780, 790),
               left=dict(at='c2', title='Lean toward 3 months', color=BLUE, icon='shield', lines=['Stable income', 'A second earner', 'Few dependents']),
               right=dict(at='c3', title='Lean toward 6+ months', color=GOLD, icon='star', lines=['Irregular income', 'Self-employed', 'The only earner', 'Volatile industry'], step=84)),
             E('callout', 'c4+0.3', region=(140, 810, 1780, 960), lines=['Pick a target you can actually reach'], size=48, color=GREEN)]),
    dict(id='where', header=dict(tag='WHERE', title='Where to keep it', color=BLUE), segs=[
        ('wh1', "Where should you keep this money?", None),
        ('wh2', "Somewhere safe, separate, and easy to reach, but not too easy.", None),
        ('wh3', "A high-yield savings account at an insured bank or credit union is a popular choice. It's separate from your checking, so you won't spend it by accident, and it usually pays more interest than a standard account.", None),
        ('wh4', "Check that deposits are insured where you live. In the U.S., the FDIC and NCUA typically cover up to two hundred fifty thousand dollars per depositor, per institution, per ownership category.", None),
        ('wh5', "Rates change, so compare current offers, and skip accounts with monthly fees.", None),
        ('wh6', "What you shouldn't do is keep your emergency fund in the stock market, or in something you can't reach within a few days. Emergencies don't wait for markets to recover.", None)],
        els=[E('checklist', 'wh2', region=(140, 310, 1060, 930), size=34, items=[
                 dict(text='Safe & insured', at='wh2+0.2'), dict(text='Easy to reach', at='wh2+2.2'), dict(text='Separate from checking', at='wh3+5.0'),
                 dict(text='Pays more interest', at='wh3+8.0'), dict(text='No monthly fees', at='wh5+2.2')]),
             E('callout', 'wh4+0.3', region=(1120, 300, 1780, 640), lines=['Deposit insurance', 'U.S.: up to $250,000', 'per depositor, per institution'], size=36, color=BLUE, fg=WHITE),
             E('checklist', 'wh6+0.5', region=(1120, 680, 1780, 930), size=30, items=[
                 dict(text='Stock market', ok=False, at='wh6+2.4'), dict(text='Locked-up accounts', ok=False, at='wh6+5.0')])]),
    dict(id='build', header=dict(tag='BUILD IT', title='How to build it', color=GREEN), segs=[
        ('b1', "Now, how do you build it?", None),
        ('b2', "First, open a separate account and name it Emergency Fund. A name makes it harder to raid.", None),
        ('b3', "Second, automate it. Set a transfer for payday, just like the pay-yourself-first tip from our budgeting video.", None),
        ('b4', "Third, feed it with extra money: tax refunds, bonuses, side income, or the savings from a cancelled subscription.", None),
        ('b5', "Here's the timeline if you save six hundred dollars a month, before any interest. The starter fund is done in two months. A three-month fund of forty-five hundred dollars takes about eight months. And the full six-month fund of nine thousand dollars takes fifteen months.", None)],
        els=[E('steps', 'b2', until='b5', region=(140, 360, 1780, 640), items=[
                 dict(title='1. Open it', sub='A separate account named Emergency Fund', color=GREEN, at='b2+0.4'),
                 dict(title='2. Automate it', sub='A transfer on payday, before you can spend it', color=GOLD, at='b3+0.4'),
                 dict(title='3. Feed it', sub='Refunds, bonuses, side income, cancelled subscriptions', color=BLUE, at='b4+0.4')]),
             E('line', 'b5', region=(140, 300, 1780, 940), dur=12.0, ymax=9000, ystep=3000, rightpad=140,
               xlabels=[(0, 'Start'), (5, 'Month 5'), (10, 'Month 10'), (15, 'Month 15')],
               series=[dict(name='saved', color=GREEN, values=mo)],
               markers=[dict(x=2, label='Starter fund ✓', at='b5+6.0', dx=140, dy=-80, color=GOLD), dict(x=8, label='3-month fund', at='b5+10.0', dx=-170, dy=-80, color=BLUE),
                        dict(x=15, label='6-month fund', at='b5+14.5', dx=-170, dy=-80, color=GREEN)])]),
    dict(id='rules', header=dict(tag='RULES', title='Three rules for using it', color=GOLD), segs=[
        ('u1', "Once it exists, you need a few rules.", None),
        ('u2', "Rule one: ask whether it's unexpected, necessary, and urgent. If it isn't all three, it isn't an emergency.", None),
        ('u3', "Rule two: if you use it, don't feel guilty. That's exactly what it's for.", None),
        ('u4', "Rule three: refill it. Pause your wants spending for a month or two, and rebuild.", None)],
        els=[E('cards', 'u2', region=(140, 330, 1780, 900), items=[
                 dict(icon='shield', big='1', title='Real emergency?', color=GREEN, at='u2', body=['Unexpected, necessary, and urgent. If it fails any of the three, it is not an emergency.']),
                 dict(icon='check', big='2', title='Use it, no guilt', color=BLUE, at='u3', body=['Using it means it worked. That is exactly what it is for.']),
                 dict(icon='piggy', big='3', title='Refill it', color=GOLD, at='u4', body=['Pause wants spending for a month or two and rebuild the cushion.'])])]),
    dict(id='faq', header=dict(tag='QUESTIONS', title='Debt first, or fund first?', color=BLUE), segs=[
        ('q1', "People always ask: should I pay off debt first, or build the emergency fund?", None),
        ('q2', "A popular approach is to build the small starter fund first, then attack high-interest debt, then grow your fund to three to six months.", None),
        ('q3', "Why? Because with no cushion at all, the next surprise just lands on the card again, and you're back where you started.", None),
        ('q4', "Another question: what about irregular costs, like annual insurance or holiday gifts? Those aren't emergencies, they're predictable. Give them their own sinking fund, a little set aside each month.", None),
        ('q5', "And if you're self-employed, aim for the higher end of the range, because your income can swing.", None)],
        els=[E('steps', 'q2', until='q4', region=(140, 360, 1780, 640), items=[
                 dict(title='1. Starter fund', sub='$500 to $1,000 first', color=GREEN, at='q2+3.2'), dict(title='2. High-interest debt', sub='Pay it down hard', color=CORAL, at='q2+5.6'),
                 dict(title='3. Full fund', sub='Grow to 3-6 months', color=BLUE, at='q2+8.2')]),
             E('callout', 'q3+1.0', until='q4', region=(140, 700, 1780, 930), lines=['No cushion = the next surprise', 'lands on the card again'], size=48, color=GOLD),
             E('cards', 'q4+4.0', region=(140, 330, 1780, 800), items=[
                 dict(icon='house', title='Annual insurance', color=BLUE, at='q4+4.0', body=['Predictable. Divide it by 12 and save monthly.']),
                 dict(icon='star', title='Holiday gifts', color=GOLD, at='q4+6.0', body=['Not an emergency. Give it its own sinking fund.']),
                 dict(icon='car', title='Car maintenance', color=GREEN, at='q4+8.0', body=['It will happen eventually. Save a little each month.'])]),
             E('callout', 'q5+0.6', region=(140, 830, 1780, 960), lines=['Self-employed? Aim for the higher end'], size=44, color=BLUE, fg=WHITE)]),
    dict(id='mistakes', header=dict(tag='AVOID', title='Four common mistakes', color=CORAL), segs=[
        ('m1', "Before we wrap up, four common mistakes.", None),
        ('m2', "One: leaving it in your everyday checking account, where it quietly gets spent.", None),
        ('m3', "Two: investing it in the stock market, where it could be down exactly when you need it.", None),
        ('m4', "Three: using it and never refilling it.", None),
        ('m5', "And four: waiting for the perfect number before starting. Even fifty dollars a week is a real start.", None)],
        els=[E('bullets', 'm2', region=(200, 320, 1720, 930), size=40, items=[
                 dict(text='Leaving it in everyday checking', icon='x', color=CORAL, at='m2'), dict(text='Investing it in the stock market', icon='x', color=CORAL, at='m3'),
                 dict(text='Using it and never refilling', icon='x', color=CORAL, at='m4'), dict(text='Waiting for a "perfect" number', icon='x', color=CORAL, at='m5')])]),
    dict(id='outro', bg=dict(kind='rain', accent=GREEN, k=8), segs=[
        ('r1', "Let's recap.", None),
        ('r2', "Start with a starter fund of five hundred to one thousand dollars.", None),
        ('r3', "Grow it to three to six months of essential expenses.", None),
        ('r4', "Keep it in a separate, insured, easy-to-reach account, and automate your deposits.", None),
        ('r4b', "And remember, even a small start beats waiting for a perfect plan.", None),
        ('r5', "In the next video, we'll tackle the other side of the equation: how to stop overspending with a simple thirty-minute money audit.", None),
        ('r6', "If this helped, subscribe, and tell me in the comments: what's your emergency fund goal?", None),
        ('r7', "This video is for education only and isn't financial advice. See you next time.", None)],
        els=[E('bullets', 'r1', until='r5', region=(220, 300, 1700, 860), size=46, items=[
                 dict(text='Starter fund: $500-$1,000', icon='piggy', color=GREEN, at='r2'), dict(text='Full fund: 3-6 months of essentials', icon='shield', color=BLUE, at='r3'),
                 dict(text='Separate, insured, automated', icon='check', color=GOLD, at='r4')]),
             E('callout', 'r4b+0.2', until='r5', region=(220, 760, 1700, 900), lines=['A small start beats a perfect plan'], size=48, color=GOLD),
             E('cta', 'r5+4.0', question="What's your emergency fund goal?", next='Stop Overspending: The 30-Minute Money Audit'),
             E('title', 'r7', region=(140, 900, 1780, 970), lines=[('For educational purposes only. Not financial advice. Examples are illustrative.', 26, GREY, 'Medium')])]),
]
