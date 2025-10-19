# ForecastIQ — Weather Prediction Tool

## 🚀 Live Demo
**Try the app now:** [https://forecastiq-weather-prediction-tool-2025.streamlit.app/](https://forecastiq-weather-prediction-tool-2025.streamlit.app/)

Get instant weather predictions by entering 14 environmental parameters including location, meteorology, and WHO air-quality metrics. Download your personalized weather report as a PDF!

---

ForecastIQ is a Streamlit app and ML workflow for predicting weather from environmental features, with a special focus on the six WHO air-quality indicators. It lets you input 14 features to get rainfall and temperature predictions, and includes a notebook that trains and compares multiple models.

## Contents
- Overview
- Features
- Project structure
- Data and features
- Models and tasks
- Installation (Windows)
- Run the app
- Train and export models (notebook)
- Troubleshooting
- License and contact

## Overview
The goal is to predict temperature and rainfall based on environmental and air-quality variables, and to study how WHO air-quality parameters relate to climate outcomes. The repository contains:
- A Streamlit UI (`app.py`) to make predictions with pre-trained models and download a styled HTML/PDF report.
- A Jupyter notebook (`final1.ipynb`) that loads the dataset, explores features, trains multiple algorithms (Extra Trees, RandomForest, XGBoost, LightGBM, SVM), evaluates results, and saves the best models with Joblib.

## Features
- Interactive Streamlit UI with 14 numeric inputs (geography, meteorology, WHO air-quality metrics)
- Predicts:
	- Rainfall amount (mm)
	- Temperature (°C)
	- Rain occurrence class (Rain / No Rain)
	- Temperature category (Cold / Moderate / Hot)
- Generates a styled HTML report and a downloadable PDF (WeasyPrint when available; ReportLab fallback)
- Notebook includes data prep (log transform, binning), model training, evaluation charts, and model export to `.pkl`

## Project structure
```
app.py                      # Streamlit application (inputs, predictions, report/PDF)
final1.ipynb                # End-to-end training & evaluation notebook
requirements.txt            # Dependency list (also see requirement.txt)
requirement.txt             # Same list for tools that expect this filename
README.md                   # This file
__pycache__/                # Bytecode (ignored by git)
```

Expected (generated/provided at runtime):
- `et_reg_rain.pkl` — ExtraTrees regression model (log rainfall)
- `et_reg_temp.pkl` — ExtraTrees regression model (temperature)
- `et_cls_rain.pkl` — ExtraTrees classifier (rain occurrence)
- `et_cls_temp.pkl` — ExtraTrees classifier (temperature category)
- `character.png` (optional) — Decorative image used in the PDF footer

## Data and features
Notebook dataset (example): `IndianWeatherRepository.xlsx`
- The notebook reads Excel via `pandas.read_excel`, so `openpyxl` is required.
- Targets created in the notebook:
	- `log_precip_mm = log1p(precip_mm)` for rainfall regression (de-skew)
	- `rain_occurred = (precip_mm > 0).astype(int)` for binary classification
	- Temperature categories via `KBinsDiscretizer(n_bins=3, strategy='quantile')`

App input features (14 numeric fields, all required):
```
latitude, longitude,
humidity, wind_kph, cloud, pressure_mb, uv_index, feels_like_celsius,
air_quality_Carbon_Monoxide, air_quality_Ozone,
air_quality_Nitrogen_dioxide, air_quality_Sulphur_dioxide,
air_quality_PM2.5, air_quality_PM10
```

## Models and tasks
The workflow supports four prediction tasks:
1) Rainfall amount (regression on `log_precip_mm`, converted back using expm1 in the app)
2) Temperature value (regression on `temperature_celsius`)
3) Rain occurrence (binary classification: No Rain / Rain)
4) Temperature category (multi-class classification: Cold / Moderate / Hot)

Algorithms evaluated in the notebook:
- Extra Trees (final `.pkl` models used by the app)
- Random Forest
- XGBoost
- LightGBM
- SVM (SVR/SVC)

Sample classification accuracies reported in the notebook:
- Rain occurrence: ExtraTrees ≈ 92.99%, LightGBM ≈ 92.38%, XGBoost ≈ 92.08%, RandomForest ≈ 91.85%, SVM ≈ 87.28%
- Temperature category: XGBoost ≈ 97.72%, LightGBM ≈ 97.64%, ExtraTrees ≈ 96.19%, RandomForest ≈ 97.03%, SVM ≈ 92.61%

## Installation (Windows / PowerShell)
1) Create and activate a virtual environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
2) Install dependencies
```powershell
pip install -r requirements.txt
# or
pip install -r requirement.txt
```
3) PDF support (choose one)
- pdfkit + wkhtmltopdf: install the wkhtmltopdf binary from https://wkhtmltopdf.org/downloads.html and ensure it is in PATH
- WeasyPrint: install via pip (already listed) and ensure required native libraries (Cairo, Pango) are installed on Windows

## Run the app
```powershell
streamlit run app.py
```
Then, in the UI:
1) Enter all 14 feature values (non-zero required)
2) Click Predict to see rainfall (mm), temperature (°C), rain occurrence, and temperature class
3) Scroll to view the full HTML report; download PDF when available (or download HTML as a fallback)

Required model files in the repo root:
```
et_reg_rain.pkl  et_reg_temp.pkl  et_cls_rain.pkl  et_cls_temp.pkl
```

## Train and export models (notebook)
Open `final1.ipynb` and run cells in order:
1) Load data (`IndianWeatherRepository.xlsx`), inspect, and clean
2) Create targets: `log_precip_mm`, `rain_occurred`, temperature bins
3) Split data and train models (ExtraTrees, RF, XGBoost, LightGBM, SVM)
4) Evaluate: MSE for regression; accuracy/confusion matrices for classification
5) Save chosen ExtraTrees models:
```python
import joblib
joblib.dump(et_reg_rain, "et_reg_rain.pkl")
joblib.dump(et_reg_temp, "et_reg_temp.pkl")
joblib.dump(et_cls_rain, "et_cls_rain.pkl")
joblib.dump(et_cls_temp, "et_cls_temp.pkl")
```

## Troubleshooting
- Missing model files: the app will fail on `joblib.load`. Train and export the four `.pkl` files as above and place them next to `app.py`.
- PDF generation fails: install wkhtmltopdf (for pdfkit) or WeasyPrint + system deps; otherwise use the “Download HTML (fallback)” option.
- Version mismatch unpickling models: ensure your environment uses compatible `scikit-learn` version with the one used to create the `.pkl` files.
- Excel reading error: ensure `openpyxl` is installed.
- “Please fill in all required fields”: all 14 inputs must be non-zero before predicting.

## Contact

Designed and developed by Varshini J
- GitHub: https://github.com/varshinijayaprabhu
- LinkedIn: https://www.linkedin.com/in/varshinij2004
