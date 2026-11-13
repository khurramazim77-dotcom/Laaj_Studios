import json
DEBTS = [dict(name='Store card', bal=800.0, apr=.12, minp=25.0), dict(name='Credit card', bal=5000.0, apr=.24, minp=125.0), dict(name='Personal loan', bal=2500.0, apr=.15, minp=80.0)]
EXTRA = 300.0

def sim(order_key, extra=EXTRA, debts=DEBTS, only_min=False):
    ds = [dict(d) for d in debts]; budget = sum(d['minp'] for d in ds) + (0 if only_min else extra)
    m = 0; cum = 0.0; bal_series = [sum(d['bal'] for d in ds)]; int_series = [0.0]; paid_off = {}
    while any(d['bal'] > 0.005 for d in ds) and m < 600:
        m += 1
        for d in ds:
            if d['bal'] > 0:
                i = d['bal'] * d['apr'] / 12; d['bal'] += i; cum += i
        avail = budget
        for d in ds:                      # minimums first
            if d['bal'] > 0:
                p = min(d['minp'], d['bal']); d['bal'] -= p; avail -= p
        for d in sorted([x for x in ds if x['bal'] > 0.005], key=order_key):   # everything else to the target
            p = min(avail, d['bal']); d['bal'] -= p; avail -= p
        for d in ds:
            if d['bal'] <= 0.005 and d['name'] not in paid_off:
                paid_off[d['name']] = m; d['bal'] = 0.0
        bal_series.append(sum(d['bal'] for d in ds)); int_series.append(cum)
    return dict(months=m, interest=cum, bal=bal_series, ints=int_series, paid=paid_off)

snow = sim(lambda d: d['bal']); aval = sim(lambda d: -d['apr']); mins = sim(lambda d: -d['apr'], only_min=True)
if __name__ == '__main__':
    for n, r in (('snowball', snow), ('avalanche', aval), ('minimums only', mins)):
        print(n, r['months'], round(r['interest'], 2), r['paid'])
    print('savings avalanche vs snowball', round(snow['interest'] - aval['interest'], 2), 'months diff', snow['months'] - aval['months'])
    d = [dict(x) for x in DEBTS if x['name'] == 'Credit card']
    print('single card min only', sim(lambda x: x['bal'], debts=d, only_min=True)['months'], round(sim(lambda x: x['bal'], debts=d, only_min=True)['interest'], 2))
