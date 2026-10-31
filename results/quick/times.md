# Time table (MODE=quick, TRAIN=load, WEIGHTS=out/weights/nostab_5bit.npz, NJ=16, tools on PATH (container), 2026-10-30 01:14)

| Group | Step | Time (s) | Result | Note |
|---|---|---:|---|---|
| install | fix paths | 0.2 | ok |  |
| install | install: mamba | 0.0 | skipped | tools already on PATH (container) |
| install | install: eda | 0.0 | skipped | tools already on PATH (container) |
| install | install: openroad | 0.0 | skipped | tools already on PATH (container) |
| install | install: openvaf | 0.0 | skipped | tools already on PATH (container) |
| install | install: ngspice | 0.0 | skipped | tools already on PATH (container) |
| install | install: xyce | 0.0 | skipped | tools already on PATH (container) |
| install | install: py | 3.2 | ok | PART py 3.1 ok |
| install | install: pdk | 0.0 | ok | PART pdk 0.0 ok |
| install | tool versions | 2.7 | ok | 8.3.685 / Netgen 1.5.324 compiled on Thu Oct 15 02:24:51 PM CEST 2026 / Warning: netgen command 'format' use fully-qualified name '::netgen::format' / 26Q4-407- |
| training | download MNIST | 7.3 | ok |  |
| training | training | 0.0 | skipped | TRAIN=load: training skipped, saved weights out/weights/nostab_5bit.npz are used |
| training | figure: training curve | 0.2 | ok |  |
| simulation | inference: saved weights, 3 seeds (nostab_5bit.npz) | 23.7 | ok | {"5b_s0": {"test": 0.958993, "saved": 0.958993, "diff": 0.0, "p_neuron_uW": 4912.35}, "5b_s1": {"test": 0.954795, "saved": 0.954795, "diff": 0.0, "p_neuron_uW": |
| simulation | figure: test accuracy and confusion matrix | 0.2 | ok |  |
| simulation | Xyce: weight-update block | 104.9 | ok | WU block: cells 132/132, decisions match 132/132, COMP1/2 sign 132/132, /ΔV_f/ path error median 6.3626 mV, power 2.7626 mW |
| simulation | figure: weight-update decisions | 0.2 | ok |  |
| simulation | ngspice: RRAM write grid (OpenVAF → OSDI) | 31.5 | ok | 1R write grid: rows 392/392, rows with G changed by > 5 %: 143 (HSPICE: 143), ird ratio vs reference log [1.0, 1.0] |
| simulation | figure: RRAM write waveform | 0.4 | ok |  |
| simulation | Xyce: chip deck sys2 | 0.0 | skipped | quick mode: the chip deck runs only in full mode (Xyce, 1 core, about 13–20 min) |
| simulation | RRAM write chip deck chip_write3 | 0.0 | skipped | not yet with open-source tools: Xyce has no OSDI, ngspice + OSDI fails at the operating point |
| layout | block: arr_w3s_128x64 | 5.7 | ok | XOR arr_w3s_128x64: same |
| layout | block: analog (input_drive, nudge_inj, bias_beta, wbuf) | 9.4 | ok | XOR input_drive: same; XOR nudge_inj: same; XOR bias_beta: same; XOR wbuf: same |
| layout | block: tg_n2 (switch macro) | 0.2 | ok | XOR tg_n2: same |
| layout | block: HOG op-amp | 0.3 | ok | XOR hog: same |
| layout | block: wu (weight update) | 8.1 | ok | XOR wu: same |
| layout | block: test patterns (4 blocks) | 1.2 | ok | XOR tp_tl: same; XOR tp_br: same; XOR tp_bandl: same; XOR tp_bandr: same |
| layout | block: pad frame | 40.4 | ok | XOR ep_die_real: same |
| layout | figure: block GDS | 1.3 | ok |  |
| layout | netlist: chip deck v3 + mk_top | 2.6 | ok | 덱 비교: 경계 node 718, 같음 701, 일부러 다름 17, 예상 밖 0, 셀 대응 틀림 0, 미분류 소자 0 / diff lines vs saved: cdl 0, v 0 |
| layout | placement: mk_lef + place_real | 17.5 | ok | LEF files different from saved: 0, place_real.json same |
| layout | figure: floorplan | 0.3 | ok |  |
| routing | pre-wiring (Python) | 25.6 | ok |  |
| routing | OpenROAD global + detailed route | 61.4 | ok | detailed route iterations 4, last: [INFO DRT-0199]   Number of violations = 0. / ORR: route nets without wire 0 / [INFO ANT-0002] Found 0 net violations. |
| routing | DEF → GDS + check | 0.8 | ok | CHECK_GDS PASS |
| routing | figure: routed core GDS | 0.7 | ok |  |
| routing | pad ring + die | 5.6 | ok | CONN OK |
| routing | figure: die GDS | 1.0 | ok |  |
| verification | Magic RRAM tech rebuild | 0.0 | ok | diff lines vs copy in src/: 0 |
| verification | core extraction + antenna (Magic) | 583.6 | ok | antenna 276, 583.52 s, 1310.9 MB |
| verification | core LVS (Netgen) | 1.6 | ok | Circuits match uniquely. / top {'dev': [83, 83], 'nets': [1130, 1130], 'result': 'Netlists match with 32 symmetries with property errors.'} |
| verification | die extraction (Magic, LVS view) | 141.8 | ok | 141.68 s, 1400.2 MB |
| verification | die LVS (Netgen, pads as black boxes) | 1.7 | ok | Circuits match uniquely. / top {'dev': [1, 1], 'nets': [25, 25], 'result': 'Netlists match uniquely.'} |
| verification | array block DRC arr_w3s_128x64 (Magic, quick mode) | 65.5 | ok | boxes 0 {} |
| verification | core and die DRC (Magic) | 0.0 | skipped | quick mode: only in full mode (core about 12 min + die about 21 min, 1 core) |
| verification | figure: DRC per rule and LVS table | 0.0 | ok |  |

| Group | Time (s) | min |
|---|---:|---:|
| install | 6.1 | 0.1 |
| training | 7.5 | 0.1 |
| simulation | 160.9 | 2.7 |
| layout | 87.0 | 1.4 |
| routing | 95.1 | 1.6 |
| verification | 794.2 | 13.2 |
| **Total** | **1150.8** | **19.2** |

0 failed: none
