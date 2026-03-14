<div align="center">

# 🌦️ ForecastIQ — Weather Prediction Tool

### AI-Powered Weather Forecasting with WHO Air Quality Integration

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Demo-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://forecastiq-weather-prediction-tool-2025.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML%20Models-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-97.72%25%20Acc-006400?style=for-the-badge)](https://xgboost.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

**ForecastIQ** is an intelligent ML-powered weather prediction platform built with Streamlit. Enter 14 environmental parameters — including location, meteorology, and WHO air-quality metrics — to instantly predict rainfall, temperature, and weather categories. Download a personalized, styled PDF report with every prediction.

</div>

---

## 🚀 Live Demo

**Try the app now:** [https://forecastiq-weather-prediction-tool-2025.streamlit.app/](https://forecastiq-weather-prediction-tool-2025.streamlit.app/)

Get instant weather predictions by entering 14 environmental parameters including location, meteorology, and WHO air-quality metrics. Download your personalized weather report as a PDF!

https://github.com/user-attachments/assets/370fce6a-07a0-4159-bb44-cdbce33b2487

---

## ✨ Key Highlights

- **🌧️ Rain Occurrence Classifier** — 92.99% accuracy (ExtraTrees) for predicting rainfall events
- **🌡️ Temperature Classifier** — 97.72% accuracy (XGBoost) for temperature category prediction
- **📊 14-Parameter Input System** — Geography, meteorology & all 6 WHO air-quality indicators
- **📄 PDF Report Generation** — Download a beautifully styled personalized weather report
- **🔬 5-Algorithm Comparison** — Extra Trees, Random Forest, XGBoost, LightGBM, SVM benchmarked
- **🌍 WHO Air Quality Integration** — CO, Ozone, NO2, SO2, PM2.5, PM10 as prediction features
- **📓 End-to-End Notebook** — Full training pipeline with evaluation charts and model export
- **⚡ Streamlit UI** — Interactive, responsive web interface with instant predictions
- **📁 Dual Output Format** — HTML report with PDF download (WeasyPrint / ReportLab fallback)
- **🔒 Reproducible Pipeline** — Joblib-serialized models for consistent, version-safe inference

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Data & Input Features](#-data--input-features)
- [Models & Tasks](#-models--tasks)
- [Model Accuracy Results](#-model-accuracy-results)
- [Technologies Used](#-technologies-used)
- [Installation](#-installation-windows--powershell)
- [Run the App](#-run-the-app)
- [Train & Export Models](#-train--export-models-notebook)
- [Troubleshooting](#-troubleshooting)
- [Contact](#-contact)

---

## 🌐 Overview

ForecastIQ predicts temperature and rainfall based on environmental and air-quality variables, studying how WHO air-quality parameters relate to climate outcomes. The repository contains:

- A **Streamlit UI** (`app.py`) to make predictions with pre-trained models and download a styled HTML/PDF report.
- A **Jupyter notebook** (`final1.ipynb`) that loads the dataset, explores features, trains multiple algorithms (Extra Trees, RandomForest, XGBoost, LightGBM, SVM), evaluates results, and saves the best models with Joblib.

---

## 🔧 Features

### 🌦️ Core Prediction Features
- **Rainfall Amount Regression** — Predicts precise rainfall in mm using log-transform pipeline
- **Temperature Regression** — Continuous temperature prediction in Celsius
- **Rain Occurrence Classification** — Binary prediction: Rain / No Rain
- **Temperature Category Classification** — Multi-class: Cold / Moderate / Hot
- **14-Feature Input Interface** — All geographic, meteorological, and air-quality parameters

### 🌍 WHO Air Quality Integration
- **Carbon Monoxide (CO)** — Air quality feature for climate correlation
- **Ozone (O3)** — Atmospheric ozone as a weather predictor
- **Nitrogen Dioxide (NO2)** — Pollution-weather relationship modeling
- **Sulphur Dioxide (SO2)** — Industrial emission impact on weather
- **PM2.5 & PM10** — Particulate matter as environmental indicators
- **Cross-domain Analysis** — Studies how air quality drives climate outcomes

### 📊 ML Pipeline Features
- **Multi-Algorithm Benchmarking** — 5 algorithms evaluated side-by-side
- **Log Transform Preprocessing** — `log1p` de-skewing for rainfall regression
- **KBinsDiscretizer Binning** — Quantile-based temperature categorization
- **Confusion Matrix Visualization** — Per-class evaluation charts in notebook
- **MSE & Accuracy Reporting** — Regression and classification metrics
- **Joblib Model Serialization** — Portable `.pkl` models for deployment

### 📄 Report & Export Features
- **Styled HTML Report** — Full-page personalized prediction summary
- **PDF Download** — WeasyPrint (primary) or ReportLab (fallback) generation
- **HTML Fallback Download** — Always-available report export option
- **Decorative Report Footer** — Optional `character.png` branding in PDF

### 🖥️ UI/UX Features
- **Responsive Streamlit Design** — Works on desktop and tablet browsers
- **Instant Prediction Feedback** — Real-time results on form submission
- **Input Validation** — All 14 fields required with non-zero enforcement
- **Clean Numeric Input Interface** — Organized by feature category
- **Browser Compatibility** — Chrome, Firefox, Opera, Brave support

### ⚙️ Development & Production Features
- **Cross-platform Compatibility** — Windows 11, macOS, Linux
- **Virtual Environment Support** — Isolated dependency management
- **Notebook-to-App Workflow** — Train in notebook, deploy via Streamlit
- **SDLC Best Practices** — Structured development and evaluation pipeline
- **Scalable Architecture** — Extendable with new features and datasets

---

## 📁 Project Structure

```
ForecastIQ/
├── app.py                      # Streamlit application (inputs, predictions, report/PDF)
├── final1.ipynb                # End-to-end training & evaluation notebook
├── requirements.txt            # Dependency list
├── README.md                   # This file
├── __pycache__/                # Bytecode (ignored by git)
│
├── et_reg_rain.pkl             # ExtraTrees regression model (log rainfall)      [generated]
├── et_reg_temp.pkl             # ExtraTrees regression model (temperature)       [generated]
├── et_cls_rain.pkl             # ExtraTrees classifier (rain occurrence)         [generated]
└── et_cls_temp.pkl             # ExtraTrees classifier (temperature category)    [generated]
```

---

## 📐 Data & Input Features

**Notebook dataset:** `IndianWeatherRepository.xlsx`
- Read via `pandas.read_excel` — requires `openpyxl`

**Targets created in the notebook:**

| Target | Type | Description |
|---|---|---|
| `log_precip_mm` | Regression | `log1p(precip_mm)` — de-skewed rainfall |
| `rain_occurred` | Classification | `(precip_mm > 0).astype(int)` — binary |
| Temperature bins | Classification | `KBinsDiscretizer(n_bins=3, strategy='quantile')` |

**App input features (14 numeric fields — all required):**

| Category | Features |
|---|---|
| Geography | `latitude`, `longitude` |
| Meteorology | `humidity`, `wind_kph`, `cloud`, `pressure_mb`, `uv_index`, `feels_like_celsius` |
| WHO Air Quality | `air_quality_Carbon_Monoxide`, `air_quality_Ozone`, `air_quality_Nitrogen_dioxide`, `air_quality_Sulphur_dioxide`, `air_quality_PM2.5`, `air_quality_PM10` |

---

## 🤖 Models & Tasks

The workflow supports **four prediction tasks**:

| # | Task | Type | Target |
|---|---|---|---|
| 1 | Rainfall Amount | Regression | `log_precip_mm` converted back via `expm1` |
| 2 | Temperature Value | Regression | `temperature_celsius` |
| 3 | Rain Occurrence | Binary Classification | No Rain / Rain |
| 4 | Temperature Category | Multi-class Classification | Cold / Moderate / Hot |

**Algorithms evaluated:**
- ⭐ **Extra Trees** — Final `.pkl` models deployed in the app
- 🌲 **Random Forest**
- 🚀 **XGBoost**
- 💡 **LightGBM**
- 🔵 **SVM** (SVR for regression / SVC for classification)

---

## 📈 Model Accuracy Results

### Rain Occurrence Classification

| Model | Accuracy |
|---|---|
| ⭐ ExtraTrees | **92.99%** |
| LightGBM | 92.38% |
| XGBoost | 92.08% |
| Random Forest | 91.85% |
| SVM | 87.28% |

### Temperature Category Classification

| Model | Accuracy |
|---|---|
| ⭐ XGBoost | **97.72%** |
| LightGBM | 97.64% |
| Random Forest | 97.03% |
| ExtraTrees | 96.19% |
| SVM | 92.61% |

---

## 🛠️ Technologies Used

### Backend & ML

| Technology | Purpose |
|---|---|
| **Python 3.10+** | Core language |
| **scikit-learn** | Extra Trees, Random Forest, SVM, preprocessing |
| **XGBoost** | Gradient boosting classifier & regressor |
| **LightGBM** | Fast gradient boosting |
| **Joblib** | Model serialization (`.pkl` export/load) |
| **NumPy / Pandas** | Data manipulation and feature engineering |
| **openpyxl** | Excel dataset reading |

### Frontend & Reporting

| Technology | Purpose |
|---|---|
| **Streamlit** | Interactive web UI |
| **WeasyPrint** | Primary PDF generation |
| **ReportLab** | PDF fallback generator |
| **Matplotlib / Seaborn** | Evaluation charts in notebook |
| **Pillow** | Image handling for PDF report |

---

## ⚙️ Installation (Windows / PowerShell)

**1. Clone the repository**
```powershell
git clone https://github.com/varshinijayaprabhu/ForecastIQ-Weather-Prediction-Tool.git
cd "ForecastIQ  Weather Prediction Tool"
```

**2. Create and activate a virtual environment**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**3. Install dependencies**
```powershell
pip install -r requirements.txt
```

**4. PDF support (choose one)**
- **WeasyPrint** — already in `requirements.txt`; ensure Cairo & Pango native libs are installed on Windows
- **pdfkit + wkhtmltopdf** — download the binary from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html) and ensure it is in PATH

---

## ▶️ Run the App

```powershell
streamlit run app.py
```

In the UI:
1. Enter all **14 feature values** (non-zero required)
2. Click **Predict** to see rainfall (mm), temperature (°C), rain occurrence, and temperature class
3. Scroll to view the full **HTML report**
4. Click **Download PDF** (or "Download HTML" as fallback)

**Required model files in the repo root:**
```
et_reg_rain.pkl    et_reg_temp.pkl    et_cls_rain.pkl    et_cls_temp.pkl
```

---

## 📓 Train & Export Models (Notebook)

Open `final1.ipynb` and run cells in order:

1. **Load data** — Read `IndianWeatherRepository.xlsx`, inspect, and clean
2. **Create targets** — `log_precip_mm`, `rain_occurred`, temperature bins
3. **Split & train** — ExtraTrees, RF, XGBoost, LightGBM, SVM
4. **Evaluate** — MSE for regression; accuracy & confusion matrices for classification
5. **Export models:**

```python
import joblib
joblib.dump(et_reg_rain,  "et_reg_rain.pkl")
joblib.dump(et_reg_temp,  "et_reg_temp.pkl")
joblib.dump(et_cls_rain,  "et_cls_rain.pkl")
joblib.dump(et_cls_temp,  "et_cls_temp.pkl")
```

---

## ❓ Troubleshooting

| Issue | Solution |
|---|---|
| **Missing model files** | App will fail on `joblib.load` — train and export the four `.pkl` files and place them next to `app.py` |
| **PDF generation fails** | Install wkhtmltopdf (pdfkit) or WeasyPrint + system deps; use "Download HTML (fallback)" otherwise |
| **Version mismatch unpickling** | Ensure `scikit-learn` version matches the one used to create the `.pkl` files |
| **Excel reading error** | Ensure `openpyxl` is installed (`pip install openpyxl`) |
| **"Fill in all required fields"** | All 14 inputs must be non-zero before predicting |

---

## 📬 Contact

<div align="center">

**Designed and developed by Varshini J**

[![GitHub](https://img.shields.io/badge/GitHub-varshinijayaprabhu-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/varshinijayaprabhu)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-varshinij2004-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/varshinij2004)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-ForecastIQ-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://forecastiq-weather-prediction-tool-2025.streamlit.app/)

---

*⭐ If you found this project useful, consider giving it a star on GitHub!*

</div>
