# Dig: D5 Plan B Grid C 第3回較正 — 2026-11-09

**CALIBRATION ONLY / NOT_CERTIFIED / NO FULL RUN / NO JUDGE PASS / V4 GENERAL DOMAIN OPEN**

2026-11-09 JST, daybreak-works, python3 -I, 16-worker ProcessPoolExecutor. The K_n and R derivative functions are unchanged from SHA-pinned B′ v2 source; the new normalised kernel is the same algebraic producer (3.12) as Round 2. The 16-worker code divides each outer box into 12 angular bands × two theta branches and sums exact rational interval lower endpoints. This is *not* an independent mathematical verifier.

## Method definitions

- (a) depth [1/32,1/16], grid C with four times the baseline subdivisions for i=3..8; beta=1.
- (b) split parent depth into beta=2 children, evaluate baseline C per child and double all bands with negative baseline raw lower endpoints (per-child selection).
- (c) beta=2 plus both modifications: fourfold i=3..8 and an additional twofold for baseline-negative bands, yielding eightfold subdivisions in their overlap.
- The scale ell is fixed by the parent depth band in both children. The two child minima are compared on the same parent region. Each child pays CUT once. Original face/analytic thin-layer bounds are not added.

## E and M deep-band results

| mode | box | child 0 lower | child 1 lower | guaranteed parent lower | child wall time(s) |
|---|---|---:|---:|---:|---|
| a | E | -0.6002538797 | — | **-0.6002538797** | 28.6316 |
| a | M | -1.3159531474 | — | **-1.3159531474** | 28.6203 |
| b | E | -0.0578945322 | -0.0131149850 | **-0.0578945322** | 25.3688 + 24.5954 |
| b | M | +0.0835630310 | +0.1697102908 | **+0.0835630310** | 26.1166 + 26.61 |
| c | E | +0.0540726069 | +0.0886295497 | **+0.0540726069** | 38.6414 + 31.4448 |
| c | M | +0.2271157309 | +0.2557872707 | **+0.2271157309** | 38.1634 + 36.2296 |

## Preceding-depth band [1/64,1/32] with C plus negative-band 2× (beta=1)

| box | H_B lower | wall time(s) |
|---|---:|---:|
| E | -0.2076933752 | 26.3744 |
| M | -5.0402948880 | 26.4544 |

Both boundary checks remain negative; negative interval lower endpoints do not establish H<0. The deepest representative E and M pass the numerical target H_B>1/20 only under (c) for both, and under (b) for M. These are calibration results, not a certified general-domain result.

## Angular band breakdown

Each table combines both branches at each i. Values are decimal presentations of exact rational interval lower endpoints, not replacement proof inputs; full rationals are in JSON. Parent guarantee for beta=2 is the minimum across child 0/1, not an average.

### mode a / E — parent

| i | raw lower | midpoint lower | z-curvature lower | s-curvature lower | both-branch cells |
|---:|---:|---:|---:|---:|---:|
| 0 | -5.26428808e-06 | +3.06039706e-06 | -2.07510124e-06 | -6.2495839e-06 | 256 |
| 1 | -4.02853714e-05 | +1.1637519e-05 | -2.54246151e-05 | -2.64982752e-05 | 256 |
| 2 | -0.0004338185 | +3.75285511e-05 | -0.000344071157 | -0.000127275894 | 256 |
| 3 | -0.00214370107 | -0.00121915255 | -0.000252747891 | -0.000671800634 | 1024 |
| 4 | -0.0366571925 | -0.0275784673 | -0.00337437528 | -0.00570434988 | 1024 |
| 5 | -0.186536983 | -0.129700503 | -0.0243205044 | -0.032515975 | 1024 |
| 6 | -0.324671499 | -0.216600694 | -0.0549266383 | -0.0531441666 | 1024 |
| 7 | -0.210065996 | -0.154017217 | -0.0348946504 | -0.0211541287 | 1024 |
| 8 | -0.0712314047 | -0.038118442 | -0.024429492 | -0.00868347065 | 1024 |
| 9 | -0.927093438 | +0.011387698 | -0.931073393 | -0.00740774272 | 512 |
| 10 | -0.0576369696 | +0.0878061728 | -0.14292859 | -0.00251455282 | 1024 |
| 11 | +0.390748966 | +0.400924366 | -0.00984342963 | -0.000331969676 | 2048 |

