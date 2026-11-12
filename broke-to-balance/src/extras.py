import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import DoughnutChart, Reference
from openpyxl.formatting.rule import CellIsRule
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

wb = Workbook(); ws = wb.active; ws.title = '50-30-20 Budget'
H = Font(bold=True, color='FFFFFF'); navy = PatternFill('solid', fgColor='0B1F3A')
inp = PatternFill('solid', fgColor='FFF4CC'); thin = Side(style='thin', color='D0D7E2')
box = Border(left=thin, right=thin, top=thin, bottom=thin)
ws['A1'] = 'Broke to Balance — 50/30/20 Budget Template'; ws['A1'].font = Font(bold=True, size=16, color='0B1F3A')
ws['A2'] = 'Yellow cells are inputs. Everything else calculates automatically. Example numbers are illustrative.'; ws['A2'].font = Font(italic=True, color='667085')
ws['A4'] = 'Monthly take-home pay (after taxes)'; ws['B4'] = 3000; ws['B4'].fill = inp; ws['A4'].font = Font(bold=True)
ws['A6'] = 'Bucket'; ws['B6'] = 'Target %'; ws['C6'] = 'Target $'; ws['D6'] = 'Planned $'; ws['E6'] = 'Actual % of pay'; ws['F6'] = 'Status'
for c in 'ABCDEF': ws[f'{c}6'].font = H; ws[f'{c}6'].fill = navy; ws[f'{c}6'].alignment = Alignment(horizontal='center')
rows = [('Needs', 0.5), ('Wants', 0.3), ('Savings & debt payoff', 0.2)]
for i, (n, p) in enumerate(rows):
    r = 7 + i
    ws[f'A{r}'] = n; ws[f'B{r}'] = p; ws[f'B{r}'].fill = inp; ws[f'B{r}'].number_format = '0%'
    ws[f'C{r}'] = f'=$B$4*B{r}'; ws[f'C{r}'].number_format = '$#,##0'
ws['A10'] = 'Total'; ws['B10'] = '=SUM(B7:B9)'; ws['B10'].number_format = '0%'; ws['C10'] = '=SUM(C7:C9)'; ws['C10'].number_format = '$#,##0'
ws['D7'] = "=SUM('Details'!B3:B12)"; ws['D8'] = "=SUM('Details'!D3:D12)"; ws['D9'] = "=SUM('Details'!F3:F12)"
for r in (7, 8, 9):
    ws[f'D{r}'].number_format = '$#,##0'; ws[f'E{r}'] = f'=IF($B$4=0,0,D{r}/$B$4)'; ws[f'E{r}'].number_format = '0.0%'
ws['F7'] = '=IF(D7<=C7,"On target","Over - trim")'; ws['F8'] = '=IF(D8<=C8,"On target","Over - trim")'; ws['F9'] = '=IF(D9>=C9,"On target","Under - add more")'
for r in range(6, 11):
    for c in 'ABCDEF': ws[f'{c}{r}'].border = box
for c in 'ABCDEF': ws[f'{c}10'].font = Font(bold=True)
ws['A12'] = 'Tip: use "Pay yourself first" - automate the savings transfer for payday.'; ws['A12'].font = Font(italic=True)
ws['A13'] = 'Educational template only; not financial advice.'; ws['A13'].font = Font(italic=True, color='667085')
ws.column_dimensions['A'].width = 38
for c in 'BCDEF': ws.column_dimensions[c].width = 18
ws.conditional_formatting.add('F7:F9', CellIsRule(operator='equal', formula=['"On target"'], font=Font(color='0E8C58', bold=True)))
ws.conditional_formatting.add('F7:F9', CellIsRule(operator='notEqual', formula=['"On target"'], font=Font(color='D92D20', bold=True)))
ch = DoughnutChart(); ch.title = 'Where your paycheck goes'
ch.add_data(Reference(ws, min_col=3, min_row=6, max_row=9), titles_from_data=True); ch.set_categories(Reference(ws, min_col=1, min_row=7, max_row=9))
ch.height, ch.width = 8, 11; ws.add_chart(ch, 'H4')

