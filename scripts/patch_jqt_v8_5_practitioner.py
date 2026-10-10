from pathlib import Path
import re

ROOT = Path('paper/submission_v8_5_jqt')
P = ROOT / 'MANUSCRIPT_JQT_v8_5_BLINDED.md'
text = P.read_text(encoding='utf-8')

old_kw = ('**Keywords:** active sampling; balanced sampling; finite-population inference; '
          'Hájek estimator; operational test and evaluation; probability sampling; '
          'reliability evaluation; small-sample qualification; uncertainty quantification')
new_kw = ('**Keywords:** active sampling; finite-population inference; reliability evaluation; '
          'small-sample qualification; test allocation')

if old_kw in text:
    text = text.replace(old_kw, new_kw, 1)
elif new_kw not in text:
    raise SystemExit('keyword line did not match expected canonical state')

old_heading = '### 5.6 Boundaries and next test'
new_heading = '### 5.7 Boundaries and next test'
advice = '''### 5.6 Advice to practitioners

c-pKTES-Hedge is most appropriate when the candidate test conditions can be enumerated before testing, the target population or operational weights are defined, and useful auxiliary covariates are available without observing the test outcomes. Before execution, practitioners should freeze the population frame, strata, critical domains, endpoint definitions, the three certainty sentinels, and the full vector of first-order inclusion probabilities. Weight stability should be checked before interpreting any apparent gain in difficult-case coverage; in the present studies, Kish effective sample size was used as an explicit guardrail rather than as a post hoc diagnostic.

The method should not be forced onto a source whose design variables become available only after the test unfolds, or onto an endpoint whose engineering meaning has not been validated. In those settings, stopping at the source or endpoint gate is preferable to constructing an outcome-informed design and calling it confirmatory. For computational reproducibility, the realized sampling-design object should be written and hashed before outcomes are opened, because rerunning the same high-level code and seeds may not reproduce an identical unequal-probability design. c-pKTES-Hedge should therefore be viewed as a disciplined allocation-and-inference workflow: auxiliary models guide where scarce tests are spent, while the physical outcomes and their realized inclusion probabilities remain the basis for population inference.

'''

if '### 5.6 Advice to practitioners' not in text:
    if old_heading not in text:
        raise SystemExit('expected boundaries heading not found')
    text = text.replace(old_heading, advice + new_heading, 1)
elif new_heading not in text:
    text = text.replace(old_heading, new_heading, 1)

# Fail closed on frozen scientific anchors.
required = [
    'n_L=40', 'min_probability_fraction=0.35', '0.006824', '0.008348',
    '0.00404', '0.00137 to 0.00671', '-0.0007586',
    '-0.0011638 to -0.0003534', '254 of 257', '0.0108412',
    'PASS_WITH_EXECUTION_CLARIFICATION', 'BLOCKED_SOURCE_STRUCTURE',
    'NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION',
]
for token in required:
    if token not in text:
        raise SystemExit(f'missing frozen scientific token: {token}')

# JQT-facing presentation checks.
kw_line = re.search(r'^\*\*Keywords:\*\* (.+)$', text, re.M)
if not kw_line:
    raise SystemExit('keywords missing')
keywords = [x.strip() for x in kw_line.group(1).split(';')]
if len(keywords) != 5:
    raise SystemExit(f'expected 5 keywords, got {len(keywords)}')
if text.count('### 5.6 Advice to practitioners') != 1:
    raise SystemExit('Advice to practitioners section count mismatch')
if text.count('### 5.7 Boundaries and next test') != 1:
    raise SystemExit('Boundaries heading count mismatch')

P.write_text(text, encoding='utf-8')
print('patched', P)
print('keywords', keywords)
