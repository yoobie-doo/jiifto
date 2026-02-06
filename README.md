# Jiifto
## Metrical Scanner

![Streamlit App Screenshot](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Overview

**Poem In → Meter Out**: An interactive web application that automatically scans the metrical structure of Somali Jiifto poetry. Simply paste a poem, and the app returns a syllable-by-syllable breakdown of short (S) and long (L) syllables.

Built with **Streamlit** and powered by a **Conditional Random Field (CRF)** model trained on hand-annotated Somali verse, this tool bridges computational linguistics and cultural preservation.

---

## Why This Matters

### Cultural Preservation

Somali has one of the world's richest oral poetic traditions, but literacy rates remain low in many communities. This tool:

- **Democratizes access** to metrical analysis for all users, regardless of technical training
- **Accelerates research** by automatically scanning large poetry collections
- **Preserves cultural knowledge** by making traditional prosody more accessible
- **Supports education** by helping learners understand the rhythmic structure of classical verse

### Technical Showcase

This project demonstrates:

| Skill Area | Implementation |
|------------|----------------|
| **Sequence Labeling** | Linear-chain CRF for structured prediction |
| **Feature Engineering** | Phonological features (vowel length, diphthongs, coda presence, word boundaries) |
| **NLP Pipeline** | Preprocessing  → Feature extraction → Prediction |
| **Model Deployment** | Streamlit web interface with caching and state management |
| **Evaluation** | 97% test accuracy on syllable-level F1 and exact sequence prediction |

---

## Quick Start

### Running Online

go to www.ayubnur.com/jiifto (this redirects to https://jiifto.streamlit.app/)


### Running Locally

```bash
# Clone the repository
git clone https://github.com/yourusername/jiifto-scansion.git
cd jiifto-scansion

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## How to Use

1. **Enter Text**: Paste Somali Jiifto poetry in the left panel (one line per line)
2. **Click Process**: The model analyzes each syllable
3. **View Results**: See the metrical pattern displayed in the right panel

### Output Columns

| Column | Description |
|--------|-------------|
| `syllables` | Tokenized syllable sequence |
| `pred_meter` | Predicted metrical labels (S = short, L = long) |
| `sum` | Total moraic weight of the line |

---

## 🔬 Technical Details

### Model Architecture

```
Input Text 
    ↓
Rule-Based Syllabifier (SomSyll)
    ↓
Feature Extraction
    ├─ Syllable identity
    ├─ Vowel length heuristics
    ├─ Coda presence
    ├─ Word boundary indicators
    └─ Positional features
    ↓
Linear-Chain CRF
    ↓
Metrical Labels
```

### Performance

| Class | Precision | Recall | F1-score | 
| ----: | --------: | -----: | -------: |
|     L |      0.95 |   0.94 |     0.94 |
|     S |      0.97 |   0.98 |     0.98 | 

The model achieves state-of-the-art performance on Jiifto poetry due to the genre's strict metrical constraints and our linguistically-motivated feature set.

---

## Future Work

- **Genre Expansion**: Extend to other Somali poetic forms (Gabay, Geeraar, Buraanbur)
- **Ambiguity Handling**: Probabilistic outputs for less constrained genres (modern lyrics, spoken narrative)
- **Interactive Learning**: Allow users to correct predictions and retrain the model
- **Mobile Deployment**: Reach users in low-connectivity regions
- **Multilingual Extension**: Apply the framework to other oral poetic traditions

---



## Citation
Coming soon.
<!--
If you use this tool in your research, please cite:

```bibtex
@article{,
  title={},
  author={Nur, Ayub AND Ali, Awo},
  year={2026}
}
```
-->
---


## Contact & Feedback

Have questions, suggestions, or want to collaborate? Open an issue or reach out directly!

---
