"""
Employment-weighted LLM exposure by era-based occupation group.

Inputs (all under raw/):
  gpts/GPTs-are-GPTs/data/occ_level.csv           Eloundou et al. (Science 2024) occupation-level exposure
  gpts/GPTs-are-GPTs/data/national_May2021_dl.csv  OEWS May 2021 national file (used only as the SOC code<->title key)
  oews_t01/t01_parsed.csv                          OEWS May 2025 News Release Table 1, parsed by parse_t01.py

Outputs ():
  G_soc_classification.csv, G_exposure_by_group.csv, G_exposure_by_major_group.csv,
  G_sensitivity.csv, G_top_occupations.csv

Run: python3 -I scripts/exposure.py
"""
import numpy as np
import pandas as pd

from pathlib import Path
HERE = Path(__file__).resolve().parent
RAW = str(HERE / 'inputs')
OUT = str(HERE / 'outputs')
GP = RAW
TOTAL_EMP_2025 = 155_495_730  # Table 1 "All occupations"

# ---------------------------------------------------------------- 1. Exposure
ex = pd.read_csv(f'{GP}/occ_level.csv')
ex = ex.rename(columns={'O*NET-SOC Code': 'onet', 'Title': 'onet_title',
                        'dv_rating_alpha': 'gpt4_alpha', 'dv_rating_beta': 'gpt4_beta',
                        'dv_rating_gamma': 'gpt4_zeta', 'human_rating_alpha': 'human_alpha',
                        'human_rating_beta': 'human_beta', 'human_rating_gamma': 'human_zeta'})
MEAS = ['human_alpha', 'human_beta', 'human_zeta', 'gpt4_alpha', 'gpt4_beta', 'gpt4_zeta']
ex['soc'] = ex.onet.str[:7]
# Several O*NET-SOC codes (.00, .01, ...) map to one 6-digit SOC: take the unweighted mean.
ex6 = ex.groupby('soc')[MEAS].mean()
ex6['n_onet'] = ex.groupby('soc').size()

# O*NET-SOC 2019 detailed codes that OEWS 2025 publishes only as an aggregate.
AGG = {
    '13-1020': ['13-1021', '13-1022', '13-1023'], '13-2020': ['13-2022', '13-2023'],
    '21-1018': ['21-1011', '21-1014'], '25-2052': ['25-2055', '25-2056'],
    '25-9045': ['25-9042', '25-9043'], '29-2010': ['29-2011', '29-2012'],
    '31-1120': ['31-1121', '31-1122'], '39-7010': ['39-7011', '39-7012'],
    '47-4090': ['47-4091', '47-4099'], '51-2028': ['51-2022', '51-2023'],
    '51-2090': ['51-2092'], '53-1047': ['53-1042', '53-1043', '53-1044'],
}

# ---------------------------------------------------------------- 2. Employment
o21 = pd.read_csv(f'{GP}/national_May2021_dl.csv', encoding='utf-8-sig')
det = o21[o21.O_GROUP == 'detailed'][['OCC_CODE', 'OCC_TITLE']].rename(
    columns={'OCC_CODE': 'soc', 'OCC_TITLE': 'title'})
det['k'] = det.title.str.lower().str.strip()
t01 = pd.read_csv(f'{RAW}/t01_parsed.csv')
t01['k'] = t01.title.str.lower().str.strip()
# A title repeated in Table 1 (broad = detailed) carries the same number; keep the deepest row.
t01 = t01.drop_duplicates('k', keep='last')
occ = det.merge(t01[['k', 'emp']], on='k', how='left').drop(columns='k')
occ['emp_source'] = np.where(occ.emp.notna(), 'OEWS May 2025 Table 1', 'missing in 2025 Table 1')


def exposure_for(soc):
    if soc in ex6.index:
        return ex6.loc[soc, MEAS], 'direct'
    if soc in AGG:
        kids = [c for c in AGG[soc] if c in ex6.index]
        return ex6.loc[kids, MEAS].mean(), 'mean of O*NET children ' + ','.join(kids)
    # 'All other' residual codes: mean of exposure-rated siblings in the same broad group, else minor group.
    for width, lab in [(6, 'broad'), (5, 'minor')]:
        sib = ex6[ex6.index.str[:width] == soc[:width]]
        if len(sib):
            return sib[MEAS].mean(), f'imputed: mean of {len(sib)} rated codes in {lab} group {soc[:width]}'
    return pd.Series(np.nan, index=MEAS), 'no exposure'