### mode a / M — parent

| i | raw lower | midpoint lower | z-curvature lower | s-curvature lower | both-branch cells |
|---:|---:|---:|---:|---:|---:|
| 0 | -0.000182038561 | +4.17210236e-06 | -7.08474309e-05 | -0.000115363232 | 256 |
| 1 | -0.00170067065 | +1.48943155e-05 | -0.000948701849 | -0.000766863121 | 256 |
| 2 | -0.0375609004 | -8.39183917e-05 | -0.0327081641 | -0.004768818 | 256 |
| 3 | -0.167910735 | -0.0116100642 | -0.108316515 | -0.0479841563 | 1024 |
| 4 | -1.44219091 | -0.0918580237 | -1.14179431 | -0.208538579 | 1024 |
| 5 | -2.44344777 | -0.191541452 | -2.07052535 | -0.18138097 | 1024 |
| 6 | -0.382867885 | -0.126580682 | -0.235726576 | -0.0205606264 | 1024 |
| 7 | -0.0590174889 | -0.0390562299 | -0.0188351544 | -0.00112610459 | 1024 |
| 8 | -0.0016590032 | +0.0044030797 | -0.00566250704 | -0.000399575864 | 1024 |
| 9 | -0.330623382 | -0.0138067898 | -0.314652245 | -0.00216434725 | 512 |
| 10 | +0.0476175444 | +0.29836811 | -0.242080325 | -0.0086702404 | 1024 |
| 11 | +0.788898204 | +0.891971223 | -0.0985256754 | -0.00454734397 | 2048 |

### mode b / E — child 0

| i | raw lower | midpoint lower | z-curvature lower | s-curvature lower | both-branch cells |
|---:|---:|---:|---:|---:|---:|
| 0 | +1.28532888e-05 | +1.34438633e-05 | -1.67911683e-07 | -4.22662809e-07 | 256 |
| 1 | +4.83030345e-05 | +5.21890986e-05 | -2.11003083e-06 | -1.7760333e-06 | 256 |
| 2 | +0.000149443666 | +0.000186534072 | -2.90938449e-05 | -7.99656057e-06 | 256 |
| 3 | +0.000261939247 | +0.000396214683 | -9.18546251e-05 | -4.24208101e-05 | 512 |
| 4 | -0.0103080709 | -0.00873483677 | -0.0012178619 | -0.000355372194 | 512 |
| 5 | -0.0731050119 | -0.055619301 | -0.0145572535 | -0.00292845735 | 512 |
| 6 | -0.16731916 | -0.0957699277 | -0.0634432849 | -0.00810594778 | 512 |
| 7 | -0.153822505 | -0.0580913102 | -0.0895924388 | -0.00613875601 | 512 |
| 8 | -0.115608595 | +0.0131281526 | -0.124352408 | -0.0043843398 | 512 |
| 9 | -0.00402209156 | +0.0486422319 | -0.0478211878 | -0.00484313571 | 1024 |
| 10 | +0.0304451265 | +0.144582891 | -0.112156354 | -0.00198141096 | 1024 |
| 11 | +0.430597897 | +0.439350072 | -0.00846455285 | -0.000287621759 | 2048 |

### mode b / M — child 0

| i | raw lower | midpoint lower | z-curvature lower | s-curvature lower | both-branch cells |
|---:|---:|---:|---:|---:|---:|
| 0 | +1.08604759e-05 | +1.83852193e-05 | -4.3013271e-06 | -3.22341633e-06 | 256 |
| 1 | +3.67916836e-05 | +6.90699886e-05 | -1.12004303e-05 | -2.10778747e-05 | 512 |
| 2 | -0.000104612188 | +0.000212497382 | -0.000165628612 | -0.000151480958 | 512 |
| 3 | -0.0104530685 | -0.00285486098 | -0.0061934949 | -0.00140471265 | 512 |
| 4 | -0.112699029 | -0.0377349589 | -0.0681872823 | -0.00677678788 | 512 |
| 5 | -0.254595138 | -0.0762176024 | -0.172302867 | -0.00607466769 | 512 |
| 6 | -0.214128455 | -0.049217106 | -0.163288924 | -0.00162242496 | 512 |
| 7 | -0.0453574512 | -0.00996106497 | -0.035153333 | -0.000243053272 | 512 |
| 8 | -0.0140953806 | +0.012122517 | -0.0259945915 | -0.000223306147 | 512 |
| 9 | -0.0105095028 | +0.00921938441 | -0.0180547841 | -0.00167410318 | 1024 |
| 10 | +0.166646661 | +0.378679906 | -0.204735895 | -0.00729734955 | 1024 |
| 11 | +0.86863432 | +0.959239012 | -0.0866348706 | -0.0039698214 | 2048 |

