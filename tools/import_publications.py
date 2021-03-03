import collections
import unicodedata
import sys
import pandas as pd

fname = sys.argv[1]

def is_japanese(row):
    for c in row['発表者氏名']:
        name = unicodedata.name(c) 
        if "CJK UNIFIED" in name or "HIRAGANA" in name or "KATAKANA" in name:
            return True
    return False
    
def get_date(row):
    return ('{}年{}月'.format(row['発表年月日'].year, row['発表年月日'].month), row['発表年月日'].strftime('%B %Y'))

def build_journal(row):
    date = get_date(row)
    if is_japanese(row):
        md = '{0[発表者氏名]}. {0[発表題名]}. {0[発表先]}, {0[採録情報［誌名、VOL、NO、PP］及び講演区分、等]}, {1}.'.format(row, date[0])
    else:
        md = '{0[発表者氏名]}. {0[発表題名]}. {0[発表先]}, {0[採録情報［誌名、VOL、NO、PP］及び講演区分、等]}, {1}.'.format(row, date[1])
    return 'journal', md

def build_conference(row):
    date = get_date(row)
    if is_japanese(row):
        md = '{0[発表者氏名]}. {0[発表題名]}. {0[発表先]}, {0[採録情報［誌名、VOL、NO、PP］及び講演区分、等]}, {1}.'.format(row, date[0])
    else:
        md = '{0[発表者氏名]}. {0[発表題名]}. {0[発表先]}, {0[採録情報［誌名、VOL、NO、PP］及び講演区分、等]}, {1}.'.format(row, date[1])
    return 'conference', md

def build_editorial(row):
    date = get_date(row)
    if is_japanese(row):
        md = '{0[発表者氏名]}. {0[発表題名]}. {0[発表先]}, {0[採録情報［誌名、VOL、NO、PP］及び講演区分、等]}, {1}.'.format(row, date[0])
    else:
        md = '{0[発表者氏名]}. {0[発表題名]}. {0[発表先]}, {0[採録情報［誌名、VOL、NO、PP］及び講演区分、等]}, {1}.'.format(row, date[1])
    return 'editorial', md

def build_presentation(row):
    date = get_date(row)
    if row['採録情報［誌名、VOL、NO、PP］及び講演区分、等'] in ('招待講演', '基調講演', '依頼講演'):
        if is_japanese(row):
            md = '{0[発表者氏名]}. {0[発表題名]}. {0[発表先]}, {0[開催都市/発表会場]}, {1}.'.format(row, date[0])
        else:
            md = '{0[発表者氏名]}. {0[発表題名]}. {0[発表先]}, {0[開催都市/発表会場]}, {1}.'.format(row, date[1])
        return 'invited', md
    else:
        if is_japanese(row):
            md = '{0[発表者氏名]}. {0[発表題名]}. {0[発表先]}, {0[採録情報［誌名、VOL、NO、PP］及び講演区分、等]}, {0[開催都市/発表会場]}, {1}.'.format(row, date[0])
        else:
            md = '{0[発表者氏名]}. {0[発表題名]}. {0[発表先]}, {0[採録情報［誌名、VOL、NO、PP］及び講演区分、等]}, {0[開催都市/発表会場]}, {1}.'.format(row, date[1])
        return 'presentation', md

def build_other(row):
    date = get_date(row)
    target = row['発表先'].lower()
    if target.find('conference') != -1 or target.find('proceedings') != -1 or target.find('workshop') != -1:
        return build_conference(row)
    else:
        if is_japanese(row):
            md = '{0[発表者氏名]}. {0[発表題名]}. {0[発表先]}, {0[採録情報［誌名、VOL、NO、PP］及び講演区分、等]}, {1}.'.format(row, date[0])
        else:
            md = '{0[発表者氏名]}. {0[発表題名]}. {0[発表先]}, {0[採録情報［誌名、VOL、NO、PP］及び講演区分、等]}, {1}.'.format(row, date[1])
        return 'other', md

M = {
    'A.研究論文': build_journal,
    'C1.査読付収録論文': build_conference,
    'F.学術解説等': build_editorial,
    'G.一般口頭発表': build_presentation,
    'H.その他資料': build_other,
}

D = collections.defaultdict(list)

df = pd.read_excel(fname, sheet_name='1.論文等', encoding='cp932', skiprows=range(11))
for index, row in df.iterrows():
    f = M[row['発表区分']]
    tag, md = f(row)
    D[tag].append((md, row['発表年月日']))

df = pd.read_excel(fname, sheet_name='4.表彰・受賞', encoding='cp932', skiprows=range(4))
for index, row in df.iterrows():
    if row['発表区分'] in ('N.受賞', 'O.表彰'):
        D['award'].append((
            '{0[受賞等タイトル等]}. {0[受賞者等氏名]}. ({1})'.format(row, row['年月日'].strftime('%Y-%m-%d')),
            row['年月日']
            ))
    elif row['発表区分'] == 'P.成果の実施':
        D['resource'].append((
            '[{0[受賞等タイトル等]}]({0[関連情報（受賞内容、等）]})'.format(row),
            row['年月日']
            ))

def write_section(fo, D, tag, title, marker='1.'):
    print('### {}'.format(title), file=fo)
    print('', file=fo)
    items = sorted(D[tag], key=lambda x: x[1], reverse=True)
    for item in items:
        print('{} {}'.format(marker, item[0]), file=fo)
    print('', file=fo)

with open('_includes/publication.md', 'w') as fo:
    write_section(fo, D, 'award', '受賞')
    write_section(fo, D, 'journal', 'ジャーナル論文')
    write_section(fo, D, 'conference', '国際会議・ワークショップ論文')
    write_section(fo, D, 'editorial', '解説')
    write_section(fo, D, 'invited', '招待講演')
    write_section(fo, D, 'presentation', '口頭発表')
    write_section(fo, D, 'other', 'その他')