vals, srcs = zip(*[exposure_for(s) for s in occ.soc])
occ = pd.concat([occ.reset_index(drop=True), pd.DataFrame(list(vals)).reset_index(drop=True)], axis=1)
occ['exposure_source'] = srcs
occ['major'] = occ.soc.str[:2]

# ---------------------------------------------------------------- 3. Classification
MAJOR_NAME = {'11': 'Management', '13': 'Business & financial operations', '15': 'Computer & mathematical',
              '17': 'Architecture & engineering', '19': 'Life, physical & social science',
              '21': 'Community & social service', '23': 'Legal', '25': 'Educational instruction & library',
              '27': 'Arts, design, entertainment, sports & media', '29': 'Healthcare practitioners & technical',
              '31': 'Healthcare support', '33': 'Protective service', '35': 'Food preparation & serving',
              '37': 'Building & grounds cleaning & maintenance', '39': 'Personal care & service',
              '41': 'Sales & related', '43': 'Office & administrative support', '45': 'Farming, fishing & forestry',
              '47': 'Construction & extraction', '49': 'Installation, maintenance & repair', '51': 'Production',
              '53': 'Transportation & material moving'}

# (a) Internet-era digital / information. Sub-groups make the sensitivity runs possible.
A1_TECH = {'11-3021', '15-2051', '17-2061'}           # plus every 15-12xx code (rule below)
A2_DIGITAL_MKT_MEDIA = {'13-1161', '15-1255', '27-1014', '27-1024', '27-3042', '27-4032'}
A3_DIGITAL_CLERICAL = {'43-9021', '43-9011', '29-9021', '29-2072', '43-9031', '49-2011'}
A4_CONTACT_CENTRE = {'43-4051', '41-9041'}
# (b) White-collar roles in the physical economy, outside the physical major groups.
B_WHITE_COLLAR = {'11-9021', '11-9111', '13-1081', '11-3051', '11-3071', '11-3013', '11-9013',
                  '11-9051', '11-9081', '11-9041', '13-1051', '11-9131'}
B_MAJORS = {'29', '31', '33', '35', '37', '39', '45', '47', '49', '51', '53'}
# (c) Pre-1995 office/professional majors. Anything else falls to (d).
C_MAJORS = {'11', '13', '23', '43'}


def classify(soc):
    mj = soc[:2]
    if soc.startswith('15-12') or soc in A1_TECH:
        return 'A', 'a1_tech', 'computer occupation (15-12xx) / CIS manager / data scientist / computer hardware engineer'
    if soc in A2_DIGITAL_MKT_MEDIA:
        return 'A', 'a2_digital_mkt_media', 'listed digital marketing / digital media / documentation occupation'
    if soc in A3_DIGITAL_CLERICAL:
        return 'A', 'a3_digital_clerical', 'listed clerical or records occupation tied to digital systems'
    if soc in A4_CONTACT_CENTRE:
        return 'A', 'a4_contact_centre', 'contact-centre occupation (customer service reps, telemarketers)'
    if soc in B_WHITE_COLLAR:
        return 'B', 'b2_physical_white_collar', 'listed manager/specialist role in a physical sector'
    if mj == '17':
        return 'B', 'b2_physical_white_collar', 'architecture & engineering major group (17), excluding 17-2061'
    if mj == '25' and (soc.startswith('25-2') or soc == '25-9045'):
        return 'B', 'b2_physical_white_collar', 'preschool / K-12 / special education teacher (25-2xxx) or K-12 teaching assistant (25-9045)'
    if soc == '11-9032':
        return 'B', 'b2_physical_white_collar', 'K-12 education administrator'
    if mj in B_MAJORS:
        return 'B', 'b1_physical_major', f'physical major group {mj}'
    if mj in C_MAJORS:
        return 'C', 'c1_office_professional', f'office/professional major group {mj}'
    return 'D', 'd1_other_pre1995', f'other pre-1995 major group {mj} (science, social service, non-K-12 education, arts/media, sales)'