### mode c / E — child 0

| i | raw lower | midpoint lower | z-curvature lower | s-curvature lower | both-branch cells |
|---:|---:|---:|---:|---:|---:|
| 0 | +1.28532888e-05 | +1.34438633e-05 | -1.67911683e-07 | -4.22662809e-07 | 256 |
| 1 | +4.83030345e-05 | +5.21890986e-05 | -2.11003083e-06 | -1.7760333e-06 | 256 |
| 2 | +0.000149443666 | +0.000186534072 | -2.90938449e-05 | -7.99656057e-06 | 256 |
| 3 | +0.000346605139 | +0.000394350955 | -5.30892576e-06 | -4.24368899e-05 | 2048 |
| 4 | -0.00915561394 | -0.00873971291 | -6.01945771e-05 | -0.00035570645 | 2048 |
| 5 | -0.0590415721 | -0.0555715115 | -0.000542514766 | -0.00292754582 | 2048 |
| 6 | -0.105586198 | -0.0957544275 | -0.00173282393 | -0.00809894706 | 2048 |
| 7 | -0.0661657055 | -0.0581926192 | -0.00182390188 | -0.00614918441 | 2048 |
| 8 | +0.00657354995 | +0.0130515893 | -0.00209307686 | -0.00438496246 | 2048 |
| 9 | -0.00402209156 | +0.0486422319 | -0.0478211878 | -0.00484313571 | 1024 |
| 10 | +0.0304451265 | +0.144582891 | -0.112156354 | -0.00198141096 | 1024 |
| 11 | +0.430597897 | +0.439350072 | -0.00846455285 | -0.000287621759 | 2048 |

### mode c / M — child 0

| i | raw lower | midpoint lower | z-curvature lower | s-curvature lower | both-branch cells |
|---:|---:|---:|---:|---:|---:|
| 0 | +1.08604759e-05 | +1.83852193e-05 | -4.3013271e-06 | -3.22341633e-06 | 256 |
| 1 | +3.67916836e-05 | +6.90699886e-05 | -1.12004303e-05 | -2.10778747e-05 | 512 |
| 2 | -0.000104612188 | +0.000212497382 | -0.000165628612 | -0.000151480958 | 512 |
| 3 | -0.00452886972 | -0.00286243072 | -0.000260651147 | -0.00140578786 | 2048 |
| 4 | -0.0466680946 | -0.037704095 | -0.00219613493 | -0.00676786461 | 2048 |
| 5 | -0.0865784847 | -0.0761847978 | -0.00431434659 | -0.00607934026 | 2048 |
| 6 | -0.0539971755 | -0.0493072796 | -0.00305595853 | -0.00163393738 | 2048 |
| 7 | -0.0109227442 | -0.0100275528 | -0.000650639903 | -0.000244551509 | 2048 |
| 8 | +0.0113706357 | +0.0120900268 | -0.000495711946 | -0.00022367913 | 2048 |
| 9 | -0.0105095028 | +0.00921938441 | -0.0180547841 | -0.00167410318 | 1024 |
| 10 | +0.166646661 | +0.378679906 | -0.204735895 | -0.00729734955 | 1024 |
| 11 | +0.86863432 | +0.959239012 | -0.0866348706 | -0.0039698214 | 2048 |

## Boundary-band breakdown

### boundary / E