d = wb.create_sheet('Details')
d['A1'] = 'Plan your buckets (monthly $)'; d['A1'].font = Font(bold=True, size=14, color='0B1F3A')
for col, t in (('A', 'Need'), ('B', 'Amount'), ('C', 'Want'), ('D', 'Amount'), ('E', 'Savings / debt'), ('F', 'Amount')):
    d[f'{col}2'] = t; d[f'{col}2'].font = H; d[f'{col}2'].fill = navy
needs = [('Rent', 1000), ('Groceries', 250), ('Utilities', 100), ('Transportation', 100), ('Insurance & minimums', 50)]
wants = [('Dining out', 250), ('Shopping', 200), ('Entertainment', 150), ('Travel fund', 140), ('Other fun', 100), ('Subscriptions', 60)]
save = [('Emergency fund', 300), ('High-interest debt', 200), ('Investing', 100)]
for i, (n, a) in enumerate(needs): d[f'A{3+i}'] = n; d[f'B{3+i}'] = a
for i, (n, a) in enumerate(wants): d[f'C{3+i}'] = n; d[f'D{3+i}'] = a
for i, (n, a) in enumerate(save): d[f'E{3+i}'] = n; d[f'F{3+i}'] = a
for r in range(3, 13):
    for c in 'BDF': d[f'{c}{r}'].fill = inp; d[f'{c}{r}'].number_format = '$#,##0'
for c, w in zip('ABCDEF', (26, 12, 20, 12, 22, 12)): d.column_dimensions[c].width = w

g = wb.create_sheet('Savings Growth')
g['A1'] = 'Hypothetical growth of monthly savings'; g['A1'].font = Font(bold=True, size=14, color='0B1F3A')
g['A3'] = 'Monthly savings'; g['B3'] = 600; g['A4'] = 'Assumed annual return'; g['B4'] = 0.07; g['B4'].number_format = '0.0%'
g['A5'] = 'Years'; g['B5'] = 5
for c in ('B3', 'B4', 'B5'): g[c].fill = inp
g['A7'] = 'You put in'; g['B7'] = '=B3*12*B5'; g['A8'] = 'Estimated value'; g['B8'] = '=FV(B4/12,B5*12,-B3)'
g['A9'] = 'Growth'; g['B9'] = '=B8-B7'
for c in ('B3', 'B7', 'B8', 'B9'): g[c].number_format = '$#,##0'
g['A11'] = 'Assumption only - not a guarantee. Investing involves risk.'; g['A11'].font = Font(italic=True, color='667085')
g.column_dimensions['A'].width = 30; g.column_dimensions['B'].width = 16
wb.save(f'{OUT}/Broke_to_Balance_50-30-20_Budget_Template.xlsx')

# thumbnail ------------------------------------------------------------
from lib import *
from PIL import Image
img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
bg_soft(img, 3.0, NAVY, NAVY2, GREEN, 1)
money_rain(img, 9, 16, 5, 0.55)
fade_overlay(img, NAVY, 0.30)
cx, cy, R, r = 1440, 540, 330, 205
cv = Cv((cx - R - 10, cy - R - 10, cx + R + 10, cy + R + 10), s=3)
for a0, fr, col in ((0, .5, NEEDS), (180, .3, WANTS), (288, .2, SAVE)):
    cv.pie((cx - R, cy - R, cx + R, cy + R), a0 - 90 + 1, a0 - 90 + 360 * fr - 1, rgba(col))
cv.d.ellipse(cv.B((cx - r, cy - r, cx + r, cy + r)), fill=(0, 0, 0, 0))
cv.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgba(NAVY))
cv.paste(img)
text(img, (cx, cy - 20), '50/30/20', 74, 'Black', WHITE, 'mm')
text(img, (cx, cy + 62), 'THE RULE', 34, 'Bold', GOLD, 'mm')
text(img, (110, 250), 'STOP BEING', 120, 'Black', WHITE, 'lm')
text(img, (110, 395), 'BROKE', 220, 'Black', CORAL, 'lm')
text(img, (110, 590), 'Budget your paycheck', 70, 'ExtraBold', GREEN, 'lm')
text(img, (110, 680), 'in under 4 minutes', 54, 'Bold', LIGHT, 'lm')
pill(img, 330, 880, 'BROKE → BALANCE', 40, WHITE, NAVY, padx=44, h=84)
img.convert('RGB').resize((1280, 720), Image.LANCZOS).save(f'{OUT}/thumbnail.png')
print('ok')