cls = occ.soc.apply(classify)
occ['group'] = [c[0] for c in cls]
occ['subgroup'] = [c[1] for c in cls]
occ['rule'] = [c[2] for c in cls]
occ['major_name'] = occ.major.map(MAJOR_NAME)
GROUP_NAME = {'A': '(a) Internet-era digital/information', 'B': '(b) Pre-1995 physical economy',
              'C': '(c) Pre-1995 office/professional', 'D': '(d) Other pre-1995 (sales, science, social service, non-K-12 education, arts)'}

occ_out = occ[['soc', 'title', 'major', 'major_name', 'group', 'subgroup', 'rule', 'emp', 'emp_source',
               'exposure_source'] + MEAS]
occ_out.to_csv(f'{OUT}/G_soc_classification.csv', index=False, float_format='%.4f')

# ---------------------------------------------------------------- 4. Statistics
an = occ.dropna(subset=['emp', 'human_beta']).copy()


def stats(df, gcol):
    rows = []
    for g, d in df.groupby(gcol):
        w = d.emp
        r = {gcol: g, 'n_occ': len(d), 'employment': int(w.sum()),
             'emp_share_of_total_pct': 100 * w.sum() / TOTAL_EMP_2025}
        for m in MEAS:
            r[f'wmean_{m}'] = np.average(d[m], weights=w)
        for m in MEAS:
            r[f'pct_emp_ge50_{m}'] = 100 * w[d[m] >= 0.5].sum() / w.sum()
        for m in ['human_beta', 'gpt4_beta']:
            r[f'pct_emp_gt50_{m}'] = 100 * w[d[m] > 0.5].sum() / w.sum()
            r[f'pct_emp_ge10_{m}'] = 100 * w[d[m] >= 0.1].sum() / w.sum()
            r[f'unweighted_mean_{m}'] = d[m].mean()
        rows.append(r)
    return pd.DataFrame(rows)


allrow = stats(an.assign(all='All occupations'), 'all').rename(columns={'all': 'group'})
g = stats(an, 'group')
g['group_name'] = g.group.map(GROUP_NAME)
sg = stats(an, 'subgroup').rename(columns={'subgroup': 'group'})
sg['group_name'] = 'subgroup'
allrow['group_name'] = 'All matched occupations'
by_group = pd.concat([g, sg, allrow], ignore_index=True)
by_group.insert(1, 'group_name', by_group.pop('group_name'))
by_group.to_csv(f'{OUT}/G_exposure_by_group.csv', index=False, float_format='%.4f')

mg = stats(an, 'major')
mg.insert(1, 'major_name', mg.major.map(MAJOR_NAME))
mg = mg.sort_values('wmean_human_beta', ascending=False)
mg.to_csv(f'{OUT}/G_exposure_by_major_group.csv', index=False, float_format='%.4f')


# ---------------------------------------------------------------- 5. Sensitivity
def summarize(df, label, a_mask, b_mask):
    out = {'variant': label}
    for name, msk in [('A', a_mask), ('B', b_mask), ('rest', ~(a_mask | b_mask))]:
        d = df[msk]
        out[f'{name}_emp_m'] = d.emp.sum() / 1e6
        for m in ['human_alpha', 'human_beta', 'human_zeta', 'gpt4_beta']:
            out[f'{name}_wmean_{m}'] = np.average(d[m], weights=d.emp)
        out[f'{name}_pct_ge50_human_beta'] = 100 * d.emp[d.human_beta >= 0.5].sum() / d.emp.sum()
        out[f'{name}_pct_ge50_human_zeta'] = 100 * d.emp[d.human_zeta >= 0.5].sum() / d.emp.sum()
    out['ratio_A_over_B_human_beta'] = out['A_wmean_human_beta'] / out['B_wmean_human_beta']
    return out


