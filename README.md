
# LOTUSDIS: A Thai Far‑Field Meeting Corpus for Robust Conversational ASR


[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](LICENSE)
[![Data Card](https://img.shields.io/badge/Dataset-Card-blue)](docs/DATASET_CARD.md)
[![Paper (preprint)](https://img.shields.io/badge/Paper-preprint-informational)](#citation)


LOTUSDIS is a Thai non‑array meeting corpus designed for far‑field transcription in realistic office conditions. It contains **~114 hours** of multi‑channel speech (≈20 hours unique session time) recorded in **15–20‑minute** sessions with **3 speakers** each. **Nine single‑channel devices** capture audio from near‑field to 10 m, preserving device and room effects (HVAC, water cooler, etc.). We provide train/dev/test splits and baseline ASR benchmarks.

> **License:** CC‑BY‑SA 4.0 (see [LICENSE](LICENSE)). By using this dataset you agree to the terms in `LICENSE` and `docs/TERMS.md`.


---


## Contents
- [Overview](#overview)
- [Device layout & splits](#device-layout--splits)
- [Download](#download)
- [Data format](#data-format)
- [Manifests](#manifests)
- [Baselines](#baselines)
- [Evaluation](#evaluation)
- [Cite](#cite)

  
## Overview
- Language: **Thai**
- Domain: **Conversational, multi‑speaker, far‑field**
- Duration: **~114 h** (≈88 h train / 12.8 h dev / 13.3 h test)
- Speakers: **86** (age 19–48; spontaneous conversation with overlap)
- Setting: **Furnished office** (16×9.5×2.7 m). Stationary noise sources active.


## Device layout & splits
Nine single‑channel devices (examples): `lav123` (~12–15 cm), `con123` (~0.5 m), `jbl` (~2 m), `bt3m` (3 m), `bt10m` (10 m).
Official splits live in `data/manifests/`.

## Download
We host public artifacts under permissive terms. Use our helper script:


```bash
pip install -r scripts/requirements.txt
python scripts/download_lotusdis.py --root ./data \
--subset train,dev,test \
--channels lav123,con123,jbl,bt3m,bt10m \ 
--verify
```

# LOTUSDIS Results

## Key takeaways
- **Fine‑tuning on in‑domain LOTUSDIS** cuts **overall WER from 64.3% → 38.3%**.
- On **far‑field** microphones, fine‑tuning reduces WER **81.6% → 49.5%**.
- WER increases with **distance** and **overlap** (2‑ and 3‑speaker).

## Overall (Pathumma Whisper)
| Model | Training | Eval subset | WER (%) |
|------|----------|-------------|---------|
| Pathumma Whisper | zero‑shot | all | **64.3** |
| Pathumma Whisper | fine‑tuned on LOTUSDIS | all | **38.3** |
| Pathumma Whisper | zero‑shot | far‑field only | **81.6** |
| Pathumma Whisper | fine‑tuned on LOTUSDIS | far‑field only | **49.5**

```
@misc{tipaksorn2025lotusdisthaifarfieldmeeting,
      title={LOTUSDIS: A Thai far-field meeting corpus for robust conversational ASR}, 
      author={Pattara Tipaksorn and Sumonmas Thatphithakkul and Vataya Chunwijitra and Kwanchiva Thangthai},
      year={2025},
      eprint={2509.18722},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2509.18722}, 
}
```
