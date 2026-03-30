#F1 Race Finish Position Predictor

## Overview
A machine learning web app that predicts where an F1 driver
will finish in a race based on qualifying position, team,
circuit, and recent form.

Built as part of my AIML learning journey using real-world
Formula 1 data from the Ergast API dataset (2010–2023).

---

## Live Demo
Run locally — see setup instructions below.

---

## Tech Stack
| Component | Tool |
|---|---|
| Language | Python |
| ML Model | XGBoost Regressor |
| Data | Ergast F1 Dataset (Kaggle) |
| App Framework | Streamlit |
| Libraries | pandas, scikit-learn, matplotlib, joblib |

---

## Features
- Predict race finish position for any driver + circuit combo
- 6 input features: grid position, constructor, driver,
  circuit, avg points last 3 races, weather indicator
- Time-based train/test split (2010-2021 train, 2022+ test)
- Podium probability indicator
- Data Insights tab: grid vs finish chart,
  top constructors, pole-to-win %
- XGBoost vs Random Forest comparison — 5% MAE improvement

---

## Model Performance
| Model | MAE |
|---|---|
| Random Forest (baseline) | 3.02 positions |
| XGBoost (final) | 2.87 positions |

MAE of 2.87 means predictions are within ~3 positions
on average — realistic for F1 given the inherent
unpredictability of safety cars and retirements.

---

## Key Insight
Grid (qualifying) position was the strongest predictor —
confirmed by feature importance analysis. This aligns with
real-world F1 knowledge: pole position converts to a race
win ~40% of the time in modern F1.

---

## How to Run
1. Clone this repo
```
//github.com/yourahul/f1-race-predictor.git
cd f1-race-predictor
```

2. Install dependencies
```
pip install -r requirements.txt
```
pip install -r requirements.txt
```

3. Download the Ergast F1 dataset from Kaggle:
   https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020

4. Run the Jupyter notebook to train and save the model
```
jupyter notebook F1_project.ipynb
```

5. Launch the Streamlit app
```
streamlit run app.py
```

---
## Project Structure
```
f1-race-predictor/
├── F1_project.ipynb     # Full ML pipeline
├── app.py               # Streamlit web app
├── requirements.txt     # Dependencies
└── predication.png       # App preview
```

---

## Dataset
Ergast F1 World Championship Dataset (1950–2023)
Source: Kaggle
Features used: results, races, constructors, drivers

---

## Author
**Rahul U**
LinkedIn:www.linkedin.com/in/rahul-u-507b57286
