#!/usr/bin/env python3
from pathlib import Path
import re, hashlib
ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "paper" / "PAPER_JQT_v8_4.md"
text = p.read_text(encoding="utf-8")
body = text[:text.index("## References")]
abstract = body.split("## Abstract",1)[1].split("**Keywords:**",1)[0]
main_words = len(re.findall(r"\b[\w-]+\b", body))
abstract_words = len(re.findall(r"\b[\w-]+\b", abstract))
cited = {int(x) for x in re.findall(r"\[(\d+)\]", body)}
for a,b in re.findall(r"\[(\d+)\]\s*[–-]\s*\[(\d+)\]", body):
    cited.update(range(int(a), int(b)+1))
checks=[]
def check(name, cond): checks.append((name,bool(cond)))
check("n=40 preserved", "n_L=40" in text and "`n=40`" in text)
check("3 certainty + 37 remainder", "three outcome-blind certainty sentinels" in text and "37-unit probability remainder" in text)
check("rho/lambda frozen", "\\rho=0.20" in text and "\\lambda=3" in text)
check("R3 calibration preserved", "0.137719714266479" in text and "0.19767009190382911" in text)
check("R5 1000 populations", "1000 new finite populations" in text)
check("edge result preserved", "0.812" in text and "0.779" in text and "-0.0013 to +0.0673" in text)
check("no edge superiority", "does not establish edge-discovery superiority" in text)
check("primary MAEs preserved", all(x in text for x in ["0.006824","0.008348","0.051746","0.060399","0.016811","0.020958"]))
check("decision metrics preserved", all(x in text for x in ["0.173","0.089","0.826","0.911"]))
check("Anti-UAV adverse profile result retained", "0.00404" in text and "0.00137 to 0.00671" in text)
check("Anti-UAV ESS retained", "33.12" in text and "32.60" in text)
check("IDF-DS explicitly no performance result", "did not produce a c-pKTES-Hedge performance result" in text)
check("AMOVFLY profile result retained", "-0.0007586" in text and "-0.0011638 to -0.0003534" in text)
check("AMOVFLY semantic defect retained", "378 exact-zero episodes" in text.lower() and "all 257 flights" in text.lower())
check("pi drift retained", "254 of 257" in text and "0.0108412" in text)
check("formal evidence classes retained", all(x in text for x in ["PASS_WITH_EXECUTION_CLARIFICATION","BLOCKED_SOURCE_STRUCTURE","NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION"]))
check("4 figure references", len(re.findall(r"!\[", body)) == 4)
check("3 main tables", len(re.findall(r"\*\*Table [123]\.", body)) == 3)
check("expanded main text >= 6000 words", main_words >= 6000)
check("abstract <= 250 words", abstract_words <= 250)
check("all references 1-17 cited in body", all(i in cited for i in range(1,18)))
check("no universal superiority claim", "universally superior" not in body.lower())
check("no defensive banned phrases", not any(x in body.lower() for x in ["unfortunately","merely","still lags far behind","severely insufficient"]))
for name,ok in checks: print(("PASS" if ok else "FAIL"), name)
print(f"WORDS {main_words}; ABSTRACT {abstract_words}; SHA256 {hashlib.sha256(text.encode()).hexdigest()}")
if not all(ok for _,ok in checks): raise SystemExit(f"{sum(ok for _,ok in checks)}/{len(checks)} checks passed")
print(f"{len(checks)}/{len(checks)} PASS")
