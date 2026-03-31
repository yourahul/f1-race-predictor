# 🏎️ F1 Race Finish Position Predictor

![F1 Predictor]
> Predicting Formula 1 race finishing positions using machine learning — built with real Ergast F1 data, trained on 1,600+ race records, and deployed as an interactive Streamlit web app.

---

## Overview

This project predicts where an F1 driver will finish in a race based on qualifying grid position, constructor performance, circuit, and recent form. Built end-to-end — from raw data merging and feature engineering to model training, evaluation, and a fully deployed web application.

The dataset covers the **2010–2025 F1 seasons** (1,600+ race entries), filtered to the modern era where regulations and team structures are consistent and relevant.

---

## Live App

Clone the repo and run locally — setup instructions at the bottom.

---

## Tech Stack

| Component        | Tool                          |
|------------------|-------------------------------|
| Language         | Python 3                      |
| ML Model         | XGBoost Regressor             |
| Baseline Model   | Random Forest Regressor       |
| App Framework    | Streamlit                     |
| Data Handling    | pandas, numpy                 |
| Visualisation    | matplotlib                    |
| Model Persistence| joblib                        |
| Dataset Source   | Ergast F1 API (via Kaggle)    |

---

## Features

- **Predict race finish position** for any driver, constructor, and circuit combination
- **5 model input features** — grid position, constructor, driver, circuit, and average points scored in last 3 races
- **Weather condition indicator** — Dry / Wet / Mixed with contextual warnings
- **Podium probability bar** — visual chance of top 3 finish
- **Time-based train/test split** — trained on 2010–2021 seasons, tested on 2022–2025 (realistic, not random)
- **Model comparison** — XGBoost vs Random Forest side by side
- **Data Insights tab** — grid vs average finish chart, top constructors, pole-to-win percentage

---

## Model Performance

| Model                    | MAE (positions) |
|--------------------------|-----------------|
| Random Forest (baseline) | 3.02            |
| **XGBoost (final)**      | **2.87**        |

**MAE of 2.87** means the model predicts finishing position within ~3 places on average on unseen 2022–2025 race data. This is realistic — F1 has inherent unpredictability from safety cars, mechanical retirements, and strategy calls that no historical model can fully capture.

---

## Key Insight

**Grid (qualifying) position was the strongest predictor** — confirmed by XGBoost feature importance analysis. Pole position converted to a race win in approximately **40% of modern F1 races**, which the model identified purely from data without being told.

This aligns with real-world F1 knowledge — track position, clean air, and avoiding first-lap incidents all stem from where you start on the grid.

---

## Dataset

**Ergast F1 World Championship Dataset**
- Source: [Kaggle — Formula 1 World Championship (1950–2025)](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020)
- Files used: `results.csv`, `races.csv`, `drivers.csv`, `constructors.csv`
- Full dataset: 1,149 races · 616 drivers · 168 constructors · 77 circuits
- Model trained on: 2010–2021 (1,200 race entries)
- Model tested on: 2022–2025 (400 race entries)

---

## Feature Engineering

- **`points_last_3`** — rolling 3-race average of points scored per driver, capturing recent form. This column was engineered from raw data and does not exist in the original dataset.
- **`circuit_encoded`** — label-encoded circuit ID, allowing the model to learn circuit-specific patterns
- **`driver_encoded`** and **`constructor_encoded`** — label-encoded identities

---

## Project Structure

```
f1-race-predictor/
├── F1_project.ipynb      # Full ML pipeline — data loading, EDA,
│                         # feature engineering, training, evaluation
├── app.py                # Streamlit web app
├── requirements.txt      # All dependencies
├── screenshot.png        # App preview
└── README.md             # This file
```

> **Note:** CSV data files and `.pkl` model files are not included in this repo. Download the dataset from Kaggle and run the notebook to generate the model files before launching the app.

---

## How to Run

**1. Clone the repository**
```bash
git clone https://github.com/yourahul/f1-race-predictor.git
cd f1-race-predictor
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Download the dataset**

Get the Ergast F1 dataset from Kaggle and place these files in the project folder:
`results.csv`, `races.csv`, `drivers.csv`, `constructors.csv`, `qualifying.csv`

**4. Train the model**

Open and run all cells in `F1_project.ipynb`. This generates:
`f1_model.pkl`, `le_driver.pkl`, `le_constructor.pkl`, `le_circuit.pkl`

**5. Launch the app**
```bash
streamlit run app.py
```

---

## What I Learned

- End-to-end ML project workflow — raw data to deployed application
- Merging multiple relational CSV files using pandas
- Rolling feature engineering for time-series data
- Label encoding categorical variables for ML models
- Time-based train/test splitting for realistic evaluation
- Comparing multiple models (Random Forest vs XGBoost)
- Building and deploying interactive ML apps with Streamlit

---

## Author

**Rahul U**

Electronics and Communication Engineering
[GitHub](https://github.com/yourahul) · [LinkedIn](https://www.linkedin.com/in/rahul-u-507b57286)