A = an.group == 'A'
B = an.group == 'B'
sens = [
    summarize(an, 'baseline (A = a1+a2+a3+a4)', A, B),
    summarize(an, 'A = a1 tech only', an.subgroup == 'a1_tech', B),
    summarize(an, 'A = a1+a2 (no clerical, no contact centre)', an.subgroup.isin(['a1_tech', 'a2_digital_mkt_media']), B),
    summarize(an, 'A excludes customer service reps (43-4051)', A & (an.soc != '43-4051'), B),
    summarize(an, 'A excludes contact centre (a4)', A & (an.subgroup != 'a4_contact_centre'), B),
    summarize(an, 'A + all office & admin support (43)', A | (an.major == '43'), B & (an.major != '43')),
    summarize(an, 'A + all office/admin (43) + sales (41)', A | an.major.isin(['43', '41']), B),
    summarize(an, 'B = physical major groups only (b1)', A, an.subgroup == 'b1_physical_major'),
    summarize(an, 'B excludes healthcare practitioners (29)', A, B & (an.major != '29')),
    summarize(an, 'exclude imputed exposure rows', A & ~an.exposure_source.str.startswith('imputed'),
              B & ~an.exposure_source.str.startswith('imputed')),
]
# Exposure from the .00 O*NET code only (rather than the mean over .xx codes)
ex00 = ex[ex.onet.str.endswith('.00')].set_index('soc')[MEAS]
alt = an.copy()
hit = alt.soc.isin(ex00.index)
alt.loc[hit, MEAS] = ex00.loc[alt.loc[hit, 'soc'], MEAS].values
sens.append(summarize(alt, 'exposure from .00 O*NET code only', alt.group == 'A', alt.group == 'B'))
# Unweighted (occupation counts)
unw = an.assign(emp=1.0)
sens.append(summarize(unw, 'unweighted (each occupation = 1)', unw.group == 'A', unw.group == 'B'))
sens = pd.DataFrame(sens)
sens.to_csv(f'{OUT}/G_sensitivity.csv', index=False, float_format='%.4f')

# Bootstrap CI (resampling occupations within group) for the A-B gap in weighted mean human_beta
rng = np.random.default_rng(20261024)
dA, dB = an[A], an[B]
gaps = []
for _ in range(2000):
    sa = dA.sample(len(dA), replace=True, random_state=rng.integers(1 << 31))
    sb = dB.sample(len(dB), replace=True, random_state=rng.integers(1 << 31))
    gaps.append(np.average(sa.human_beta, weights=sa.emp) - np.average(sb.human_beta, weights=sb.emp))
gaps = np.array(gaps)

# Top-employment occupations within A for the write-up
top = an[A].sort_values('emp', ascending=False)[['soc', 'title', 'subgroup', 'emp', 'human_beta', 'gpt4_beta', 'human_zeta']]
top.to_csv(f'{OUT}/G_top_occupations_groupA.csv', index=False, float_format='%.4f')

# Share of all exposed employment by group (where exposure sits in the economy)
an['exp_emp_beta'] = an.emp * an.human_beta
share = an.groupby('group').exp_emp_beta.sum() / an.exp_emp_beta.sum() * 100
ge50 = an[an.human_beta >= 0.5].groupby('group').emp.sum() / an[an.human_beta >= 0.5].emp.sum() * 100

pd.set_option('display.width', 250)
print('coverage: matched emp', int(an.emp.sum()), f'{100*an.emp.sum()/TOTAL_EMP_2025:.2f}% of total;',
      'occupations', len(an), 'of', len(occ))
print(occ.exposure_source.str.split(':').str[0].value_counts())
print(occ[occ.emp.isna() | occ.human_beta.isna()][['soc', 'title', 'emp', 'exposure_source']])
cols = ['group', 'n_occ', 'employment', 'emp_share_of_total_pct', 'wmean_human_beta', 'wmean_gpt4_beta',
        'wmean_human_alpha', 'wmean_human_zeta', 'pct_emp_ge50_human_beta', 'pct_emp_ge50_gpt4_beta',
        'pct_emp_ge50_human_zeta', 'pct_emp_ge50_gpt4_zeta', 'pct_emp_ge50_human_alpha', 'pct_emp_ge10_human_beta']
print(by_group[cols].round(3).to_string())
print(mg[['major', 'major_name', 'employment', 'wmean_human_beta', 'wmean_gpt4_beta', 'wmean_human_zeta',
          'pct_emp_ge50_human_beta', 'pct_emp_ge50_human_zeta']].round(3).to_string())
print(sens.round(3).T.to_string())
print('bootstrap A-B gap human_beta: mean %.3f, 95%% CI [%.3f, %.3f]' % (gaps.mean(), *np.percentile(gaps, [2.5, 97.5])))
print('share of exposure-weighted employment (human beta) by group:\n', share.round(1))
print('share of employment with human_beta>=0.5 by group:\n', ge50.round(1))
print(top.head(15).round(3).to_string())
print(an.sort_values('human_beta', ascending=False)[['soc', 'title', 'group', 'emp', 'human_beta']].head(20).round(3).to_string())
