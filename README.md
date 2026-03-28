## WORK CULTURE INDEX Project
### Dashboard Link - https://wci-project-rahul.streamlit.app/

A quantitative framework for measuring workplace culture from unstructured employee review text. Built as an internship research project, focused on Indian Manufacturing and IT Services companies listed on AmbitionBox.

---
## Overview
The WCI pipeline converts raw employee reviews into a composite 0–100 score per company, using a blend of transformer-based sentiment analysis and expert-weighted theme scoring. The final scores are surfaced through an interactive Streamlit dashboard.

**Companies covered:** Tata Motors · Hero Motocorp · LTIMindtree · Jay Ushin · Roto Pumps · Veljan Denison  
**Total reviews:** ~6,628 across 6 companies  
**Sectors:** Automotive, Two-Wheeler, Auto Components, Industrial Pumps, Hydraulics, IT Services

---

## Pipeline

```
Raw reviews (Data.xlsx + ltimindtree_reviews.csv)
        ↓
    Cleaning & deduplication
        ↓
    Sentiment scoring  (RoBERTa + VADER ensemble)
        ↓
    Theme scoring  (5 themes via keyword × sentiment)
        ↓
    WCI construction  (PCA + expert weights, normalized 0–100)
        ↓
    Dashboard  (Streamlit + Plotly)
```

All steps live in `code_file_main.ipynb`. The notebook produces a series of intermediate CSVs that feed into `app.py`.

---

## Methodology

**Sentiment models**  
RoBERTa (`cardiffnlp/twitter-roberta-base-sentiment-latest`) and VADER are run in parallel and blended via confidence weighting. Separate scores are computed for `like_text` and `dislike_text` fields.

**Combined sentiment**  
`combined = 0.40 × like_sentiment + 0.60 × dislike_sentiment`  
The 40/60 split is grounded in Baumeister et al. (2001) negativity bias.

**Five themes scored per review**

| Theme | Expert Weight |
|---|---|
| Respect & Fairness | 0.28 |
| Management Quality | 0.24 |
| Compensation & Benefits | 0.20 |
| Growth & Learning | 0.16 |
| Work-Life Balance | 0.12 |

**WCI construction**  
Firm-level theme scores are aggregated, then weighted by a blend of PCA-derived weights (objective) and the expert weights above. The blend parameter Q is tuned via Leave-One-Out cross-validation against average star ratings. Raw scores are normalized to 0–100.

**Robustness**  
Rankings are tested under four alternative like/dislike splits (50/50, 40/60, 35/65, 30/70). Spearman rank correlation = 1.0 across all configurations.

---

## Dashboard Pages

| Page | Contents |
|---|---|
| Home & Leaderboard | WCI ranking chart, rank cards, key insights |
| Company Profile | Radar chart, sentiment trends, theme breakdown, sample reviews |
| Head-to-Head | Side-by-side comparison of any two companies |
| Regression & Insights | OLS results, WCI vs star rating scatter, sensitivity analysis |

---

## Key Finding

Higher WCI scores associate with *lower* average star ratings (negative OLS beta). This is intentional — text sentiment and star ratings capture different dimensions of workplace experience. The divergence is a central insight of the project.

> Veljan Denison (n = 35) results are marked with an asterisk throughout the dashboard. Treat with caution.

---

## Setup

```bash
conda activate LEO_environment
cd path/to/wci-analysis
streamlit run app.py
```

The notebook must be run end-to-end before launching the dashboard to generate the required CSV files.

**Key dependencies:** `transformers`, `vaderSentiment`, `scikit-learn`, `statsmodels`, `streamlit`, `plotly`, `pandas`, `scipy`

---

## File Structure

```
wci-analysis/
├── Data.xlsx                      # Raw input (merged in Cell 1)
├── ltimindtree_reviews.csv        # LTIMindtree scrape
├── data_cleaned.csv
├── data_sentiment.csv
├── data_themes.csv
├── data_final.csv                 # Dashboard input
├── wci_scores.csv                 # Per-company WCI scores and ranks
├── wci_weights.csv                # Theme weights (expert + PCA + final)
├── app.py                         # Streamlit dashboard
├── clening_data_stage_1.ipynb     # Full pipeline
└── requirements.txt
```

---

## References

- Baumeister et al. (2001) — negativity bias in sentiment weighting
- Chen et al. (2021) — composite index construction via PCA + expert weights
- Cardiff NLP (2022) — RoBERTa sentiment model
- Hutto & Gilbert (2014) — VADER
- Uyeno (2020) — theme selection from Glassdoor data
