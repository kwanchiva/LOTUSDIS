
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

| Base model | Fine-tuned data | Front-end | lavalier | condenser | jbl | bt3m | bt10m | Near-field | Far-field | Overall |
|------------|----------------|-----------|----------|-----------|-----|------|-------|------------|-----------|---------|
| **(A) Zero-shot** | | | | | | | | | | |
| Whisper-large-v3 | – | – | 51.95 | 48.37 | 59.90 | 117.03 | 125.52 | 50.16 | 100.82 | 79.84 |
| Pathumma-whisper-th-large-v3 | – | – | 37.55 | 36.43 | 44.22 | 96.27 | 104.22 | 36.99 | 81.57 | 64.32 |
| Biodatlab/whisper-th-large-v3-combined | – | – | 42.51 | 39.45 | 46.00 | 97.77 | 106.43 | 40.98 | 83.40 | 66.36 |
| Monsoon-whisper-medium-gigaspeech2 | – | – | 39.03 | 37.29 | 43.31 | 109.10 | 124.87 | 38.16 | 92.43 | 66.15 |
| **(B) Full Fine-tuned on All Mic (Baseline)** | | | | | | | | | | |
| Whisper-large-v3 | All Mic | – | 23.20 | 20.81 | 27.27 | 59.00 | 65.25 | 22.01 | 50.51 | 39.05 |
| Pathumma-whisper-th-large-v3 | All Mic | – | 22.77 | 20.40 | **26.42** | **58.15** | **64.04** | 21.59 | **49.54** | **38.33** |
| **(C) Front-end processing** | | | | | | | | | | |
| Pathumma-whisper-th-large-v3 | All Mic | WPE | 37.14 | 34.69 | 37.00 | 63.04 | 68.32 | 35.92 | 56.12 | 48.00 |
| Pathumma-whisper-th-large-v3 | All Mic | MMSE-LSA | 26.69 | 23.14 | 31.22 | 62.92 | 69.52 | 24.92 | 54.55 | 42.89 |
| **(D) Single-mic fine-tunes** | | | | | | | | | | |
| Pathumma-whisper-th-large-v3 | Condenser | – | 22.27 | 19.26 | 27.02 | 97.95 | 113.65 | 20.77 | 79.54 | 50.12 |
| Pathumma-whisper-th-large-v3 | BT3M | – | 29.38 | 26.61 | 34.51 | 60.17 | 69.86 | 28.00 | 54.85 | 44.75 |
| **(E) Data augmentation (single-mic)** | | | | | | | | | | |
| Pathumma-whisper-th-large-v3 | Condenser+Spec | – | 23.16 | 19.67 | 28.99 | 82.40 | 90.06 | 21.42 | 67.15 | 49.11 |
| Pathumma-whisper-th-large-v3 | Condenser+Reverb | – | **21.57** | **18.77** | 26.61 | 80.30 | 89.25 | **20.17** | 65.39 | 45.86 |