| i | raw lower | midpoint lower | z-curvature lower | s-curvature lower | both-branch cells |
|---:|---:|---:|---:|---:|---:|
| 0 | -1.04818582e-05 | +5.810526e-06 | -3.05763289e-06 | -1.32347513e-05 | 512 |
| 1 | -8.529124e-05 | +1.86387214e-05 | -4.05405196e-05 | -6.33894418e-05 | 512 |
| 2 | -0.00149515649 | -0.000630932483 | -0.000531412766 | -0.000332811243 | 512 |
| 3 | -0.0244988475 | -0.0139185665 | -0.00781199701 | -0.00276828398 | 512 |
| 4 | -0.143634544 | -0.0645221363 | -0.0643671107 | -0.0147452975 | 512 |
| 5 | -0.288056291 | -0.106956003 | -0.158368125 | -0.0227321634 | 512 |
| 6 | -0.203606619 | -0.0817052156 | -0.112189063 | -0.00971234055 | 512 |
| 7 | -0.0909848879 | -0.0314467732 | -0.056121913 | -0.00341620172 | 512 |
| 8 | -0.0970237836 | +0.00746571298 | -0.10124232 | -0.00324717695 | 512 |
| 9 | -0.0239738221 | +0.0227427138 | -0.0425830826 | -0.00413345341 | 1024 |
| 10 | +0.0105169569 | +0.118801772 | -0.106430467 | -0.00185434737 | 1024 |
| 11 | +0.423697341 | +0.432247878 | -0.00826854809 | -0.000281989244 | 2048 |

### boundary / M

| i | raw lower | midpoint lower | z-curvature lower | s-curvature lower | both-branch cells |
|---:|---:|---:|---:|---:|---:|
| 0 | -0.000480471388 | +7.43208481e-06 | -0.000104847128 | -0.000383056345 | 512 |
| 1 | -0.00545873725 | -4.71944873e-05 | -0.00303285345 | -0.00237868931 | 512 |
| 2 | -0.30672678 | -0.00584151096 | -0.277071992 | -0.0238132765 | 512 |
| 3 | -3.64420688 | -0.0459581259 | -3.4965225 | -0.101726252 | 512 |
| 4 | -11.6221987 | -0.0959018175 | -11.440295 | -0.0860018602 | 512 |
| 5 | -0.971407279 | -0.0658438688 | -0.895664002 | -0.00989940791 | 512 |
| 6 | -0.108457295 | -0.0256748956 | -0.0821844884 | -0.000597911057 | 512 |
| 7 | -0.0187047685 | -0.00257392149 | -0.0160191575 | -0.000111689523 | 512 |
| 8 | -0.0253486726 | +0.000552237512 | -0.0256743302 | -0.00022657985 | 512 |
| 9 | -0.0363408864 | -0.0155492615 | -0.0190499262 | -0.00174169867 | 1024 |
| 10 | +0.146799369 | +0.358886106 | -0.204854928 | -0.0072318096 | 1024 |
| 11 | +0.861521382 | +0.950874047 | -0.0854615732 | -0.00389109179 | 2048 |

## Wall-time extrapolation — provisional only

Measured (a)/E 16-worker single-box time: 28.6316 s. The empirical (a)/M time is 28.6203 s. The remote CPU exposes 24 logical CPUs.

| stage r_in | distinct depth bands | parent boxes | cumulative time at constant a/E sample | incremental time |
|---|---:|---:|---:|---:|
| 255/256 | 8 | 6656 | 52.94 h | +52.94 h |
| 63/64 | 10 | 8320 | 66.17 h | +13.23 h |
| 15/16 | 12 | 9984 | 79.40 h | +13.23 h |

This is a *conditional planning proxy*, not a predicted proof run. In particular, mode (a) itself fails E/M. Using beta=2 on one full 832-box depth band adds a second child evaluation to those parents. For the deepest band, the measured (c) E parent costs 38.6414+31.4448=70.0862 s instead of 28.6316 s for (a), a sample extra of roughly 9.58 h over 832 boxes. M costs 74.393 s per beta=2 parent (sample extra roughly 10.58 h). Other boxes may behave differently. Full proof costs also require independent verifier time, and boundary-band negative checks cannot be budgeted as certified.

## Integrity and limitations

- `audit_round3_remote.py` verifies 17 current result JSON objects: all 24 branch-band contributions, exact rational aggregation, sign-aware prefactor, one CUT deduction, and method-specific grid factors. A superseded exploratory combined refinement with only max(factors) is not used.
- The 2026-11-08 (round 2) independent aggregate checker is not a mathematical verifier; neither is the present round 3 checker.
- No proof of all 9,984 outer boxes, no V4 freeze, no chat independent verifier, no Muse code audit, no official PASS, no Judge ruling.
- B7 L0_T2_D3/L0_T3_D3 new ZIPs and remaining 11 box runs were not found in the inspected remote workspaces. Official B7 remains 25/40; V5.3 FROZEN.
