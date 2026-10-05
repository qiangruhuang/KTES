# Phase 2A full-population outcome freeze v8

**N:** 120 sequences  
**Primary endpoint:** sequence-level Anti-UAV410 State Accuracy  
**Population mean SA:** 0.351505  
**Median SA:** 0.251659  
**Sample SD:** 0.291704  

## Frozen challenge-domain truths

| Domain | N | Mean SA |
|---|---:|---:|
| TC | 81 | 0.314810 |
| OV | 31 | 0.176616 |
| SV | 27 | 0.192375 |
| FM | 52 | 0.224810 |
| OC | 12 | 0.147603 |
| DBC | 21 | 0.315042 |

## Frozen size-stratum truths

| Stratum | N | Mean SA |
|---|---:|---:|
| Tiny | 33 | 0.257994 |
| Small | 54 | 0.267334 |
| Medium | 29 | 0.557355 |
| Normal | 4 | 0.766884 |

## Difficult-case set

The pre-registered bottom 10% set contains 12 sequences. The 12th-order cutoff is SA=0.028172; tie at cutoff: **false**.

| Rank | Sequence | SA | Size | Active challenges |
|---:|---|---:|---|---|
| 1 | `3700000000002_162623_1` | 0.000741 | Tiny | TC, OV, SV, FM, OC, DBC |
| 2 | `20190925_124000_1_5` | 0.002164 | Small | TC |
| 3 | `3700000000002_133828_2` | 0.003124 | Tiny | TC, OV, FM, OC, DBC |
| 4 | `20190925_101846_1_4` | 0.007006 | Small | SV |
| 5 | `20190925_134301_1_3` | 0.007653 | Small | TC |
| 6 | `new10_train_newfix` | 0.009169 | Tiny | FM |
| 7 | `20190925_200805_1_1` | 0.011378 | Small | TC, FM |
| 8 | `20190925_134301_1_9` | 0.015884 | Small | TC |
| 9 | `3700000000002_135232_2` | 0.016721 | Tiny | TC, OV, SV, FM, OC |
| 10 | `20190925_124612_1_3` | 0.018269 | Small | TC, OV, SV |
| 11 | `20190925_193610_1_5` | 0.023063 | Small | OV, FM |
| 12 | `20190925_193610_1_6` | 0.028172 | Medium | FM |

This file freezes population truths only. No KTES, SRS, split-style sampling draw, inclusion probability, estimator, or design-UQ calculation is executed here.
