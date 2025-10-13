
# LOTUSDIS: A Thai Far‑Field Meeting Corpus for Robust Conversational ASR


[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Paper (preprint)](https://img.shields.io/badge/Paper-preprint-informational)](https://arxiv.org/pdf/2509.18722)


LOTUSDIS is a Thai non‑array meeting corpus designed for far‑field transcription in realistic office conditions. It contains **~114 hours** of multi‑channel speech (≈20 hours unique session time) recorded in **15–20‑minute** sessions with **3 speakers** each. **Nine single‑channel devices** capture audio from near‑field to 10 m, preserving device and room effects (HVAC, water cooler, etc.). We provide train/dev/test splits and baseline ASR benchmarks.

> **License:** CC‑BY‑SA 4.0. By using this dataset you agree to the terms in `LICENSE`.


---


## Contents
- [Overview](#overview)
- [Device layout & splits](#device-layout--splits)
- [Download](#download)
- [Data format](#data-format)
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
Nine single-channel devices (examples): `lav123` (~12–15 cm), `con123` (~0.5 m), `jbl` (~2 m), `bt3m` (3 m), `bt10m` (10 m).  

**Microphone arrangement inside the recording room:**

<p align="center">
  <img src="assets/device_layout.png" alt="LOTUSDIS device layout diagram" width="700">
</p>


## Download
### Audio files
- **Utterance-level audio file (train,dev,test split)**

  [📥 Train Set](https://drive.google.com/file/d/1tsZ-Qlzur80dUmYevt2d71KV5nRFdHGx/view?usp=sharing)
  
  [📥 Dev Set](https://drive.google.com/file/d/1uxu6QCQAWrP7BYgVWZyBUuWtQNwaZ3xP/view?usp=sharing)

  [📥 Test Set](https://drive.google.com/file/d/1S7nv9H41sRgYBRA_17bv31hfMqF0vdex/view?usp=sharing)

  


### Annotation files
- **Praat TextGrid annotations**  
  [📥 Download TextGrid (.zip)](https://drive.google.com/file/d/14fMv_X_8sGDPGbnU-hpJ85Mug43AHlgO/view?usp=sharing)
- **Utterance-level annotation CSV**  
  [📥 Download annotation CSV](https://drive.google.com/file/d/1ut44pgT1tJRd30clNp-IPx6nJiW7co-z/view?usp=sharing)



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


## Cite
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
